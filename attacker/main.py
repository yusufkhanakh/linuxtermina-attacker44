import os
import requests
import socket
from urllib.parse import urlparse
from datetime import datetime

def banner():
    print("=" * 65)
    print("   YUSUFXONPRO - ELITE CYBER SECURITY & PENTEST TOOL")
    print("   Local Device File & Report Generator")
    print("=" * 65)

def save_report_to_laptop(domain, report_data):
    # Noutbukingizda 'reports' nomli papka yaratish
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
        print(f"[+] Kompyuteringizda yangi papka ochildi: /{reports_dir}/")

    # Fayl nomini va vaqtini belgilash
    safe_domain = domain.replace('.', '_')
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = os.path.join(reports_dir, f"audit_{safe_domain}_{timestamp}.txt")

    # Faylga yozish
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report_data)
    
    print(f"[SUCCESS] Hisobot noutbukingizga saqlandi: {os.path.abspath(filename)}")

def check_target(target_url):
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        target_url = "https://" + target_url

    parsed_url = urlparse(target_url)
    domain = parsed_url.netloc or parsed_url.path
    
    report_lines = []
    report_lines.append(f"=== YUSUFXONPRO SECURITY AUDIT REPORT ===")
    report_lines.append(f"Target: {target_url}")
    report_lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    print(f"\n[+] Skanerlanmoqda: {target_url}")
    print(f"[+] Domen: {domain}")
    print("-" * 65)

    # 1. HTTP Sarlavhalari
    try:
        response = requests.get(target_url, timeout=7, allow_redirects=True)
        status_msg = f"[OK] Serverga ulanish muvaffaqiyatli! Status kodi: {response.status_code}"
        print(status_msg)
        report_lines.append(status_msg)
        
        report_lines.append("\n--- SECURITY HEADERS ---")
        headers = response.headers
        security_headers = {
            'X-Frame-Options': 'Clickjacking himoyasi',
            'X-XSS-Protection': 'XSS himoyasi',
            'Content-Security-Policy': 'CSP siyosati',
            'Strict-Transport-Security': 'HSTS (HTTPS majburlash)'
        }

        for header, desc in security_headers.items():
            if header in headers:
                res_str = f" [PASSED] {header}: Topildi ({desc})"
            else:
                res_str = f" [VULNERABILITY] {header} TOPILMADI! ({desc} zaif)"
            print(res_str)
            report_lines.append(res_str)

    except requests.exceptions.RequestException as e:
        err_msg = f"[-] Xatolik: Saytga ulanib bo'lmadi. Sabab: {e}"
        print(err_msg)
        return

    # 2. Portlarni tekshirish
    print("\n--- TCP PORT SCAN ---")
    report_lines.append("\n--- TCP PORT SCAN ---")
    ports_to_check = [80, 443, 21, 22, 3306]
    
    for port in ports_to_check:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        try:
            result = s.connect_ex((domain, port))
            if result == 0:
                p_str = f" [OPEN PORT] Port {port}: Ochiq"
            else:
                p_str = f" [CLOSED] Port {port}: Yopiq"
            print(p_str)
            report_lines.append(p_str)
        except Exception:
            pass
        finally:
            s.close()

    # To'liq ma'lumotni noutbukdagi faylga saqlash
    full_report_text = "\n".join(report_lines)
    save_report_to_laptop(domain, full_report_text)

    print("\n" + "=" * 65)
    print("[+] Audit yakunlandi va fayl noutbukingizga yozildi.")
    print("=" * 65)

if __name__ == "__main__":
    banner()
    target = input("Tekshiriladigan sayt domenini kiriting (masalan: kun.uz): ").strip()
    if target:
        check_target(target)
    else:
        print("[-] Xato: Domen kiritilmadi!")
