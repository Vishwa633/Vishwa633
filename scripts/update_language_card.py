from pathlib import Path
from urllib.request import urlopen
from html import escape
from datetime import datetime
from zoneinfo import ZoneInfo
import xml.etree.ElementTree as E
import re
root=Path(__file__).resolve().parents[1]
url="https://github-readme-stats-git-master-rickstaa.vercel.app/api/top-langs/?username=vishwa633&layout=compact&langs_count=8"
tree=E.fromstring(urlopen(url,timeout=30).read())
items=[]
for el in tree.iter():
    if el.tag.endswith("}text"):
        m=re.fullmatch(r"(.+?)\s+(\d+\.\d+)%", "".join(el.itertext()).strip())
        if m: items.append((m[1],float(m[2])))
if len(items)<3: raise RuntimeError("No usable language statistics returned")
date=datetime.now(ZoneInfo("Asia/Colombo")).strftime("%d %b %Y")
for mode in ("day","night"):
    bg,edge,accent,muted,bar=("#09241d","#346452","#a6e9ba","#b9d2c1","#79ba96") if mode=="day" else ("#090f19","#263b50","#72dcd5","#a5bbd0","#77abc4")
    height=140+len(items)*39
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" viewBox="0 0 1000 {height}"><title>Repository languages</title><rect x="1" y="1" width="998" height="{height-2}" rx="18" fill="{bg}" stroke="{edge}" stroke-width="2"/><g font-family="Arial,sans-serif"><text x="38" y="49" fill="#edf5ff" font-size="30" font-weight="700">Repository languages</text><text x="39" y="78" fill="{muted}" font-size="15">Public repository code · updated {date}</text>'
    for i,(name,pct) in enumerate(items):
        y=108+i*39
        svg+=f'<text x="39" y="{y+15}" fill="{muted}" font-size="17">{escape(name)}</text><rect x="263" y="{y}" width="580" height="17" rx="8" fill="{edge}"/><rect x="263" y="{y}" width="{max(2,580*pct/100):.2f}" height="17" rx="8" fill="{bar}"/><text x="948" y="{y+15}" text-anchor="end" fill="{accent}" font-size="16">{pct:.2f}%</text>'
    svg+='</g></svg>'
    E.fromstring(svg)
    (root/f"assets/themes/{mode}/languages-bars-v1.svg").write_text(svg,encoding="utf-8")
