"""Prove one-command restart retains the live, fictional catalog."""
from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
QUERY = ('import json; from catalog.models import Edition,Category,Poll,Option; '
         'print(json.dumps({"editions":Edition.objects.count(),"categories":Category.objects.count(),'
         '"polls":Poll.objects.count(),"options":Option.objects.count(),'
         '"evidence_category":list(Category.objects.filter(name="Evidencia de persistencia - ficticia").values_list("pk",flat=True))}))')

def snapshot():
    result = subprocess.run(['docker','compose','exec','-T','web','python','manage.py','shell','-c',QUERY],
                            cwd=ROOT,capture_output=True,text=True,check=True)
    return json.loads(result.stdout.strip().splitlines()[-1])

before = snapshot()
subprocess.run(['docker','compose','stop','web'],cwd=ROOT,check=True,capture_output=True)
started = subprocess.run(['./start.sh'],cwd=ROOT,capture_output=True,text=True)
if started.returncode:
    print(started.stderr[-3000:])
    raise SystemExit(started.returncode)
after = snapshot()
passed = before == after and bool(after['evidence_category'])
report = {'command':'./start.sh','after_explicit_web_stop':True,'before':before,
          'after':after,'passed':passed,'startup_output':started.stdout[-2000:]}
(ROOT/'evidence/restart.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
print('Restart persistence:', 'PASS' if passed else 'FAIL', after)
raise SystemExit(0 if passed else 1)
