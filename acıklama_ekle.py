import sqlite3
import os

ANA_DIZIN = os.path.dirname(os.path.abspath(__file__))
DB_YOLU = os.path.join(ANA_DIZIN, "veriler.db")

try:
    baglanti = sqlite3.connect(DB_YOLU)
    imlec = baglanti.cursor()
    
    # urunler tablosuna 'acıklama' adında yeni bir TEXT sütunu ekler
    imlec.execute("ALTER TABLE urunler ADD COLUMN acıklama TEXT DEFAULT ''")
    
    baglanti.commit()
    print("✓ 'acıklama' sütunu veritabanına başarıyla eklendi!")
except sqlite3.OperationalError:
    print("ℹ 'acıklama' sütunu veritabanında zaten mevcut.")
finally:
    baglanti.close()
