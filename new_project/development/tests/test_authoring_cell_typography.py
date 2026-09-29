import tempfile
import unittest
from pathlib import Path
import xml.etree.ElementTree as ET

from govoffice.services.authoring_typography import review_spans,review_paragraphs
from govoffice.services.document_authoring import render_draft,own_text
from govoffice.services.authoring_validation import audit_layout


HEAD='''<HEAD><MAPPINGTABLE><CHARSHAPELIST Count="1">
<CHARSHAPE Id="0" Height="1100" TextColor="16711680"><FONTID Hangul="2"/>
<CHARSPACING Hangul="-3"/></CHARSHAPE></CHARSHAPELIST>
<PARASHAPELIST Count="1"><PARASHAPE Id="0" Align="Center" LineWrap="Squeeze" KeepLines="true">
<PARAMARGIN Left="800" Right="800" Indent="1000" LineSpacingType="Fixed" LineSpacing="500"/>
</PARASHAPE></PARASHAPELIST></MAPPINGTABLE></HEAD>'''

def p(value):return '<P ParaShape="0" Style="0"><TEXT CharShape="0"><CHAR>'+value+'</CHAR></TEXT></P>'
def cell(value):return '<CELL Width="10000" Height="800" ColSpan="1" RowSpan="1" BorderFill="1"><PARALIST LineWrap="Squeeze" VertAlign="Center">'+p(value)+'</PARALIST></CELL>'
def table():return ('<TABLE PageBreak="None" ColCount="2"><SHAPEOBJECT><SIZE Width="20000" Height="800" Protect="true"/>'
                   '<POSITION TreatAsChar="true" FlowWithText="false" AllowOverlap="true"/></SHAPEOBJECT>'
                   '<INSIDEMARGIN Left="200" Right="200" Top="100" Bottom="100"/><ROW>'+cell('____')+cell('____')+'</ROW></TABLE>')

