"""Run real MySQL checks and store credential-free academic evidence."""
from datetime import datetime
from pathlib import Path
import json
import subprocess
import sys
import urllib.request
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'evidence'
OUT.mkdir(exist_ok=True)
results = []

def run(name, arguments):
    completed = subprocess.run(arguments, cwd=ROOT, capture_output=True, text=True)
    output = completed.stdout + completed.stderr
    results.append({'name': name, 'command': ' '.join(arguments),
                    'exit_code': completed.returncode, 'output': output})
    print(f'{name}: exit {completed.returncode}')
    if completed.returncode:
        print(output[-9000:])
    return completed

base = ['docker', 'compose', 'exec', '-T', 'web', 'python', 'manage.py']
run('Django configuration', base + ['check'])
run('Committed migrations match models', base + ['makemigrations', '--check', '--dry-run'])
run('Applied migrations', base + ['showmigrations'])
run('Full Django test suite on MySQL', base + ['test', '--noinput'])
run('Database engine and persisted catalog', base + ['shell', '-c',
    'import json; from django.db import connection; from catalog.models import Edition,Category,Poll,Option; '
    'c=connection.cursor(); c.execute("SELECT VERSION()"); version=c.fetchone()[0]; '
    'print(json.dumps({"vendor":connection.vendor,"version":version,"editions":Edition.objects.count(),'
    '"categories":Category.objects.count(),"polls":Poll.objects.count(),"options":Option.objects.count()}))'])
for route in ['/', '/accounts/register/', '/accounts/login/', '/health/', '/static/css/site.css']:
    try:
        with urllib.request.urlopen('http://localhost:8000' + route, timeout=10) as response:
            status = response.status
        results.append({'name': 'HTTP ' + route, 'exit_code': 0 if status == 200 else 1, 'output': str(status)})
        print(f'HTTP {route}: {status}')
    except Exception as error:
        results.append({'name': 'HTTP ' + route, 'exit_code': 1, 'output': str(error)})
        print(f'HTTP {route}: failed')
config = subprocess.run(['docker','compose','config','--format','json'], cwd=ROOT,
                        capture_output=True, text=True, check=True)
services = json.loads(config.stdout)['services']
boundary_checks = {
    'database_port_unpublished': not services['db'].get('ports'),
    'web_loopback_only': all(p.get('host_ip') == '127.0.0.1' for p in services['web']['ports']),
    'root_password_absent_from_web': 'MYSQL_ROOT_PASSWORD' not in services['web']['environment'],
    'debug_disabled': services['web']['environment']['DJANGO_DEBUG'].lower() == 'false',
}
results.append({'name':'Container security boundaries','exit_code':0 if all(boundary_checks.values()) else 1,
                'output': json.dumps(boundary_checks)})
report = {'date':datetime.now(ZoneInfo('America/Bogota')).isoformat(), 'checks':results,
          'passed':all(r['exit_code'] == 0 for r in results)}
(OUT/'verification.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
(OUT/'verification.txt').write_text('\n\n'.join(
    r['name'] + '\n' + r.get('command','') + '\nExit: ' + str(r['exit_code']) + '\n' + r['output']
    for r in results))
print('Verification evidence:',OUT/'verification.json')
sys.exit(0 if report['passed'] else 1)
