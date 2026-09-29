"""Short GUI commands; authentication, extraction and writing never block its pipe."""
from pathlib import Path
import tempfile
import threading
import shutil
from uuid import uuid4

from govoffice.adapters.codex_author import CodexAuthor
from govoffice.adapters.hwp_form_export import export_generated_hwp
from govoffice.adapters.hwp_output_open import open_output_hwp
from govoffice.adapters.hwp_template_import import extract_hwp
from govoffice.services.document_authoring import AuthoringService, read_json, digest, parse_source
from govoffice.services.authoring_inputs import field_labels, validate_local_values, saved_profile_rows
from govoffice.adapters.json_user_profile import JSON사용자프로필저장소
from govoffice.services.user_profile import 사용자프로필서비스


class AuthoringCommands:
    def __init__(self, data_root):
        self.service = AuthoringService(data_root, CodexAuthor, export_generated_hwp)
        self.operations = {}
        self.operation_stops = {}
        self.lock = threading.RLock()
        self.account = {'connected': False, 'login_required': True}
        self.closed = threading.Event()
        self.profile = 사용자프로필서비스(JSON사용자프로필저장소(Path(data_root)/'user_profile.json'))

    def _operation(self, function):
        with self.lock:
            if any(o['status'] == 'running' for o in self.operations.values()):
                raise ValueError('연결 또는 등록 작업이 진행 중입니다.')
            op_id = uuid4().hex
            self.operations[op_id] = {'id': op_id, 'status': 'running'}
            self.operation_stops[op_id] = threading.Event()
        def run():
            try:
                result = function(op_id)
                with self.lock:
                    self.operations[op_id].update(status='completed', result=result)
            except Exception as exc:
                with self.lock:
                    self.operations[op_id].update(status='failed', error=str(exc))
        threading.Thread(target=run, daemon=True).start()
        return {'operation_id': op_id}

    def _auth(self, op_id, login):
        connection = CodexAuthor(self.service.root)
        try:
            status = connection.account()
            if login and not status['connected']:
                flow = connection.login_start()
                with self.lock:
                    self.operations[op_id]['login_url'] = flow['url']
                status = connection.login_wait(self.closed)
            with self.lock:
                self.account = status
            return status
        finally:
            connection.close()

    def _logout(self, op_id):
        connection = CodexAuthor(self.service.root)
        try:
            status = connection.logout()
            with self.lock:
                self.account = status
            return status
        finally:
            connection.close()

    def handle(self, command):
        action = command['action']
        if action == 'authoring_profile':
            return {'values':self.profile.불러오기().사전()}
        if action == 'authoring_profile_save':
            incoming = command.get('values')
            if not isinstance(incoming,dict) or set(incoming)-{'이름','전화번호','이메일'}:
                raise ValueError('기본 사용자 정보 형식이 올바르지 않습니다.')
            values = self.profile.불러오기().사전()
            for key in ('이름','전화번호','이메일'):
                values[key] = incoming.get(key,'')
            return {'values':self.profile.저장(values).사전()}
        if action == 'authoring_prepare_inputs':
            def prepare(op):
                m = self.service.registry.load(command.get('template_id'))
                root = parse_source(self.service.registry.path(m['id'])/'source.hwpml')
                labels = field_labels(root,list(root.iter('P')))
                for t in m['topics']:
                    for f in t['fields']:
                        f.setdefault('label',labels.get(f['index'],''))
                total = sum(len(t['fields']) for t in m['topics'])
                if not total:
                    raise ValueError('양식에서 입력할 빈칸을 찾지 못했습니다. 자동 작성 전에 입력 위치 연결이 필요합니다.')
                rows = saved_profile_rows(m, self.profile.불러오기())
                return {'template_id':m['id'],'rows':rows,
                        'total_fields':total, 'guides':m.get('guide_documents',[])}
            return self._operation(prepare)
        if action == 'authoring_validate_inputs':
            m = self.service.registry.load(command.get('template_id'))
            return {'values':validate_local_values(m,command.get('local_values'))}
        if action == 'authoring_guide_outline':
            m=self.service.registry.load(command.get('template_id'))
            return {'outline':m.get('guide_outline'), 'template_id':m['id']}
        if action == 'authoring_delete_template':
            if command.get('confirmed') is not True:raise ValueError('양식 삭제 확인이 필요합니다.')
            with self.lock,self.service.lock:
                self._require_idle_operation()
                if any(w.is_alive() for w in self.service.workers.values()):
                    raise ValueError('문서 작성이 끝나거나 중단된 뒤 양식을 삭제해 주세요.')
                return self.service.registry.delete(command.get('template_id'))
        if action == 'authoring_overview':
            templates, warnings = [], []
            for p in self.service.registry.folder.glob('*/manifest.json'):
                try:
                    m = read_json(p)
                    if m.get('registration_mode')=='guides_then_research_and_write':
                        from .template_guide_registration import registered_guided_reviews
                        reviews=registered_guided_reviews(self.service.registry,m)
                    else:reviews=m.get('analysis_reviews',[])
                    templates.append({'id': m['id'], 'name': m['name'], 'topics': len(m['topics']),
                                  'analysis_reviews':reviews,
                                  'review_mode':'guided_slots' if m.get('registration_mode')=='guides_then_research_and_write' else 'analysis',
                                  'input_slot_analysis':m.get('input_slot_analysis',{}),
                                  'has_slot_audit':bool(m.get('input_slot_audit_file')),
                                  'can_recheck_slots':bool(m.get('input_slot_audit_file') and reviews),
                                  'has_guide_outline':'guide_outline' in m,'analysis_version':m.get('analysis_sha256',''),
                                  'guide_file':str((p.parent/m['guide_file']).resolve()) if m.get('guide_file') else None,
                                  'folder': str(p.parent.resolve()), '_modified':p.stat().st_mtime})
                except (OSError, ValueError, KeyError, TypeError) as exc:
                    warnings.append({'template_id':p.parent.name,'message':'양식을 읽지 못해 목록에서 제외했습니다. 원본은 유지됩니다: '+str(exc)})
            templates.sort(key=lambda item:item.pop('_modified'), reverse=True)
            jobs = [self.service.status(p.parent.name) for p in sorted(self.service.jobs.glob('*/state.json'))]
            return {'templates': templates, 'template_warnings':warnings, 'jobs': sorted(jobs, key=lambda j:j['created_at'], reverse=True), 'account': self.account}
        if action in {'authoring_login', 'authoring_connection_check', 'authoring_logout'}:
            with self.lock, self.service.lock:
                if action != 'authoring_connection_check' and any(t.is_alive() for t in self.service.workers.values()):
                    raise ValueError('문서 작성 중에는 계정을 변경할 수 없습니다. 작성을 중단한 뒤 연결을 해제하세요.')
                return self._operation(self._logout if action == 'authoring_logout' else
                                       lambda op: self._auth(op, action == 'authoring_login'))
        if action == 'authoring_operation':
            with self.lock:
                return dict(self.operations[str(command['operation_id'])])
        if action == 'authoring_cancel_operation':
            with self.lock:
                self.operation_stops[str(command['operation_id'])].set()
                return {'requested':True}
        if action == 'authoring_register_builtin':
            def register(op):
                from govoffice.institutions.packages.seoultech.climate_2026.authoring import register_climate
                return register_climate(self.service.registry)
            return self._operation(register)
        if action in {'authoring_register_file', 'authoring_reanalyze_template'}:
            if action == 'authoring_reanalyze_template':
                existing=self.service.registry.load(command.get('template_id'))
                if existing.get('input_slot_audit_file'):
                    def recheck(op):
                        from .template_guide_registration import recheck_registered_guided
                        def progress(phase,done,total):
                            with self.lock:self.operations[op].update(phase=phase,completed=done,total=total)
                        with tempfile.TemporaryDirectory(prefix='govoffice_slot_recheck_') as tmp:
                            agent=self.service.agent_factory(Path(tmp))
                            try:
                                if not agent.account()['connected']:
                                    raise ValueError('입력칸을 재검토할 AI 계정을 먼저 연결해 주세요.')
                                return recheck_registered_guided(self.service.registry,existing['id'],agent,
                                    self.operation_stops[op],progress)
                            finally:agent.close()
                    return self._operation(recheck)
                source=self.service.registry.path(existing['id'])/'template.hwp'
                name=existing['name']
            else:
                source=Path(str(command.get('path',''))).resolve()
                name=source.stem
            def register_body(op):
                from .template_guide_registration import register_guided
                def progress(phase,done,total):
                    with self.lock:self.operations[op].update(phase=phase,completed=done,total=total)
                with tempfile.TemporaryDirectory(prefix='govoffice_authoring_form_') as tmp:
                    if not source.is_file() or source.suffix.lower()!='.hwp':raise ValueError('등록할 .hwp 파일을 선택해 주세요.')
                    agent=self.service.agent_factory(Path(tmp))
                    try:
                        if not agent.account()['connected']:raise ValueError('양식을 등록할 AI 계정을 먼저 연결해 주세요.')
                        copied=Path(tmp)/'template.hwp';shutil.copy2(source,copied)
                        xml=Path(tmp)/'source.hwpml'
                        progress('한글 양식 사본 읽는 중',0,1);extract_hwp(copied,xml)
                        return register_guided(self.service.registry,xml,copied,name,agent,
                                               self.operation_stops[op],progress)
                    finally:agent.close()
            return self._operation(register_body)
        if action == 'authoring_extract_guides':
            source = Path(str(command.get('path', ''))).resolve()
            def register(op):
                with tempfile.TemporaryDirectory(prefix='govoffice_registration_') as tmp:
                    if not source.is_file() or source.suffix.lower()!='.hwp':raise ValueError('등록할 .hwp 파일을 선택해 주세요.')
                    from .ai_guide_export import export_ai_guides
                    def progress(phase,done,total):
                        with self.lock:self.operations[op].update(phase=phase,completed=done,total=total)
                    agent=self.service.agent_factory(Path(tmp))
                    try:
                        if not agent.account()['connected']:raise ValueError('작성요령을 찾을 AI 계정을 먼저 연결해 주세요.')
                        progress('한글 양식 사본 읽는 중',0,1)
                        copied=Path(tmp)/'template.hwp';shutil.copy2(source,copied)
                        xml=Path(tmp)/'source.hwpml';extract_hwp(copied,xml)
                        return export_ai_guides(xml,self.service.root/'guide_exports'/uuid4().hex,
                                                source.stem,agent,self.operation_stops[op],progress)
                    finally:agent.close()
            return self._operation(register)
        if action == 'authoring_analysis_resolve':
            with self.lock,self.service.lock:
                self._require_idle_operation()
                if any(w.is_alive() for w in self.service.workers.values()):raise ValueError('문서 작성 중에는 양식 분석을 변경할 수 없습니다.')
                current=self.service.registry.load(command.get('template_id'))
                if current.get('registration_mode')=='guides_then_research_and_write':
                    from .template_guide_registration import resolve_guided_reviews
                    return resolve_guided_reviews(self.service.registry,current['id'],command.get('choices'))
                from .template_analysis import resolve_reviews
                return resolve_reviews(self.service.registry,current['id'],command.get('choices'))
        if action == 'authoring_create':
            with self.lock:
                self._require_idle_operation()
                state = self.service.create(command.get('template_id'), command.get('brief'),
                           reviewed=command.get('reviewed') is True,
                           review_mode=command.get('review_mode'),
                           research_enabled=command.get('research_enabled', True) is True,
                           external_consent=command.get('external_consent') is True,
                           local_values=command.get('local_values'),input_snapshot=command.get('input_snapshot'))
                return self.service.start(state['id'])
        if action == 'authoring_prepare_replay':
            from .saved_authoring_responses import prepare_bundle
            return self._operation(lambda op:prepare_bundle(self.service,command.get('template_id'),command.get('path'))[1])
        if action == 'authoring_create_replay':
            from .saved_authoring_responses import create_replay
            with self.lock,self.service.lock:
                self._require_idle_operation()
                state=create_replay(self.service,command.get('template_id'),command.get('path'),
                                    command.get('sha256'),command.get('local_values'),command.get('input_snapshot'))
                return self.service.start(state['id'])
        if action == 'authoring_status':
            return self.service.status(command['job_id'])
        if action == 'authoring_open_output':
            job_id = command.get('job_id')
            folder = self.service.job_path(job_id).resolve()
            state = read_json(folder / 'state.json')
            if state.get('status') != 'completed' or not state.get('hwp_path'):
                raise ValueError('작성과 저장이 완료된 한글 파일만 열 수 있습니다.')
            path = Path(state['hwp_path']).resolve(strict=True)
            if not path.is_relative_to(folder):
                raise ValueError('작업 폴더 밖의 파일은 출력본으로 열 수 없습니다.')
            return self._operation(lambda op: open_output_hwp(path))
        if action == 'authoring_resume':
            with self.lock:
                self._require_idle_operation()
                return self.service.start(command['job_id'])
        if action == 'authoring_stop':
            return self.service.stop(command['job_id'])
        raise ValueError('알 수 없는 문서 작성 요청입니다.')

    def _require_idle_operation(self):
        if any(o['status'] == 'running' for o in self.operations.values()):
            raise ValueError('계정 연결 또는 양식 처리가 끝난 뒤 작성을 시작하세요.')

    def close(self):
        self.closed.set()
        for event in self.operation_stops.values():event.set()
        self.service.close()
