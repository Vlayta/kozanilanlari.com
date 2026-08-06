# -*- coding: utf-8 -*-
import sqlite3
import random
import os

def kur():
    ANA_DIZIN = os.path.dirname(os.path.abspath(__file__))
    DB_YOLU = os.path.join(ANA_DIZIN, "veriler.db")
    
    baglanti = sqlite3.connect(DB_YOLU)
    imlec = baglanti.cursor()
    


    imlec.execute("""
        CREATE TABLE IF NOT EXISTS kullanicilar (
            ad TEXT PRIMARY KEY,
            email TEXT UNIQUE,
            sifre TEXT,
            telefon TEXT UNIQUE,
            sifre_token TEXT,
            token_suresi TEXT
        )
        
        
    """)
        
    imlec.execute("""
        CREATE TABLE IF NOT EXISTS urunler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kod TEXT,
            ad TEXT,
            fiyat REAL,
            resim TEXT,
            marka TEXT,
            model TEXT,
            yil TEXT,
            km TEXT,
            yakit TEXT,
            vites TEXT,
            degisen TEXT,
            boya TEXT,
            tramer TEXT,
            telefon TEXT,
            resimler TEXT,
            ilani_veren TEXT,
            kategori TEXT,
            acıklama TEXT DEFAULT ''
        )
    """)
    baglanti.commit()

    imlec.execute("SELECT * FROM kullanicilar WHERE ad='mahir'")
    if len(imlec.fetchall()) == 0:
        imlec.execute(""" INSERT INTO kullanicilar (ad,email,sifre,telefon,sifre_token,token_suresi) VALUES ('mahir','m@gmail.com','1234','05051112233', NULL , NULL )""")
    
    imlec.execute("SELECT * FROM urunler")
    if len(imlec.fetchall()) == 0:
        semboller = "0123456789ABCDEFGHJKLMNPRST"
        kod1 = "".join(random.choices(semboller, k=5))
        kod2 = "".join(random.choices(semboller, k=5))
        kod3 = "".join(random.choices(semboller, k=5))
        kod4 = "".join(random.choices(semboller, k=5))
        
        imlec.execute("""
            INSERT INTO urunler (kod, ad, fiyat, resim, marka, model, yil, km, yakit, vites, degisen, boya, tramer, telefon, resimler, ilani_veren, kategori, acıklama)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (kod1, "Kozan Merkezde Temiz Egea", 640000.0, "1_egea.jpg", "Fiat", "Egea", "2019", "120000", "Dizel", "Manuel", "false", "true", "false", "05051112233", '["1_egea.jpg"]', "mahir", "Otomobil", ""))
        
        imlec.execute("""
            INSERT INTO urunler (kod, ad, fiyat, resim, marka, model, yil, km, yakit, vites, degisen, boya, tramer, telefon, resimler, ilani_veren, kategori, acıklama)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (kod2, "Doktordan Otomatik Corolla", 890000.0, "1_corolla.jpg", "Toyota", "Corolla", "2021", "65000", "Benzin", "Otomatik", "false", "false", "false", "05324445566", '["1_corolla.jpg"]', "mahir", "Otomobil", ""))

        imlec.execute("""
            INSERT INTO urunler (kod, ad, fiyat, resim, marka, model, yil, km, yakit, vites, degisen, boya, tramer, telefon, resimler, ilani_veren, kategori, acıklama)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (kod3, "Kozan Satılık Geniş 3+1 Daire", 2450000.0, "varsayilan_araba.jpg", "Apartman Dairesi", "Satılık", "5", "145", "3+1", "3. Kat", "false", "false", "true", "05051112233", '["varsayilan_araba.jpg"]', "mahir", "Daire", ""))

        imlec.execute("""
            INSERT INTO urunler (kod, ad, fiyat, resim, marka, model, yil, km, yakit, vites, degisen, boya, tramer, telefon, resimler, ilani_veren, kategori, acıklama)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (kod4, "Yatırımlık İmarlı Arsa", 1150000.0, "varsayilan_araba.jpg", "Konut İmarı", "Satılık", "", "520", "", "", "142", "8", "false", "05051112233", '["varsayilan_araba.jpg"]', "mahir", "Arsa", ""))
        
    baglanti.commit()
    baglanti.close()
    print("✓ Veritabanı ve yetki tabloları başarıyla kuruldu!")

if __name__ == "__main__":
    kur()
