"""Re-render cached test responses; no AI calls and no overwrite of job outputs."""
import argparse
import json
from pathlib import Path
import sys
from uuid import uuid4
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src'))
from govoffice.services.document_authoring import read_json, write_json, render_draft
from govoffice.adapters.hwp_form_export import export_generated_hwp

p=argparse.ArgumentParser()
p.add_argument('job',type=Path)
p.add_argument('--inline',action='store_true')
args=p.parse_args()
job=args.job.resolve()
m=read_json(job/'template/manifest.json')
results={t['id']:read_json(job/'responses'/f"{t['id']}.json") for t in m['topics']}
xml,fields=render_draft(job/'template',m,results)
if args.inline:
    root=ET.fromstring(xml)
    for table in root.iter('TABLE'):
        pos=table.find('SHAPEOBJECT/POSITION')
        if pos is not None:
            pos.set('TreatAsChar','true')
    xml='<?xml version="1.0" encoding="UTF-8"?>'+ET.tostring(root,encoding='unicode')
folder=job/('qa_'+uuid4().hex[:8])
folder.mkdir()
(folder/'작성중.hml').write_text(xml,encoding='utf-8')
write_json(folder/'입력필드.json',fields)
target=folder/'가상과제_검토초안.hwp'
result=export_generated_hwp(job/'template/template.hwp',folder/'작성중.hml',target)
print(json.dumps({'hwp':str(target),'native':result},ensure_ascii=False))
