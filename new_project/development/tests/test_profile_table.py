import ast
import copy
import tempfile
import time
import unittest
from pathlib import Path
from types import SimpleNamespace

from govoffice.adapters.json_user_profile import JSON사용자프로필저장소
from govoffice.domain.user_profile import 사용자프로필
from govoffice.services.profile_table import ProfileTableCommands


def block(*pairs):
    return '<HWPML><BODY><SECTION><TABLE>' + ''.join(
        '<ROW>' + ''.join(f'<CELL><P><TEXT><CHAR>{s}</CHAR></TEXT></P></CELL>' for s in pair) + '</ROW>'
        for pair in pairs) + '</TABLE></SECTION></BODY></HWPML>'


class ProfileTableTest(unittest.TestCase):
    def test_modeless_manager_rejects_stale_legacy_button_writes(self):
        source=Path(__file__).resolve().parents[2].joinpath('gui_backend.py').read_text(encoding='utf-8')
        handler=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='처리')
        prefix=[]
        for node in handler.body:
            prefix.append(node)
            if isinstance(node,ast.If) and 'snapshot' in ast.unparse(node.test):
                break
        self.assertIn('profile_writes',ast.unparse(ast.Module(body=prefix,type_ignores=[])))
        handler.body=prefix+[ast.Return(value=ast.Constant(value=True))]
        namespace={'사용자프로필저장소':self.repo}
        exec(compile(ast.fix_missing_locations(ast.Module(body=[handler],type_ignores=[])),'profile_guard','exec'),namespace)
        snapshot=self.repo.불러오기().사전()
        actions=['user_profile_entry_add','user_profile_aliases_set','user_profile_default_set',
                 'user_profile_field_parent_set','user_profile_field_delete','user_profile_entry_delete']
        for action in actions:
            self.assertTrue(namespace['처리']({'action':action,'snapshot':snapshot}))
            with self.assertRaisesRegex(ValueError,'다른 화면'):
                namespace['처리']({'action':action,'snapshot':{}})
        self.assertEqual(snapshot,self.repo.불러오기().사전())

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'profile.json'
        self.repo = JSON사용자프로필저장소(self.path)
        self.repo.저장(사용자프로필.생성({}))
        self.commands = ProfileTableCommands(self.repo)

    def mutate(self, field, op, **extra):
        return self.commands.mutate(dict(field_id=field, operation=op,
            snapshot=self.repo.불러오기().사전(), **extra))

    def seed(self):
        p = self.repo.불러오기().대표필드추가('연구자', ('그룹 값',))
        p = p.하위필드추가('연구자', '성명', ('홍길동', '김하늘'))
        p = p.대표필드추가('책임자')
        self.repo.저장(p)
        return p

    def test_real_selection_analysis_only_saves_checked_and_reuses_basic_alias(self):
        before = self.path.read_bytes()
        result = self.commands.analyze(block(('성명', '홍길동'), ('전화번호', '010-1234-5678')), ('doc', 1))
        self.assertEqual(before, self.path.read_bytes())
        selected = next(c for c in result['candidates'] if c['value'] == '홍길동')
        self.commands.save_selection(dict(draft_id=result['draft_id'], rows=[
            dict(candidate_id=selected['candidate_id'], field='성명', value=selected['value'])]), ('doc', 1))
        p = self.repo.불러오기()
        self.assertIn('홍길동', p.대표필드찾기('이름').값목록)
        self.assertFalse(p.대표필드찾기('전화번호').값목록)
        self.assertIsNone(self.commands.draft)
        self.assertEqual(['profile.json'], [f.name for f in Path(self.temp.name).iterdir()])

    def draft(self):
        result = self.commands.analyze(block(('성명', '홍길동'), ('전화번호', '010-1234-5678')), 'doc')
        rows = [dict(candidate_id=c['candidate_id'], field='연구자 > 성명', value=c['value']) for c in result['candidates']]
        return dict(draft_id=result['draft_id'], rows=rows)

    def test_same_path_groups_multiple_values_and_repeat_deduplicates(self):
        command = self.draft()
        self.commands.save_selection(command, 'doc')
        p = self.repo.불러오기();field = p.대표필드찾기('연구자 > 성명')
        self.assertGreaterEqual(len(field.값목록), 2)
        old_id = field.id
        command = self.draft();self.commands.save_selection(command, 'doc')
        new = self.repo.불러오기().대표필드찾기('연구자 > 성명')
        self.assertEqual(old_id, new.id);self.assertEqual(field.값목록, new.값목록)

    def test_invalid_last_row_leaves_repository_untouched(self):
        command = self.draft();command['rows'][-1]['field'] = '부모 > '
        before = self.path.read_bytes()
        with self.assertRaises(ValueError): self.commands.save_selection(command, 'doc')
        self.assertEqual(before, self.path.read_bytes())

    def test_stale_document_snapshot_unknown_duplicate_expired_rejected(self):
        for kind in ('document', 'snapshot', 'unknown', 'duplicate', 'expired', 'empty'):
            with self.subTest(kind=kind):
                command = self.draft();key = 'doc'
                if kind == 'document': key = 'other'
                elif kind == 'snapshot': self.repo.저장(self.repo.불러오기().대표필드추가('추가'))
                elif kind == 'unknown': command['rows'][0]['candidate_id'] = 'unknown'
                elif kind == 'duplicate': command['rows'].append(command['rows'][0])
                elif kind == 'expired': self.commands.draft['created_at'] = time.monotonic() - 901
                elif kind == 'empty': command['rows'] = []
                before = self.path.read_bytes()
                with self.assertRaises(ValueError): self.commands.save_selection(command, key)
                self.assertEqual(before, self.path.read_bytes())

    def test_move_parent_preserves_children_values_and_ids(self):
        p = self.seed();parent = p.대표필드찾기('연구자');child = p.대표필드찾기('연구자 > 성명');target = p.대표필드찾기('책임자')
        result = self.mutate(parent.id, 'move_field', target_id=target.id)
        self.assertEqual(child.id, result.대표필드찾기('책임자 > 연구자 > 성명').id)
        self.assertEqual(child.값목록, result.대표필드ID찾기(child.id).값목록)
        result = self.mutate(parent.id, 'move_field', target_id='')
        self.assertEqual(parent.id, result.대표필드찾기('연구자').id)

    def test_move_child_and_rename_preserve_id(self):
        p=self.seed();child=p.대표필드찾기('연구자 > 성명');target=p.대표필드찾기('책임자')
        self.mutate(child.id, 'move_field', target_id=target.id)
        result=self.mutate(child.id, 'edit_field', name='참여자 이름', aliases=['성명'])
        self.assertEqual(child.id, result.대표필드찾기('책임자 > 참여자 이름').id)
        self.assertEqual(child.값목록, result.대표필드ID찾기(child.id).값목록)

    def test_cycle_duplicate_names_basic_move_and_basic_delete_rejected(self):
        p=self.seed();parent=p.대표필드찾기('연구자');child=p.대표필드찾기('연구자 > 성명');basic=p.대표필드찾기('이름')
        for field, op, extra in (
            (parent.id, 'move_field', dict(target_id=child.id)),
            (parent.id, 'move_field', dict(target_id=parent.id)),
            (parent.id, 'edit_field', dict(name='책임자')),
            (basic.id, 'move_field', dict(target_id=parent.id)),
            (basic.id, 'delete_field', {}),
            (basic.id, 'edit_field', dict(name='성명 변경')),
        ):
            before=self.path.read_bytes()
            with self.assertRaises(ValueError):self.mutate(field,op,**extra)
            self.assertEqual(before,self.path.read_bytes())

    def test_value_edit_move_default_and_delete(self):
        p=self.seed();child=p.대표필드찾기('연구자 > 성명');target=p.대표필드찾기('책임자')
        result=self.mutate(child.id,'edit_value',value='홍길동',new_value='이예시')
        self.assertEqual('이예시',result.대표필드ID찾기(child.id).기본값)
        result=self.mutate(child.id,'move_value',value='이예시',target_id=target.id)
        self.assertEqual(('김하늘',),result.대표필드ID찾기(child.id).값목록)
        self.assertIn('이예시',result.대표필드ID찾기(target.id).값목록)
        self.mutate(target.id,'add_value',value='박예시')
        result=self.mutate(target.id,'default',value='박예시')
        self.assertEqual('박예시',result.대표필드ID찾기(target.id).기본값)
        result=self.mutate(target.id,'delete_value',value='박예시')
        self.assertEqual('이예시',result.대표필드ID찾기(target.id).기본값)

    def test_delete_subtree_only_and_stale_edit_rejected(self):
        p=self.seed();parent=p.대표필드찾기('연구자');child=p.대표필드찾기('연구자 > 성명')
        result=self.mutate(parent.id,'delete_field')
        self.assertIsNone(result.대표필드ID찾기(parent.id));self.assertIsNone(result.대표필드ID찾기(child.id))
        self.assertIsNotNone(result.대표필드찾기('책임자'))
        with self.assertRaises(ValueError): self.commands.mutate(dict(field_id=parent.id,operation='delete_field',snapshot=p.사전()))

    def test_backend_route_uses_live_selection_not_preset_draft_or_cache(self):
        source=Path(__file__).resolve().parents[2].joinpath('gui_backend.py').read_text(encoding='utf-8')
        parsed=ast.parse(source)
        handler=next(n for n in parsed.body if isinstance(n,ast.FunctionDef) and n.name=='처리')
        statements=handler.body
        branch=next(n for n in statements if isinstance(n,ast.If) and 'user_profile_selection_analyze' in ast.unparse(n.test))
        # Run the production branch against a fake document, real analyzer and isolated repository.
        responses=[];sentinel=object();draft={'unchanged':sentinel}
        key=('object','doc',True,'doc')
        ns=dict(action='user_profile_selection_analyze', 개인정보표명령=self.commands,
            한글=SimpleNamespace(선택영역서식내보내기=lambda **kw:block(('성명','홍길동'))),
            time=time,서식프리셋준비=lambda:None,현재선택문서키=lambda:key,문서키가현재문서인가=lambda k:k==key,
            안정사용자프로필=lambda:self.repo.불러오기(),응답=lambda *args,**kw:responses.append(kw),_서식초안=draft,
            _최근선택={'hwpml':block(('성명','이전선택'))})
        function=ast.FunctionDef(name='run',args=ast.arguments(posonlyargs=[],args=[],kwonlyargs=[],kw_defaults=[],defaults=[]),body=[branch],decorator_list=[])
        reader=next(n for n in parsed.body if isinstance(n,ast.FunctionDef) and n.name=='개인정보선택영역읽기')
        exec(compile(ast.fix_missing_locations(ast.Module(body=[reader,function],type_ignores=[])),'backend_test','exec'),ns)
        ns['run']()
        self.assertIs(ns['_서식초안'],draft)
        self.assertTrue(any(c['value']=='홍길동' for c in responses[0]['candidates']))
        self.assertFalse(any(c['value']=='이전선택' for c in responses[0]['candidates']))
        self.assertEqual([], list(self.repo.불러오기().대표필드찾기('이름').값목록))

    def selection_reader(self, cache, live=None, key=('object','doc',True,'doc')):
        source=Path(__file__).resolve().parents[2].joinpath('gui_backend.py').read_text(encoding='utf-8')
        parsed=ast.parse(source)
        reader=next(n for n in parsed.body if isinstance(n,ast.FunctionDef) and n.name=='개인정보선택영역읽기')
        def read(**kwargs):
            self.assertEqual({'선택텍스트검증': True}, kwargs)
            if live is None: raise ValueError('Selection lost when focus changed')
            return live
        ns=dict(한글=SimpleNamespace(선택영역서식내보내기=read),time=time,
                _최근선택=cache,현재선택문서키=lambda:key,문서키가현재문서인가=lambda k:k==key,
                안전문서상태=lambda:{})
        exec(compile(ast.fix_missing_locations(ast.Module(body=[reader],type_ignores=[])),'selection_test','exec'),ns)
        return ns['개인정보선택영역읽기']

    def test_never_substitutes_even_fresh_drag_for_current_selection(self):
        cache=dict(hwpml=block(('성명','홍길동')),document_key=('object','doc',True,'doc'),
                   source='drag_probe',captured_at=time.monotonic(),manual_token=None)
        with self.assertRaises(ValueError):
            self.selection_reader(cache)()
        source,key,origin=self.selection_reader(cache,live='fresh selection')()
        self.assertEqual('fresh selection',source);self.assertEqual('preset_saveblock',origin)

    def test_handoff_rejects_old_other_document_preset_manual_and_empty_caches(self):
        cache=dict(hwpml='selection',document_key=('object','doc',True,'doc'),
                   source='drag_probe',captured_at=time.monotonic(),manual_token=None)
        for change in [dict(captured_at=time.monotonic()-31),dict(document_key=('other','doc',True,'doc')),
                       dict(source=None),dict(source='preset_analysis'),dict(manual_token='manual'),dict(hwpml='')]:
            with self.subTest(change=change),self.assertRaises(ValueError):
                self.selection_reader({**cache,**change})()
        for key in [None,('object','output',True,'doc'),('object','doc',False,'doc')]:
            with self.subTest(key=key),self.assertRaises(ValueError):
                self.selection_reader(cache,live='selection',key=key)()

    def test_document_key_uses_restored_object_not_stale_connection(self):
        source=Path(__file__).resolve().parents[2].joinpath('gui_backend.py').read_text(encoding='utf-8')
        parsed=ast.parse(source)
        reader=next(n for n in parsed.body if isinstance(n,ast.FunctionDef) and n.name=='현재선택문서키')
        old=object();managed=object();original=SimpleNamespace(대상=old)
        def status():
            original.대상=managed
            return dict(managed=True,document_id='doc',active_document_id='doc')
        ns=dict(한글=SimpleNamespace(원본=original),안전문서상태=status)
        exec(compile(ast.Module(body=[reader],type_ignores=[]),'document_key_test','exec'),ns)
        first=ns['현재선택문서키']();second=ns['현재선택문서키']()
        self.assertEqual((id(managed),'doc',True,'doc'),first)
        self.assertEqual(first,second)


if __name__ == '__main__':
    unittest.main()
