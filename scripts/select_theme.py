from pathlib import Path
import re
import sys
from datetime import datetime
from zoneinfo import ZoneInfo
root=Path(__file__).resolve().parents[1]
mode=sys.argv[1] if len(sys.argv)>1 else ("day" if 6<=datetime.now(ZoneInfo("Asia/Colombo")).hour<18 else "night")
if mode not in {"day","night"}:
    raise SystemExit("Expected day or night")
readme=root/"README.md"
content=readme.read_text(encoding="utf-8-sig")
content=re.sub(r"assets/themes/(?:day|night)/",f"assets/themes/{mode}/",content)
readme.write_text(content,encoding="utf-8")
