from collections import deque
import queue
import threading
import time
import unittest
from unittest.mock import Mock, patch
from pathlib import Path
import tempfile

from govoffice.adapters.codex_author import CodexAuthor, find_codex


class CodexProtocolTests(unittest.TestCase):
    def test_desktop_install_discovery_when_path_missing(self):
        with tempfile.TemporaryDirectory() as temp:
            exe = Path(temp)/'OpenAI/Codex/bin/test/codex.exe'
            exe.parent.mkdir(parents=True)
            exe.write_bytes(b'test discovery only')
            with patch('shutil.which', return_value=None), patch.dict('os.environ', {'LOCALAPPDATA':temp}, clear=True):
                self.assertEqual(str(exe), find_codex())

    def connection(self):
        a = CodexAuthor.__new__(CodexAuthor)
        a.cwd = 'test'
        a.events = queue.Queue()
        a.pending = deque()
        a.counter = 0
        a.send = Mock()
        a._tool_config = Mock(return_value={'web_search':'disabled'})
        return a

    def test_rpc_keeps_notifications_before_response(self):
        a = self.connection()
        event = {'method':'account/login/completed','params':{'success':True}}
        a.events.put(event)
        a.events.put({'id':1,'result':{'ok':True}})
        self.assertEqual({'ok':True}, a.rpc('test', {}))
        self.assertEqual([event], list(a.pending))

    def test_api_key_is_not_silently_used_for_login_workflow(self):
        a = self.connection()
        a.rpc = Mock(return_value={'account':{'type':'apiKey'}})
        self.assertFalse(a.account()['connected'])
        a.rpc.return_value = {'account':{'type':'chatgpt','planType':'test'}}
        self.assertTrue(a.account()['connected'])

    def test_end_of_process_and_cancel_do_not_hang(self):
        a = self.connection()
        a.events.put({'_eof':True})
        with self.assertRaises(RuntimeError):
            a._next(time.monotonic()+1)
        event = threading.Event();event.set()
        with self.assertRaises(InterruptedError):
            a._next(time.monotonic()+1, event)

    def test_account_identity_is_metadata_only_and_logout_is_verified(self):
        a = self.connection()
        a.rpc = Mock(return_value={'account': {'type':'chatgpt', 'email':'test@example.invalid',
                                             'planType':'test', 'accessToken':'never expose'}})
        self.assertEqual('test@example.invalid', a.account()['email'])
        self.assertNotIn('accessToken', a.account())
        a.rpc = Mock(side_effect=[{}, {'account':None}])
        self.assertFalse(a.logout()['connected'])
        self.assertEqual(('account/logout', None), a.rpc.call_args_list[0].args)
        self.assertEqual('account/read', a.rpc.call_args_list[1].args[0])
        a.rpc = Mock(side_effect=[{}, {'account':{'type':'chatgpt'}}])
        with self.assertRaises(RuntimeError):
            a.logout()

    def test_command_approval_is_denied(self):
        a = self.connection()
        a.events.put({'id':99,'method':'item/commandExecution/requestApproval','params':{}})
        a.events.put({'id':1,'result':{}})
        a.rpc('test', {})
        a.send.assert_any_call({'id':99,'result':{'decision':'decline'}})

    def test_final_message_is_used_not_commentary_or_another_topic(self):
        a = self.connection()
        a.account = Mock(return_value={'connected':True})
        a.rpc = Mock(side_effect=[{'thread':{'id':'thread1'}},{'turn':{'id':'turn1'}}])
        a.events.put({'method':'item/completed','params':{'threadId':'other','item':{'type':'agentMessage','id':'wrong','text':'wrong'}}})
        a.events.put({'method':'item/completed','params':{'threadId':'thread1','turnId':'turn1','item':{'type':'agentMessage','id':'comment','phase':'commentary','text':'writing'}}})
        a.events.put({'method':'item/completed','params':{'threadId':'thread1','turnId':'turn1','item':{'type':'agentMessage','id':'final','phase':'final_answer','text':'{"ok":true}'}}})
        a.events.put({'method':'turn/completed','params':{'threadId':'thread1','turn':{'id':'turn1','status':'completed'}}})
        self.assertEqual({'ok':True}, a.generate('prompt', {}, threading.Event()))
        params = a.rpc.call_args_list[-1].args[1]
        self.assertEqual({'type':'readOnly','networkAccess':False}, params['sandboxPolicy'])
        self.assertEqual('never', params['approvalPolicy'])

    def test_research_enables_hosted_web_without_shell_apps_or_inherited_mcp(self):
        a=self.connection()
        a.rpc=Mock(return_value={'config':{'mcp_servers':{'private.server':{'command':'private-tool'}},'plugins':{'private@team':{}}}})
        config=CodexAuthor._tool_config(a,True,threading.Event())
        self.assertEqual('live',config['web_search'])
        self.assertFalse(config['features.shell_tool'])
        self.assertFalse(config['features.apps'])
        self.assertFalse(config['mcp_servers']['private.server']['enabled'])
        self.assertEqual({'enabled':False},config['mcp_servers']['private.server'])
        self.assertFalse(config['plugins']['private@team']['enabled'])
        self.assertEqual('disabled',CodexAuthor._tool_config(a,False,threading.Event())['web_search'])

    def research_connection(self, items):
        a=self.connection();a.account=Mock(return_value={'connected':True})
        a.rpc=Mock(side_effect=[{'thread':{'id':'t'}},{'turn':{'id':'r'}}])
        for item in items:
            a.events.put({'method':'item/started','params':{'threadId':'t','turnId':'r','item':item}})
            a.events.put({'method':'item/completed','params':{'threadId':'t','turnId':'r','item':item}})
        a.events.put({'method':'item/completed','params':{'threadId':'t','turnId':'r','item':{'type':'agentMessage','id':'final','text':'{"ok":true}'}}})
        a.events.put({'method':'turn/completed','params':{'threadId':'t','turn':{'id':'r','status':'completed'}}})
        return a

    def test_research_records_real_search_and_open_events(self):
        a=self.research_connection([{'type':'webSearch','id':'s','query':'public topic'},
                                   {'type':'webSearch','id':'o','action':{'type':'openPage','url':'https://example.org/study'}}])
        progress=Mock()
        self.assertEqual({'ok':True},a.research('prompt',{},threading.Event(),progress))
        self.assertEqual(2,len(a.last_research_trace));progress.assert_called()
        self.assertFalse(a.rpc.call_args_list[-1].args[1]['sandboxPolicy']['networkAccess'])

    def test_unexecuted_research_is_not_reported_as_completed(self):
        a=self.research_connection([])
        with self.assertRaisesRegex(ValueError,'웹 조사 실행 기록'):
            a.research('prompt',{},threading.Event())

    def test_writing_stays_tool_free_and_research_rejects_other_tools(self):
        a=self.research_connection([{'type':'webSearch','id':'s'}])
        with self.assertRaises(RuntimeError): a.generate('prompt',{},threading.Event())
        for kind in ['commandExecution','fileChange','mcpToolCall','dynamicToolCall','collabAgentToolCall','imageGeneration']:
            a=self.research_connection([{'type':kind,'id':'x'}])
            with self.subTest(kind=kind),self.assertRaises(RuntimeError):
                a.research('prompt',{},threading.Event())
            self.assertEqual('turn/interrupt',a.send.call_args.args[0]['method'])

    def test_research_has_a_finite_web_action_budget(self):
        a=self.research_connection([{'type':'webSearch','id':str(i)} for i in range(7)])
        with self.assertRaisesRegex(RuntimeError,'6회'):
            a.research('prompt',{},threading.Event())


if __name__ == '__main__':
    unittest.main()
