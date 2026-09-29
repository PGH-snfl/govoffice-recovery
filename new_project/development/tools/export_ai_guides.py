"""Export source-bound guides using the program's configured AI connection."""
import argparse
import json
from pathlib import Path
import sys
import tempfile
import threading

PROJECT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(PROJECT/'src'))
from govoffice.adapters.codex_author import CodexAuthor
from govoffice.services.ai_guide_export import export_ai_guides


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('source');parser.add_argument('destination');parser.add_argument('--name',required=True)
    args=parser.parse_args()
    if Path(args.destination).exists():raise FileExistsError(args.destination)
    with tempfile.TemporaryDirectory(prefix='govoffice_ai_guide_') as cwd:
        agent=CodexAuthor(cwd)
        try:
            if not agent.account()['connected']:raise RuntimeError('AI 계정 연결이 필요합니다.')
            result=export_ai_guides(args.source,args.destination,args.name,agent,threading.Event(),
                lambda phase,done,total:print(json.dumps({'phase':phase,'done':done,'total':total},ensure_ascii=False),flush=True))
            print(json.dumps({k:v for k,v in result.items() if k!='outline'},ensure_ascii=False),flush=True)
        finally:agent.close()


if __name__=='__main__':
    main()
