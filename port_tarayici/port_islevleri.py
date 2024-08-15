import socket
import queue
import threading
import re

port_servisleri = {
    20: "FTP Data",
    21: "FTP Control",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    443: "HTTPS",
    3306: "MySQL",
    5432: "PostgreSQL",
    6379: "Redis",
    # Diğer portlar ve servisler buraya eklenebilir
}

def gecerli_ip_adresi(ip):
    pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    if not pattern.match(ip):
        return False

    octets = ip.split('.')
    for octet in octets:
        if not (0 <= int(octet) <= 255):
            return False

    return True

def calisici(ip, port_kuyrugu, acik_portlar):
    while not port_kuyrugu.empty():
        port = port_kuyrugu.get()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        try:
            sonuc = s.connect_ex((ip, port))
            if sonuc == 0:
                servis = port_servisleri.get(port, "Bilinmeyen Servis")
                acik_portlar.append((port, servis))
        except socket.error:
            pass
        finally:
            s.close()
            port_kuyrugu.task_done()

def port_tarama(ip, port_araligi):
    port_kuyrugu = queue.Queue()
    acik_portlar = []

    for port in port_araligi:
        port_kuyrugu.put(port)

    is_parcaciklari = []
    for _ in range(100):  # 100 iş parçacığı
        is_parcacigi = threading.Thread(target=calisici, args=(ip, port_kuyrugu, acik_portlar))
        is_parcacigi.start()
        is_parcaciklari.append(is_parcacigi)

    port_kuyrugu.join()

    for is_parcacigi in is_parcaciklari:
        is_parcacigi.join()

    return acik_portlar

def sonuclari_kaydet(dosya_adi, ip, acik_portlar):
    with open(dosya_adi, 'w') as f:
        f.write(f"Tarama sonuçları IP: {ip}\n")
        if acik_portlar:
            for port, servis in acik_portlar:
                f.write(f"Port {port}: {servis}\n")
        else:
            f.write("Açık port bulunamadı.\n")
