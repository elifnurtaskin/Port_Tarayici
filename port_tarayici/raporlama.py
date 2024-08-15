import matplotlib.pyplot as plt
from tkinter import messagebox

def analiz_ve_raporlama(acik_portlar):
    if not acik_portlar:
        messagebox.showinfo("Analiz", "Analiz edilecek açık port bulunamadı.")
        return

    # Servislerin dağılımı
    servis_dagilimi = {}
    for _, servis in acik_portlar:
        if servis in servis_dagilimi:
            servis_dagilimi[servis] += 1
        else:
            servis_dagilimi[servis] = 1

    # Pasta grafiği oluşturma
    servisler = list(servis_dagilimi.keys())
    sayilar = list(servis_dagilimi.values())

    plt.figure(figsize=(10, 7))
    plt.pie(sayilar, labels=servisler, autopct='%1.1f%%', startangle=140)
    plt.title("Açık Portların Servis Dağılımı")
    plt.axis('equal')  # Eşit eksen oranı
    plt.show()
