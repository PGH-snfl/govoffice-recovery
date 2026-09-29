"""Audit files selected by Git, without printing possible secret values."""
from pathlib import Path
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
TEXT = {'.py', '.ps1', '.cmd', '.json', '.md', '.txt', '.toml', '.yml', '.yaml', '.ini', '.cfg'}
SECRETS = {
    'private_key': re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'github_token': re.compile(rb'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{60,})\b'),
    'openai_token': re.compile(rb'\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{45,}\b'),
}


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    paths = subprocess.check_output(['git', '-c', f'safe.directory={ROOT.as_posix()}', '-c', 'core.quotepath=false', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'], cwd=ROOT).decode('utf-8').split('\0')
    files = sorted({p for p in paths if p and (ROOT/p).is_file()})
    large, sensitive, findings, unreadable = [], [], [], []
    total = 0
    for relative in files:
        path = ROOT/relative
        size = path.stat().st_size
        total += size
        if size >= 100*1024*1024:
            large.append({'path':relative, 'bytes':size})
        private = (relative.startswith(('tmp/', 'system_backups/', 'new_project/config/document_authoring/',
                    'new_project/config/generated_documents/', 'new_project/config/style_presets/'))
                   or relative in {'new_project/config/user_profile.json','new_project/config/user_profile.dat','new_project/config/favorites.json'}
                   or relative.startswith('new_project/ai_response_library/') and path.suffix=='.json'
                   or relative.startswith('materials/validation/') and path.name!='README.md'
                   or path.name in {'.env','auth.json','credentials.json'})
        if private:
            sensitive.append(relative)
        if path.suffix.lower() in TEXT and size <= 20*1024*1024:
            try:
                data = path.read_bytes()
            except OSError as error:
                unreadable.append({'path':relative, 'error':type(error).__name__})
                continue
            for name, pattern in SECRETS.items():
                if pattern.search(data):
                    findings.append({'path':relative, 'kind':name})
    result = {'files':len(files),'bytes':total,'files_over_100_mib':large,
              'private_paths_selected':sensitive,'credential_pattern_candidates':findings,
              'unreadable_files':unreadable,
              'scope':'path/token-pattern check, not an exhaustive personal-data or history audit'}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return int(bool(large or sensitive or findings or unreadable))


if __name__=='__main__':
    raise SystemExit(main())
