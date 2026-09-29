"""Collect public reference pages using the existing read-only source collector."""
import concurrent.futures
import json
from pathlib import Path
import runpy

BASE = Path(__file__).resolve().parent
previous = BASE.parent / 'msit-research-writing-2026-09-25' / 'collect_public.py'
module = runpy.run_path(str(previous), run_name='reference_collector')
fetch = module['fetch']
fetch.__globals__['BASE'] = BASE
data = json.loads((BASE / 'sources.json').read_text(encoding='utf-8'))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(fetch, data['cases']))
(BASE / 'retrieval_status.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
for result in results:
    print(json.dumps(result, ensure_ascii=False))
