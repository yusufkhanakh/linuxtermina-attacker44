import requests
import socket
from urllib.parse import urlparse

def banner():
    print("=" * 65)
    print("   YUSUFXONPRO - REAL CYBER SECURITY AUDIT & PENTEST TOOL")
    print("   Etika va xavfsizlik auditi uchun rasmiy skaner")
    print("=" * 65)

def check_target(target_url):
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        target_url = "https://" + target_url

    parsed_url = urlparse(target_url)
    domain = parsed_url.netloc or parsed_url.path
    
    print(f"\n[+] Skanerlanmoqda: {target_url}")
    print(f"[+] Domen: {domain}")
    print("-" * 65)

    # 1. HTTP Sarlavhalari va Xavfsizlik darajasini tekshirish
    try:
        response = requests.get(target_url, timeout=7, allow_redirects=True)
        print(f"[OK] Serverga ulanish muvaffaqiyatli! Status kodi: {response.status_code}")
        
        print("\n--- XAVFSIZLIK SARLAVHALARI (SECURITY HEADERS) TAHLILI ---")
        headers = response.headers
        
        security_headers = {
            'X-Frame-Options': 'Clickjacking hujumidan himoya',
            'X-XSS-Protection': 'Cross-Site Scripting (XSS) himoyasi',
            'Content-Security-Policy': 'CSP - Kontent xavfsizligi siyosati',
            'Strict-Transport-Security': 'HSTS - Majburiy HTTPS ulanishi',
            'X-Content-Type-Options': 'MIME-sniffing himoyasi'
        }

        for header, description in security_headers.items():
            if header in headers:
                print(f" [PASSED] {header}: Topildi ({description})")
            else:
                print(f" [VULNERABILITY] {header} TOPILMADI! ({description} zaif)")

    except requests.exceptions.RequestException as e:
        print(f"[-] Xatolik: Saytga ulanib bo'lmadi. Sabab: {e}")
        return

    # 2. Ochiq portlarni socket orqali tekshirish
    print("\n--- TARMOQ PORTLARINI TEKSHIRISH (TCP PORT SCAN) ---")
    ports_to_check = [80, 443, 21, 22, 3306, 8080]
    
    for port in ports_to_check:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        try:
            result = s.connect_ex((domain, port))
            if result == 0:
                print(f" [OPEN PORT] Port {port}: Ochiq (Xizmat faol)")
            else:
                print(f" [CLOSED] Port {port}: Yopiq yoki himoyalangan")
        except Exception:
            print(f" [ERROR] Port {port} tekshirib bo'lmadi.")
        finally:
            s.close()

    print("\n" + "=" * 65)
    print("[+] Audit yakunlandi. Natijalar tahlil qilindi.")
    print("=" * 65)

if __name__ == "__main__":
    banner()
    target = input("Tekshiriladigan sayt domenini kiriting (masalan: example.com): ").strip()
    if target:
        check_target(target)
    else:
        print("[-] Xato: Domen kiritilmadi!")
