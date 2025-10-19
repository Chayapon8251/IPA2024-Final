from netmiko import ConnectHandler
from pprint import pprint

# ไม่ต้อง hardcode IP ที่นี่ เราจะรับมาจากไฟล์หลัก
# device_ip = "<!!!REPLACEME with router IP address!!!>" 
username = "admin"
password = "cisco"

def gigabit_status(router_ip):
    
    device_params = {
        "device_type": "cisco_xe", # <--- 1. Device Type ที่ถูกต้องสำหรับ IOS XE
        "ip": router_ip,           # <--- 2. ใช้ IP ที่รับเข้ามา
        "username": username,
        "password": password,
        "conn_timeout": 15
    }
    
    ans = ""
    with ConnectHandler(**device_params) as ssh:
        up = 0
        down = 0
        admin_down = 0
        
        # <--- 3. คำสั่งที่ถูกต้อง และเปิดใช้ TextFSM
        result = ssh.send_command("show interfaces", use_textfsm=True)
        
        # TextFSM จะคืนค่ามาเป็น List ของ Dictionaries
        for status in result:
            
            # <--- 4. กรองเอาเฉพาะ Interface ที่เราสนใจ
            if 'GigabitEthernet' in status['interface']:
                
                interface_name = status['interface']
                link_status = status['link_status']
                protocol_status = status['protocol_status'] # สถานะ line protocol
                
                status_str = "" # ตัวแปรเก็บสถานะ "up", "down", ...
                
                # <--- 5. Logic การนับสถานะ
                if link_status == "up" and protocol_status == "up":
                    status_str = "up"
                    up += 1
                elif link_status == "administratively down":
                    status_str = "administratively down"
                    admin_down += 1
                else: 
                    # กรณีอื่นๆ (เช่น up/down, down/down) ตีเป็น down
                    status_str = "down"
                    down += 1
                
                # <--- 6. สร้าง String ส่วนแรก
                ans += f"{interface_name} {status_str}, "

        # <--- 7. สรุปผลรวมต่อท้าย
        ans = ans.strip(', ') # ลบ , ตัวสุดท้ายออก
        ans += f" -> {up} up, {down} down, {admin_down} administratively down"
        
        pprint(ans) # Print ให้เห็นใน terminal
        return ans