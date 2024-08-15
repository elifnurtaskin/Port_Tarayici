import tkinter as tk
from tkinter import scrolledtext, messagebox
from port_islevleri import gecerli_ip_adresi, port_tarama, sonuclari_kaydet
from raporlama import analiz_ve_raporlama

def tarama_yap():
    ip = ip_entry.get()
    baslangic_portu = start_port_entry.get()
    bitis_portu = end_port_entry.get()
    dosya_adi = filename_entry.get()

    if not gecerli_ip_adresi(ip):
        messagebox.showerror("Hata", "Geçersiz IP adresi. Lütfen geçerli bir IP adresi girin.")
        return

    try:
        baslangic_portu = int(baslangic_portu)
        bitis_portu = int(bitis_portu)
    except ValueError:
        messagebox.showerror("Hata", "Port aralıkları sayısal değerler olmalıdır.")
        return

    if baslangic_portu > bitis_portu:
        messagebox.showerror("Hata", "Başlangıç portu bitiş portundan büyük olamaz.")
        return

    port_araligi = range(baslangic_portu, bitis_portu + 1)
    acik_portlar = port_tarama(ip, port_araligi)

    sonuc_text.delete(1.0, tk.END)
    if acik_portlar:
        for port, servis in acik_portlar:
            sonuc_text.insert(tk.END, f"Port {port}: {servis}\n")
    else:
        sonuc_text.insert(tk.END, "Açık port bulunamadı.\n")

    try:
        sonuclari_kaydet(dosya_adi, ip, acik_portlar)
        messagebox.showinfo("Bilgi", f"Sonuçlar {dosya_adi} dosyasına kaydedildi.")
    except Exception as e:
        messagebox.showerror("Hata", f"Sonuçları kaydederken bir hata oluştu: {e}")

    analiz_ve_raporlama(acik_portlar)

# GUI oluşturma
pencere = tk.Tk()
pencere.title("Port Tarayıcı")

tk.Label(pencere, text="IP Adresi:").grid(row=0, column=0, padx=10, pady=5)
ip_entry = tk.Entry(pencere, width=20)
ip_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(pencere, text="Başlangıç Portu:").grid(row=1, column=0, padx=10, pady=5)
start_port_entry = tk.Entry(pencere, width=20)
start_port_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(pencere, text="Bitiş Portu:").grid(row=2, column=0, padx=10, pady=5)
end_port_entry = tk.Entry(pencere, width=20)
end_port_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(pencere, text="Dosya Adı:").grid(row=3, column=0, padx=10, pady=5)
filename_entry = tk.Entry(pencere, width=20)
filename_entry.grid(row=3, column=1, padx=10, pady=5)

tarama_buton = tk.Button(pencere, text="Tarama Yap", command=tarama_yap)
tarama_buton.grid(row=4, column=0, columnspan=2, pady=10)

sonuc_text = scrolledtext.ScrolledText(pencere, width=50, height=15)
sonuc_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

pencere.mainloop()
