import sqlite3
import tkinter as tk
from tkinter import ttk

class EserUygulamasi:
    def __init__(self, master):
        self.master = master
        self.master.title("Katalog Uygulaması")

        # Arayüz öğeleri oluşturuluyor
        self.tree = ttk.Treeview(self.master)
        self.tree["columns"] = ("eserID", "eserADI", "yazarID", "yayineviID", "konuID", "yayinyili", "ISBN")
        self.tree.heading("#0", text="", anchor="w")
        self.tree.column("#0", anchor="w", width=0)
        self.tree.heading("eserID", text="Eser ID")
        self.tree.heading("eserADI", text="Eser Adı")
        self.tree.heading("yazarID", text="Yazar ID")
        self.tree.heading("yayineviID", text="Yayınevi ID")
        self.tree.heading("konuID", text="Konu ID")
        self.tree.heading("yayinyili", text="Yayın Yılı")
        self.tree.heading("ISBN", text="ISBN")
        self.tree.pack()

        # Veritabanına bağlanma
        self.conn, self.cursor = self.baglanti_kur()

        # Arayüz düğmeleri
        self.btn_listele = tk.Button(self.master, text="Eserleri Listele", command=self.eserleri_listele)
        self.btn_listele.pack(pady=5)

        self.btn_ekle = tk.Button(self.master, text="Yeni Eser Ekle", command=self.yeni_eser_ekle_gui)
        self.btn_ekle.pack(pady=5)

        self.btn_ara = tk.Button(self.master, text="Eser Ara", command=self.eser_arama_gui)
        self.btn_ara.pack(pady=5)

        self.btn_sil = tk.Button(self.master, text="Veri Sil", command=self.veri_sil_gui)
        self.btn_sil.pack(pady=5)

        self.btn_guncelle = tk.Button(self.master, text="Veri Güncelle", command=self.veri_guncelle_gui)
        self.btn_guncelle.pack(pady=5)

    def baglanti_kur(self):
        conn = sqlite3.connect("veritabaniii.db")
        cursor = conn.cursor()
        return conn, cursor

    def baglanti_kapat(self):
        self.conn.close()

    def eserleri_listele(self):
        self.tree.delete(*self.tree.get_children())
        self.cursor.execute("SELECT * FROM Eser")
        eserler = self.cursor.fetchall()
        for eser in eserler:
            self.tree.insert("", "end", values=eser)

    def yeni_eser_ekle_gui(self):
        yeni_eser_pencere = tk.Toplevel(self.master)
        yeni_eser_pencere.title("Yeni Eser Ekle")

        tk.Label(yeni_eser_pencere, text="Eser Adı:").grid(row=0, column=0)
        eser_adi_entry = tk.Entry(yeni_eser_pencere)
        eser_adi_entry.grid(row=0, column=1)

        tk.Label(yeni_eser_pencere, text="Yazar ID:").grid(row=1, column=0)
        yazar_id_entry = tk.Entry(yeni_eser_pencere)
        yazar_id_entry.grid(row=1, column=1)

        tk.Label(yeni_eser_pencere, text="Yayınevi ID:").grid(row=2, column=0)
        yayinevi_id_entry = tk.Entry(yeni_eser_pencere)
        yayinevi_id_entry.grid(row=2, column=1)

        tk.Label(yeni_eser_pencere, text="Konu ID:").grid(row=3, column=0)
        konu_id_entry = tk.Entry(yeni_eser_pencere)
        konu_id_entry.grid(row=3, column=1)

        tk.Label(yeni_eser_pencere, text="Yayın Yılı:").grid(row=4, column=0)
        yayin_yili_entry = tk.Entry(yeni_eser_pencere)
        yayin_yili_entry.grid(row=4, column=1)

        tk.Label(yeni_eser_pencere, text="ISBN:").grid(row=5, column=0)
        isbn_entry = tk.Entry(yeni_eser_pencere)
        isbn_entry.grid(row=5, column=1)

        btn_ekle = tk.Button(yeni_eser_pencere, text="Eser Ekle", command=lambda: self.yeni_eser_ekle(eser_adi_entry.get(), yazar_id_entry.get(), yayinevi_id_entry.get(), konu_id_entry.get(), yayin_yili_entry.get(), isbn_entry.get()))
        btn_ekle.grid(row=6, columnspan=2, pady=10)

    def yeni_eser_ekle(self, eser_adi, yazar_id, yayinevi_id, konu_id, yayin_yili, isbn):
        self.cursor.execute("INSERT INTO Eser (eserADI, yazarID, yayineviID, konuID, yayinyili, ISBN) VALUES (?, ?, ?, ?, ?, ?)",
                            (eser_adi, yazar_id, yayinevi_id, konu_id, yayin_yili, isbn))
        self.conn.commit()
        self.eserleri_listele()

    def eser_arama_gui(self):
        arama_pencere = tk.Toplevel(self.master)
        arama_pencere.title("Eser Ara")

        tk.Label(arama_pencere, text="Arama Terimi:").grid(row=0, column=0)
        arama_terimi_entry = tk.Entry(arama_pencere)
        arama_terimi_entry.grid(row=0, column=1)

        btn_ara = tk.Button(arama_pencere, text="Ara", command=lambda: self.eser_arama(arama_terimi_entry.get()))
        btn_ara.grid(row=1, columnspan=2, pady=10)

    def eser_arama(self, arama_terimi):
        self.tree.delete(*self.tree.get_children())
        self.cursor.execute("SELECT * FROM Eser WHERE eserADI LIKE ? OR yazarID LIKE ? OR yayineviID LIKE ? OR konuID LIKE ? OR yayinyili LIKE ? OR ISBN LIKE ?",
                            ('%' + arama_terimi + '%', '%' + arama_terimi + '%', '%' + arama_terimi + '%', '%' + arama_terimi + '%', '%' + arama_terimi + '%', '%' + arama_terimi + '%'))
        eserler = self.cursor.fetchall()
        for eser in eserler:
            self.tree.insert("", "end", values=eser)

    def veri_sil_gui(self):
        sil_pencere = tk.Toplevel(self.master)
        sil_pencere.title("Veri Sil")

        tk.Label(sil_pencere, text="Silmek istediğiniz Eser ID:").grid(row=0, column=0)
        eser_id_sil_entry = tk.Entry(sil_pencere)
        eser_id_sil_entry.grid(row=0, column=1)

        btn_sil = tk.Button(sil_pencere, text="Sil", command=lambda: self.veri_sil(eser_id_sil_entry.get()))
        btn_sil.grid(row=1, columnspan=2, pady=10)

    def veri_sil(self, eser_id):
        self.cursor.execute("DELETE FROM Eser WHERE eserID=?", (eser_id,))
        self.conn.commit()
        self.eserleri_listele()

    def veri_guncelle_gui(self):
        guncelle_pencere = tk.Toplevel(self.master)
        guncelle_pencere.title("Veri Güncelle")

        tk.Label(guncelle_pencere, text="Güncellemek istediğiniz Eser ID:").grid(row=0, column=0)
        eser_id_guncelle_entry = tk.Entry(guncelle_pencere)
        eser_id_guncelle_entry.grid(row=0, column=1)

        tk.Label(guncelle_pencere, text="Yeni Eser Adı:").grid(row=1, column=0)
        yeni_eser_adi_entry = tk.Entry(guncelle_pencere)
        yeni_eser_adi_entry.grid(row=1, column=1)

        tk.Label(guncelle_pencere, text="Yeni Yazar ID:").grid(row=2, column=0)
        yeni_yazar_id_entry = tk.Entry(guncelle_pencere)
        yeni_yazar_id_entry.grid(row=2, column=1)

        tk.Label(guncelle_pencere, text="Yeni Yayınevi ID:").grid(row=3, column=0)
        yeni_yayinevi_id_entry = tk.Entry(guncelle_pencere)
        yeni_yayinevi_id_entry.grid(row=3, column=1)

        tk.Label(guncelle_pencere, text="Yeni Konu ID:").grid(row=4, column=0)
        yeni_konu_id_entry = tk.Entry(guncelle_pencere)
        yeni_konu_id_entry.grid(row=4, column=1)

        tk.Label(guncelle_pencere, text="Yeni Yayın Yılı:").grid(row=5, column=0)
        yeni_yayin_yili_entry = tk.Entry(guncelle_pencere)
        yeni_yayin_yili_entry.grid(row=5, column=1)

        tk.Label(guncelle_pencere, text="Yeni ISBN:").grid(row=6, column=0)
        yeni_isbn_entry = tk.Entry(guncelle_pencere)
        yeni_isbn_entry.grid(row=6, column=1)

        btn_guncelle = tk.Button(guncelle_pencere, text="Güncelle", command=lambda: self.veri_guncelle(eser_id_guncelle_entry.get(), yeni_eser_adi_entry.get(), yeni_yazar_id_entry.get(), yeni_yayinevi_id_entry.get(), yeni_konu_id_entry.get(), yeni_yayin_yili_entry.get(), yeni_isbn_entry.get()))
        btn_guncelle.grid(row=7, columnspan=2, pady=10)

    def veri_guncelle(self, eser_id, yeni_eser_adi, yeni_yazar_id, yeni_yayinevi_id, yeni_konu_id, yeni_yayin_yili, yeni_isbn):
        self.cursor.execute("UPDATE Eser SET eserADI=?, yazarID=?, yayineviID=?, konuID=?, yayinyili=?, ISBN=? WHERE eserID=?",
                            (yeni_eser_adi, yeni_yazar_id, yeni_yayinevi_id, yeni_konu_id, yeni_yayin_yili, yeni_isbn, eser_id))
        self.conn.commit()
        self.eserleri_listele()

if __name__ == "__main__":
    root = tk.Tk()
    uygulama = EserUygulamasi(root)
    root.mainloop()
