import sqlite3
import os

ANA_DIZIN = os.path.dirname(os.path.abspath(__file__))
DB_YOLU = os.path.join(ANA_DIZIN, "veriler.db")

baglanti = sqlite3.connect(DB_YOLU)
imlec = baglanti.cursor()

# urunler tablosu
try:
    imlec.execute("ALTER TABLE urunler ADD COLUMN acıklama TEXT DEFAULT ''")
    print("✓ acıklama sütunu eklendi.")
except sqlite3.OperationalError:
    print("ℹ acıklama sütunu zaten mevcut.")

# kullanicilar tablosu
try:
    imlec.execute("ALTER TABLE kullanicilar ADD COLUMN sifre_token TEXT")
    print("✓ sifre_token sütunu eklendi.")
except sqlite3.OperationalError:
    print("ℹ sifre_token sütunu zaten mevcut.")

try:
    imlec.execute("ALTER TABLE kullanicilar ADD COLUMN token_suresi TEXT")
    print("✓ token_suresi sütunu eklendi.")
except sqlite3.OperationalError:
    print("ℹ token_suresi sütunu zaten mevcut.")

baglanti.commit()
baglanti.close()

print("✓ Veritabanı güncellemesi tamamlandı.")
