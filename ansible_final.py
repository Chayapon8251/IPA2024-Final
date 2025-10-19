import subprocess
import sys
import os

ROUTER_MAP = {
    "10.0.15.61": "CSR1KV-Pod1-1",
    "10.0.15.62": "CSR1KV-Pod1-2",
    "10.0.15.63": "CSR1KV-Pod1-3",
    "10.0.15.64": "CSR1KV-Pod1-4",
    "10.0.15.65": "CSR1KV-Pod1-5",
}

def showrun(student_id, router_ip):
    
    router_name = ROUTER_MAP.get(router_ip)
    if not router_name:
        return "Error: Unknown Router IP"
        
    filename = f"show_run_{student_id}_{router_name}.txt"

    # --- 1. กลับมาใช้ Command แบบ List (นี่คือวิธีที่ถูกต้อง) ---
    command = [
        sys.executable,
        '-m',
        'ansible.cli.playbook',
        'playbook.yaml', 
        '--limit', router_ip,
        '-e', f'student_id={student_id}'
    ]
    
    # --- 2. สร้าง "สุดยอด" Environment บังคับ UTF-8 ---
    env = os.environ.copy() 
    env['PYTHONUTF8'] = '1' 
    env['LC_ALL'] = 'en_US.UTF-8'
    env['LANG'] = 'en_US.UTF-8'
    env['PYTHONIOENCODING'] = 'utf-8' # <--- เพิ่มตัวนี้เข้าไป

    # --- 3. รันโดยไม่ใช้ shell=True ---
    result = subprocess.run(
        command, 
        capture_output=True, 
        text=True,
        encoding='utf-8', 
        env=env  # <--- ส่ง Environment ที่เราแก้แล้วเข้าไป
    )
    
    # --- โค้ดที่เหลือเหมือนเดิม ---
    if 'ok=2' in result.stdout and 'failed=0' in result.stdout:
        return filename
    else:
        print("--- Ansible Error Output ---")
        print(result.stderr)
        print(result.stdout)
        print("----------------------------")
        return "Error: Ansible"