class CellTypographyTests(unittest.TestCase):
    def test_adjacent_body_fields_can_share_original_font_style(self):
        source='<HWPML><HEAD><CHARSHAPELIST Count="2"><CHARSHAPE Id="0" Height="1200" TextColor="0"><FONTID Hangul="7"/></CHARSHAPE><CHARSHAPE Id="1" Height="1300" TextColor="0"><FONTID Hangul="3"/><BOLD/></CHARSHAPE></CHARSHAPELIST></HEAD><BODY><SECTION><P ParaShape="0" Style="0"><TEXT CharShape="0"><CHAR/></TEXT></P><P ParaShape="0" Style="0"><TEXT CharShape="1"><CHAR/></TEXT></P></SECTION></BODY></HWPML>'
        manifest={'paragraph_count':2,'topics':[{'id':'s','start':0,'fields':[
            {'id':'P0000','index':0,'original':'','role':'body','max_chars':200,'multiline':True},
            {'id':'P0001','index':1,'original':'','role':'body','max_chars':200,'multiline':True,'style_from_index':0}]}],
            'render_policy':{'readable_body':True,'blue_review':True,'preserve_layout':True}}
        with tempfile.TemporaryDirectory() as temp:
            (Path(temp)/'source.hwpml').write_text(source,encoding='utf-8')
            xml,log=render_draft(Path(temp),manifest,{'s':{'topic_id':'s','values':{'P0000':'국내 본문','P0001':'국외 본문\n다음 문단'},'needs_review':[]}})
        root=ET.fromstring(xml);ps=list(root.iter('P'));shapes={s.get('Id'):s for s in root.iter('CHARSHAPE')}
        def font(index):
            shape=shapes[ps[index].find('TEXT').get('CharShape')]
            return shape.get('Height'),shape.find('FONTID').get('Hangul'),shape.find('BOLD') is not None
        self.assertEqual(font(log[0]['output_index']),font(log[1]['output_indices'][0]))
        self.assertEqual(font(log[0]['output_index']),font(log[1]['output_indices'][1]))
        self.assertEqual(("1200","7",False),font(log[1]['output_indices'][0]))

    def render(self,values,notes=(),in_table=False):
        source='<HWPML>'+HEAD+'<BODY><SECTION>'+p('1. 제목')
        source+=(('<P><TEXT CharShape="0">'+table()+'</TEXT></P>') if in_table else p('____')+p('____'))
        source+=p('그대로 보존')+'</SECTION></BODY></HWPML>'
        root=ET.fromstring(source);ps=list(root.iter('P'))
        fields=[{'id':f'P{i:04d}','index':i,'original':'____','label':'금액' if n else '실행 계획',
                 'role':'body','max_chars':5000,'multiline':True}
                for n,i in enumerate(i for i,x in enumerate(ps) if own_text(x)=='____')]
        ids=[f['id'] for f in fields]
        manifest={'paragraph_count':len(ps),'topics':[{'id':'s','start':0,'fields':fields}],
                  'render_policy':{'readable_body':True,'blue_review':True,'preserve_layout':True}}
        notes=[note.replace('FIELD',ids[0]) for note in notes]
        with tempfile.TemporaryDirectory() as temp:
            (Path(temp)/'source.hwpml').write_text(source,encoding='utf-8')
            xml,log=render_draft(Path(temp),manifest,{'s':{'topic_id':'s','values':dict(zip(ids,values)),'needs_review':notes}})
        self.assertEqual([],audit_layout(xml,log)['issues'])
        return ET.fromstring(xml),log

    def colors(self,root,index):
        shapes={s.get('Id'):s for s in root.iter('CHARSHAPE')}
        return [(''.join(c.itertext()),shapes[t.get('CharShape')].get('TextColor'))
                for t in list(root.iter('P'))[index].findall('TEXT') for c in t.findall('CHAR')]

    def test_uncertain_sentence_is_parenthesized_below_black_body(self):
        root,log=self.render(['확정 내용입니다. 예산은 확인 필요합니다. 다음은 확정 내용입니다.\n\n일반 문단입니다.','정상 값'])
        indices=log[0]['output_indices']
        self.assertEqual(3,len(indices))
        self.assertEqual([('확정 내용입니다. 다음은 확정 내용입니다.','0')],self.colors(root,indices[0]))
        self.assertEqual([('(예산은 확인 필요합니다.)','16711680')],self.colors(root,indices[1]))
        self.assertEqual([('일반 문단입니다.','0')],self.colors(root,indices[2]))

    def test_brackets_only_and_normal_terms_black(self):
        value='가정용 장비 예시와 추정 방법을 설명합니다. 예산 [확인 필요: 금액] 외에는 확정입니다.'
        spans=review_spans(value)
        self.assertEqual(['[확인 필요: 금액]'],[value[a:b] for a,b in spans])
        self.assertEqual([],review_spans('가정용 장비를 검토합니다. 결과는? 확인 필요 없음.'))
        self.assertEqual([(0,1)],review_spans('?'))

    def test_generic_review_does_not_color_all_fields(self):
        root,log=self.render(['정상 내용','확정 값'],['전반적인 검토 권장','FIELD 사전 검토 완료'])
        self.assertEqual([('정상 내용','0')],self.colors(root,log[0]['output_index']))
        self.assertEqual([('확정 값','0')],self.colors(root,log[1]['output_index']))

    def test_field_specific_note_is_below_unchanged_body_only_in_that_field(self):
        root,log=self.render(['목표 90%를 달성합니다.','목표 90%'],['FIELD: "목표 90%"는 사용자 확인 필요'])
        self.assertEqual([('목표 90%를 달성합니다.','0')],self.colors(root,log[0]['output_index']))
        self.assertEqual([('("목표 90%"는 사용자 확인 필요)','16711680')],self.colors(root,log[0]['output_indices'][1]))
        self.assertEqual([('목표 90%','0')],self.colors(root,log[1]['output_index']))

    def test_inline_and_standalone_notes_are_below_and_not_duplicated(self):
        self.assertEqual([('목표를 검증합니다.',False),('(확인 필요: 목표 수치)',True)],
                         review_paragraphs(['목표를 검증합니다. [확인 필요: 목표 수치]'],['P0001: 확인 필요: 목표 수치']))
        self.assertEqual([('목표를 검증합니다.',False),('(확인 필요: 목표 수치)',True)],
                         review_paragraphs(['목표를 검증합니다.','(확인 필요: 목표 수치)']))
        self.assertEqual([('(확인 필요: 일정 미확정)',True)],review_paragraphs(['?']))

    def test_review_reason_without_marker_is_not_lost(self):
        self.assertEqual([('예산 100원',False),('(확인 필요: 금액 근거가 없습니다.)',True)],
                         review_paragraphs(['예산 100원'],['P0001: 금액 근거가 없습니다.']))

    def test_mid_sentence_placeholder_does_not_leave_broken_black_sentence(self):
        self.assertEqual([('검증을 진행합니다.',False),('(예산은 [확인 필요: 금액]입니다.)',True)],
                         review_paragraphs(['검증을 진행합니다. 예산은 [확인 필요: 금액]입니다.']))
        self.assertEqual([('주소  상세',False)],review_paragraphs(['주소  상세']))

    def test_table_review_remains_in_same_cell_with_wrapping(self):
        root,log=self.render(['자료 검증을 진행합니다.\n(확인 필요: 참여기관 협의)','1,200,000'],in_table=True)
        cells=next(root.iter('TABLE')).findall('ROW/CELL')
        self.assertEqual(['자료 검증을 진행합니다.','(확인 필요: 참여기관 협의)'],
                         [own_text(p) for p in cells[0].findall('PARALIST/P')])
        self.assertEqual([('(확인 필요: 참여기관 협의)','16711680')],self.colors(root,log[0]['output_indices'][1]))
        self.assertEqual('Break',cells[0].find('PARALIST').get('LineWrap'))

    def test_long_table_wraps_without_shrinking_font_and_numbers_align_right(self):
        root,log=self.render(['긴 내용을 여러 줄로 나눠서 읽을 수 있도록 내용을 충분히 작성합니다.\n\n두 번째 문단입니다.','1,200,000'],in_table=True)
        t=next(root.iter('TABLE'));cells=t.findall('ROW/CELL')
        self.assertEqual('Cell',t.get('PageBreak'))
        self.assertEqual('false',t.find('SHAPEOBJECT/POSITION').get('TreatAsChar'))
        self.assertEqual('false',t.find('SHAPEOBJECT/SIZE').get('Protect'))
        self.assertEqual('TopAndBottom',t.find('SHAPEOBJECT').get('TextWrap'))
        self.assertEqual(['Top','Center'],[c.find('PARALIST').get('VertAlign') for c in cells])
        self.assertTrue(all(c.find('PARALIST').get('LineWrap')=='Break' for c in cells))
        self.assertTrue(all(c.get('HasMargin')=='true' and int(c.find('CELLMARGIN').get('Left'))>=200 for c in cells))
        self.assertEqual(20000,sum(int(c.get('Width')) for c in cells))
        self.assertTrue(all(c.get('ColSpan')=='1' and c.get('BorderFill')=='1' for c in cells))
        paras={s.get('Id'):s for s in root.iter('PARASHAPE')}
        chars={s.get('Id'):s for s in root.iter('CHARSHAPE')}
        for n,c in enumerate(cells):
            for par in c.findall('PARALIST/P'):
                style=paras[par.get('ParaShape')]
                self.assertEqual('Left' if n==0 else 'Right',style.get('Align'))
                self.assertEqual('KeepWord',style.get('BreakLatinWord'))
                self.assertEqual('false',style.get('BreakNonLatinWord'))
                self.assertEqual('0',style.find('PARAMARGIN').get('Indent'))
                self.assertEqual('Percent',style.find('PARAMARGIN').get('LineSpacingType'))
                self.assertEqual('1100',chars[par.find('TEXT').get('CharShape')].get('Height'))
                self.assertTrue(-5<=int(chars[par.find('TEXT').get('CharShape')].find('CHARSPACING').get('Hangul'))<=0)
        self.assertEqual('Squeeze',paras['0'].get('LineWrap'))  # Shared source styles unchanged.
        fixed=next(x for x in root.iter('P') if own_text(x)=='그대로 보존')
        self.assertEqual('0',fixed.get('ParaShape'))
        self.assertEqual([('그대로 보존','16711680')],self.colors(root,list(root.iter('P')).index(fixed)))

    def test_table_body_paragraph_spacing_review_gap_and_hanging_lists(self):
        values=['첫 문단입니다.\n둘째 문단입니다.\n(확인 필요: 협의)\n- 항목 내용은 이어지는 줄도 글자 시작 위치에 맞춥니다.','1,200,000']
        root,log=self.render(values,in_table=True)
        shapes={s.get('Id'):s for s in root.iter('PARASHAPE')}
        ps=next(root.iter('CELL')).findall('PARALIST/P')
        margins=[shapes[p.get('ParaShape')].find('PARAMARGIN') for p in ps]
        self.assertEqual('0',margins[0].get('Prev'))
        self.assertGreater(int(margins[1].get('Prev')),0)
        self.assertGreater(int(margins[2].get('Prev')),0)
        self.assertLess(int(margins[2].get('Prev')),int(margins[1].get('Prev')))
        self.assertEqual('0',margins[3].get('Left'))
        self.assertEqual(-2640,int(margins[3].get('Indent')))  # 1100pt-units * 1.2 glyphs * 2 URC.
        self.assertTrue(all(shapes[p.get('ParaShape')].get('Align')=='Left' for p in ps))
        self.assertTrue(all(m.get('Next')=='0' for m in margins))
        self.assertEqual(values[0].split('\n'),log[0]['paragraph_values'])

    def test_short_prose_uses_left_alignment_not_source_center(self):
        root,log=self.render(['목표 검증','1,200,000'],in_table=True)
        shapes={s.get('Id'):s for s in root.iter('PARASHAPE')}
        cells=list(root.iter('CELL'))
        self.assertEqual('Left',shapes[cells[0].find('PARALIST/P').get('ParaShape')].get('Align'))
        self.assertEqual('Right',shapes[cells[1].find('PARALIST/P').get('ParaShape')].get('Align'))

if __name__=='__main__':unittest.main()
