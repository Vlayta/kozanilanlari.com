# -*- coding: utf-8 -*-

import os
import re
import sqlite3
from datetime import datetime, timedelta


# =========================================================
# DOSYA / VERİTABANI YOLU
# =========================================================

ANA_DIZIN = os.path.dirname(
    os.path.abspath(__file__)
)

VERI_DIZINI = (
    os.environ.get("PERSISTENT_DATA_DIR")
    or os.environ.get("DATA_DIR")
    or ANA_DIZIN
)

os.makedirs(
    VERI_DIZINI,
    exist_ok=True
)

DB_YOLU = os.path.join(
    VERI_DIZINI,
    "veriler.db"
)


# =========================================================
# KATEGORİLER
# =========================================================

KATEGORILER = [
    "Otomobil",
    "Daire",
    "Ev",
    "Dukkan",
    "Arsa",
    "Tarla"
]


# =========================================================
# İLAN KODU ÖN EKLERİ
# =========================================================

ILAN_KOD_ON_EKLERI = {
    "Otomobil": "OTO",
    "Daire": "DAI",
    "Ev": "EV",
    "Dukkan": "DUK",
    "Arsa": "ARS",
    "Tarla": "TAR"
}


# =========================================================
# TARİH
# =========================================================

def simdi():
    return datetime.now().isoformat(
        timespec="seconds"
    )


# =========================================================
# SQLITE BAĞLANTISI
# =========================================================

def baglan():

    baglanti = sqlite3.connect(
        DB_YOLU,
        timeout=30
    )

    baglanti.row_factory = sqlite3.Row

    baglanti.execute(
        "PRAGMA foreign_keys = ON"
    )

    baglanti.execute(
        "PRAGMA busy_timeout = 30000"
    )

    return baglanti


# =========================================================
# TABLO VAR MI?
# =========================================================

def tablo_var_mi(imlec, tablo):

    imlec.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
          AND name=?
        LIMIT 1
        """,
        (tablo,)
    )

    return imlec.fetchone() is not None


# =========================================================
# SÜTUN VAR MI?
# =========================================================

def sutun_var_mi(imlec, tablo, sutun):

    if not tablo_var_mi(imlec, tablo):
        return False

    imlec.execute(
        f'PRAGMA table_info("{tablo}")'
    )

    for kolon in imlec.fetchall():

        if kolon["name"] == sutun:
            return True

    return False


# =========================================================
# GÜVENLİ SQL İSMİ
# =========================================================

def sql_isim_kontrol(isim):

    if not re.match(
        r"^[A-Za-z_][A-Za-z0-9_]*$",
        isim or ""
    ):
        raise ValueError(
            f"Geçersiz SQL adı: {isim}"
        )

    return isim


# =========================================================
# SÜTUN EKLE
# =========================================================

def sutun_ekle(
    imlec,
    tablo,
    sutun,
    tanim,
    doldur=None
):

    tablo = sql_isim_kontrol(tablo)
    sutun = sql_isim_kontrol(sutun)

    if sutun_var_mi(
        imlec,
        tablo,
        sutun
    ):
        return False

    guvenli_tanim = tanim

    # Mevcut kayıtları bulunan SQLite
    # veritabanına doğrudan NOT NULL sütun
    # eklemek sorun çıkarabilir.
    if (
        "NOT NULL" in tanim.upper()
        and "DEFAULT" not in tanim.upper()
    ):

        guvenli_tanim = (
            tanim
            .replace(
                "NOT NULL",
                ""
            )
            .strip()
        )

    imlec.execute(
        f"""
        ALTER TABLE "{tablo}"
        ADD COLUMN "{sutun}" {guvenli_tanim}
        """
    )

    print(
        f"✓ {tablo}.{sutun} eklendi."
    )

    if doldur is not None:

        imlec.execute(
            f"""
            UPDATE "{tablo}"
            SET "{sutun}"=?
            WHERE "{sutun}" IS NULL
            """,
            (doldur,)
        )

    return True


# =========================================================
# İNDEKS OLUŞTUR
# =========================================================

def indeks_olustur(
    imlec,
    isim,
    tablo,
    kolonlar,
    unique=False
):

    isim = sql_isim_kontrol(isim)
    tablo = sql_isim_kontrol(tablo)

    if not tablo_var_mi(
        imlec,
        tablo
    ):
        return

    kolonlar = kolonlar.strip()

    ifade = "CREATE "

    if unique:
        ifade += "UNIQUE "

    ifade += (
        f'INDEX IF NOT EXISTS "{isim}" '
        f'ON "{tablo}" ({kolonlar})'
    )

    imlec.execute(ifade)


# =========================================================
# VARSAYILAN YÖNETİCİ
# =========================================================

def yonetici_kontrol(imlec):

    imlec.execute(
        """
        SELECT id
        FROM kullanicilar
        WHERE LOWER(ad)=LOWER(?)
        LIMIT 1
        """,
        ("mahir",)
    )

    kullanici = imlec.fetchone()

    if kullanici:

        print(
            "✓ Varsayılan yönetici mevcut: mahir"
        )

        return

    try:

        imlec.execute(
            """
            INSERT INTO kullanicilar
            (
                ad,
                email,
                sifre,
                telefon,
                sifre_token,
                token_suresi,
                olusturma_tarihi
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "mahir",
                "m@gmail.com",
                "1234",
                "05051112233",
                None,
                None,
                simdi()
            )
        )

        print(
            "✓ Varsayılan yönetici oluşturuldu: mahir"
        )

    except sqlite3.IntegrityError as hata:

        print(
            "⚠ Varsayılan yönetici oluşturulamadı:"
        )

        print(hata)


# =========================================================
# KATEGORİ NORMALİZE
# =========================================================

def kategori_normalize(kategori):

    kategori = str(
        kategori or ""
    ).strip()

    eslesmeler = {

        "Dükkan": "Dukkan",
        "Dükkan/İşyeri": "Dukkan",
        "Dukkan/İşyeri": "Dukkan",
        "İşyeri": "Dukkan",
        "Isyeri": "Dukkan"

    }

    return eslesmeler.get(
        kategori,
        kategori
    )


# =========================================================
# ESKİ KATEGORİLERİ DÜZELT
# =========================================================

def kategorileri_duzelt(imlec):

    if not tablo_var_mi(
        imlec,
        "ilanlar"
    ):
        return

    imlec.execute(
        """
        UPDATE ilanlar
        SET kategori='Dukkan'
        WHERE kategori IN (
            'Dükkan',
            'Dükkan/İşyeri',
            'Dukkan/İşyeri',
            'İşyeri',
            'Isyeri'
        )
        """
    )


# =========================================================
# TARİHLERİ DOLDUR
# =========================================================

def tarihleri_doldur(imlec):

    if not tablo_var_mi(
        imlec,
        "ilanlar"
    ):
        return

    tarih = simdi()

    imlec.execute(
        """
        UPDATE ilanlar
        SET olusturma_tarihi=?
        WHERE olusturma_tarihi IS NULL
           OR TRIM(olusturma_tarihi)=''
        """,
        (tarih,)
    )

    imlec.execute(
        """
        UPDATE ilanlar
        SET guncelleme_tarihi=?
        WHERE guncelleme_tarihi IS NULL
           OR TRIM(guncelleme_tarihi)=''
        """,
        (tarih,)
    )


# =========================================================
# İLAN KODLARINI TAMAMLA
# =========================================================

def eski_ilan_kodlarini_tamamla(imlec):

    if not tablo_var_mi(
        imlec,
        "ilanlar"
    ):
        return

    if not tablo_var_mi(
        imlec,
        "ilan_sayaclari"
    ):
        return

    imlec.execute(
        """
        SELECT
            id,
            kategori,
            ilan_kodu
        FROM ilanlar
        ORDER BY id ASC
        """
    )

    ilanlar = imlec.fetchall()

    kullanilan_kodlar = set()

    for ilan in ilanlar:

        kod = str(
            ilan["ilan_kodu"] or ""
        ).strip()

        if kod:
            kullanilan_kodlar.add(kod)

    sayaclar = {
        kategori: 0
        for kategori in KATEGORILER
    }

    # Önce mevcut geçerli kodlardan sayaçları hesapla.
    for ilan in ilanlar:

        kategori = kategori_normalize(
            ilan["kategori"]
        )

        if kategori not in ILAN_KOD_ON_EKLERI:
            continue

        kod = str(
            ilan["ilan_kodu"] or ""
        ).strip()

        on_ek = ILAN_KOD_ON_EKLERI[
            kategori
        ]

        if not kod.startswith(
            on_ek + "-"
        ):
            continue

        try:

            numara = int(
                kod.split(
                    "-",
                    1
                )[1]
            )

            if numara > sayaclar[kategori]:
                sayaclar[kategori] = numara

        except (
            ValueError,
            IndexError
        ):
            continue

    # Eksik kodları tamamla.
    for ilan in ilanlar:

        mevcut_kod = str(
            ilan["ilan_kodu"] or ""
        ).strip()

        kategori = kategori_normalize(
            ilan["kategori"]
        )

        if kategori not in ILAN_KOD_ON_EKLERI:
            kategori = "Otomobil"

        if mevcut_kod:
            # Kategoriyi de standartlaştır.
            if ilan["kategori"] != kategori:
                imlec.execute(
                    """
                    UPDATE ilanlar
                    SET kategori=?
                    WHERE id=?
                    """,
                    (
                        kategori,
                        ilan["id"]
                    )
                )
            continue

        sayaclar[kategori] += 1

        on_ek = ILAN_KOD_ON_EKLERI[
            kategori
        ]

        yeni_kod = (
            f"{on_ek}-"
            f"{sayaclar[kategori]:06d}"
        )

        while yeni_kod in kullanilan_kodlar:

            sayaclar[kategori] += 1

            yeni_kod = (
                f"{on_ek}-"
                f"{sayaclar[kategori]:06d}"
            )

        imlec.execute(
            """
            UPDATE ilanlar
            SET
                ilan_kodu=?,
                kategori=?
            WHERE id=?
            """,
            (
                yeni_kod,
                kategori,
                ilan["id"]
            )
        )

        kullanilan_kodlar.add(
            yeni_kod
        )

        print(
            f"✓ İlan kodu tamamlandı: "
            f"ID {ilan['id']} -> {yeni_kod}"
        )

    # Sayaçları kesin olarak yeniden yaz.
    for kategori in KATEGORILER:

        imlec.execute(
            """
            SELECT ilan_kodu
            FROM ilanlar
            WHERE kategori=?
            """,
            (kategori,)
        )

        en_buyuk = 0

        on_ek = ILAN_KOD_ON_EKLERI[
            kategori
        ]

        for satir in imlec.fetchall():

            kod = str(
                satir["ilan_kodu"] or ""
            ).strip()

            if not kod.startswith(
                on_ek + "-"
            ):
                continue

            try:

                numara = int(
                    kod.split(
                        "-",
                        1
                    )[1]
                )

                en_buyuk = max(
                    en_buyuk,
                    numara
                )

            except (
                ValueError,
                IndexError
            ):
                continue

        imlec.execute(
            """
            UPDATE ilan_sayaclari
            SET son_numara=?
            WHERE kategori=?
            """,
            (
                en_buyuk,
                kategori
            )
        )

    print(
        "✓ İlan kodları ve sayaçlar senkronize edildi."
    )


# =========================================================
# ESKİ KULLANICILARA ÜCRETSİZ ABONELİK
# =========================================================

def eski_kullanicilara_abonelik_ver(
    imlec
):

    if not tablo_var_mi(
        imlec,
        "kullanicilar"
    ):
        return

    if not tablo_var_mi(
        imlec,
        "abonelikler"
    ):
        return

    imlec.execute(
        """
        SELECT ad
        FROM kullanicilar
        """
    )

    kullanicilar = imlec.fetchall()

    for kullanici in kullanicilar:

        kullanici_adi = str(
            kullanici["ad"] or ""
        ).strip()

        if not kullanici_adi:
            continue

        mevcut = imlec.execute(
            """
            SELECT id
            FROM abonelikler
            WHERE kullanici_adi=?
            LIMIT 1
            """,
            (kullanici_adi,)
        ).fetchone()

        if mevcut:
            continue

        baslangic = datetime.now()

        bitis = (
            baslangic +
            timedelta(days=30)
        )

        imlec.execute(
            """
            INSERT INTO abonelikler
            (
                kullanici_adi,
                paket,
                durum,
                baslangic_tarihi,
                bitis_tarihi,
                olusturma_tarihi
            )
            VALUES (
                ?,
                'Ucretsiz',
                'aktif',
                ?,
                ?,
                ?
            )
            """,
            (
                kullanici_adi,
                baslangic.isoformat(
                    timespec="seconds"
                ),
                bitis.isoformat(
                    timespec="seconds"
                ),
                baslangic.isoformat(
                    timespec="seconds"
                )
            )
        )

        print(
            "✓ Eski kullanıcı için ücretsiz "
            f"abonelik oluşturuldu: {kullanici_adi}"
        )


# =========================================================
# VERİTABANI KURULUMU
# =========================================================

def kur():

    print()
    print(
        "=========================================="
    )
    print(
        "VERİTABANI KURULUMU / MİGRASYON"
    )
    print(
        "=========================================="
    )
    print(
        f"Veri dizini: {VERI_DIZINI}"
    )
    print(
        f"Veritabanı: {DB_YOLU}"
    )
    print()

    baglanti = baglan()
    imlec = baglanti.cursor()

    try:

        # =================================================
        # SQLITE
        # =================================================

        imlec.execute(
            "PRAGMA foreign_keys = ON"
        )

        imlec.execute(
            "PRAGMA busy_timeout = 30000"
        )

        try:
            imlec.execute(
                "PRAGMA journal_mode = WAL"
            )
        except sqlite3.DatabaseError as hata:
            print(
                "⚠ WAL modu etkinleştirilemedi:",
                hata
            )

        try:
            imlec.execute(
                "PRAGMA synchronous = NORMAL"
            )
        except sqlite3.DatabaseError:
            pass


        # =================================================
        # 1. KULLANICILAR
        # =================================================

        imlec.execute(
            """
            CREATE TABLE IF NOT EXISTS kullanicilar (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                ad TEXT NOT NULL UNIQUE,

                email TEXT NOT NULL UNIQUE,

                sifre TEXT NOT NULL,

                telefon TEXT NOT NULL UNIQUE,

                sifre_token TEXT,

                token_suresi TEXT,

                olusturma_tarihi TEXT NOT NULL

            )
            """
        )

        sutun_ekle(
            imlec,
            "kullanicilar",
            "sifre_token",
            "TEXT"
        )

        sutun_ekle(
            imlec,
            "kullanicilar",
            "token_suresi",
            "TEXT"
        )

        sutun_ekle(
            imlec,
            "kullanicilar",
            "olusturma_tarihi",
            "TEXT"
        )

        if sutun_var_mi(
            imlec,
            "kullanicilar",
            "olusturma_tarihi"
        ):

            imlec.execute(
                """
                UPDATE kullanicilar
                SET olusturma_tarihi=?
                WHERE olusturma_tarihi IS NULL
                   OR TRIM(olusturma_tarihi)=''
                """,
                (simdi(),)
            )

        print(
            "✓ kullanicilar hazır."
        )


        # =================================================
        # 2. İLANLAR
        # =================================================

        imlec.execute(
            """
            CREATE TABLE IF NOT EXISTS ilanlar (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                ilan_kodu TEXT,

                kategori TEXT NOT NULL
                    DEFAULT 'Otomobil',

                baslik TEXT NOT NULL
                    DEFAULT '',

                fiyat REAL NOT NULL
                    DEFAULT 0,

                aciklama TEXT
                    DEFAULT '',

                ilan_sahibi TEXT NOT NULL
                    DEFAULT '',

                telefon TEXT
                    DEFAULT '',

                aktif INTEGER NOT NULL
                    DEFAULT 1,

                olusturma_tarihi TEXT
                    DEFAULT '',

                guncelleme_tarihi TEXT
                    DEFAULT ''

            )
            """
        )

        ilan_sutunlari = [

            (
                "ilan_kodu",
                "TEXT"
            ),

            (
                "kategori",
                "TEXT DEFAULT 'Otomobil'"
            ),

            (
                "baslik",
                "TEXT DEFAULT ''"
            ),

            (
                "fiyat",
                "REAL DEFAULT 0"
            ),

            (
                "aciklama",
                "TEXT DEFAULT ''"
            ),

            (
                "ilan_sahibi",
                "TEXT DEFAULT ''"
            ),

            (
                "telefon",
                "TEXT DEFAULT ''"
            ),

            (
                "aktif",
                "INTEGER DEFAULT 1"
            ),

            (
                "olusturma_tarihi",
                "TEXT DEFAULT ''"
            ),

            (
                "guncelleme_tarihi",
                "TEXT DEFAULT ''"
            )

        ]

        for sutun, tanim in ilan_sutunlari:

            sutun_ekle(
                imlec,
                "ilanlar",
                sutun,
                tanim
            )

        print(
            "✓ ilanlar hazır."
        )


        # =================================================
        # 3. OTOMOBİL
        # =================================================

        imlec.execute(
            """
            CREATE TABLE IF NOT EXISTS otomobil_detay (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                ilan_id INTEGER NOT NULL UNIQUE,

                marka TEXT DEFAULT '',

                model TEXT DEFAULT '',

                yil INTEGER,

                km INTEGER,

                yakit TEXT DEFAULT '',

                vites TEXT DEFAULT '',

                kasa_tipi TEXT DEFAULT '',

                motor_hacmi TEXT DEFAULT '',

                motor_gucu TEXT DEFAULT '',

                cekis TEXT DEFAULT '',

                renk TEXT DEFAULT '',

                hasar_durumu TEXT DEFAULT '',

                degisen INTEGER DEFAULT 0,

                boya INTEGER DEFAULT 0,

                tramer INTEGER DEFAULT 0,

                takas INTEGER DEFAULT 0,

                kredi_uygun INTEGER DEFAULT 0,

                FOREIGN KEY (ilan_id)
                    REFERENCES ilanlar(id)
                    ON DELETE CASCADE

            )
            """
        )

        otomobil_sutunlari = [

            ("marka", "TEXT DEFAULT ''"),
            ("model", "TEXT DEFAULT ''"),
            ("yil", "INTEGER"),
            ("km", "INTEGER"),
            ("yakit", "TEXT DEFAULT ''"),
            ("vites", "TEXT DEFAULT ''"),
            ("kasa_tipi", "TEXT DEFAULT ''"),
            ("motor_hacmi", "TEXT DEFAULT ''"),
            ("motor_gucu", "TEXT DEFAULT ''"),
            ("cekis", "TEXT DEFAULT ''"),
            ("renk", "TEXT DEFAULT ''"),
            ("hasar_durumu", "TEXT DEFAULT ''"),
            ("degisen", "INTEGER DEFAULT 0"),
            ("boya", "INTEGER DEFAULT 0"),
            ("tramer", "INTEGER DEFAULT 0"),
            ("takas", "INTEGER DEFAULT 0"),
            ("kredi_uygun", "INTEGER DEFAULT 0")

        ]

        for sutun, tanim in otomobil_sutunlari:

            sutun_ekle(
                imlec,
                "otomobil_detay",
                sutun,
                tanim
            )

        print(
            "✓ otomobil_detay hazır."
        )


        # =================================================
        # 4. EMLAK
        # =================================================

        imlec.execute(
            """
            CREATE TABLE IF NOT EXISTS emlak_detay (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                ilan_id INTEGER NOT NULL UNIQUE,

                emlak_tipi TEXT DEFAULT '',

                ilan_durumu TEXT DEFAULT '',

                metrekare REAL,

                oda_sayisi TEXT DEFAULT '',

                salon_sayisi TEXT DEFAULT '',

                bina_yasi INTEGER,

                bulundugu_kat TEXT DEFAULT '',

                toplam_kat INTEGER,

                isitma TEXT DEFAULT '',

                banyo_sayisi INTEGER,

                balkon INTEGER DEFAULT 0,

                asansor INTEGER DEFAULT 0,

                otopark INTEGER DEFAULT 0,

                esyali INTEGER DEFAULT 0,

                site_icerisinde INTEGER DEFAULT 0,

                aidat REAL,

                kredi_uygun INTEGER DEFAULT 0,

                tapu_durumu TEXT DEFAULT '',

                kullanim_durumu TEXT DEFAULT '',

                takas INTEGER DEFAULT 0,

                FOREIGN KEY (ilan_id)
                    REFERENCES ilanlar(id)
                    ON DELETE CASCADE

            )
            """
        )

        emlak_sutunlari = [

            ("emlak_tipi", "TEXT DEFAULT ''"),
            ("ilan_durumu", "TEXT DEFAULT ''"),
            ("metrekare", "REAL"),
            ("oda_sayisi", "TEXT DEFAULT ''"),
            ("salon_sayisi", "TEXT DEFAULT ''"),
            ("bina_yasi", "INTEGER"),
            ("bulundugu_kat", "TEXT DEFAULT ''"),
            ("toplam_kat", "INTEGER"),
            ("isitma", "TEXT DEFAULT ''"),
            ("banyo_sayisi", "INTEGER"),
            ("balkon", "INTEGER DEFAULT 0"),
            ("asansor", "INTEGER DEFAULT 0"),
            ("otopark", "INTEGER DEFAULT 0"),
            ("esyali", "INTEGER DEFAULT 0"),
            ("site_icerisinde", "INTEGER DEFAULT 0"),
            ("aidat", "REAL"),
            ("kredi_uygun", "INTEGER DEFAULT 0"),
            ("tapu_durumu", "TEXT DEFAULT ''"),
            ("kullanim_durumu", "TEXT DEFAULT ''"),
            ("takas", "INTEGER DEFAULT 0")

        ]

        for sutun, tanim in emlak_sutunlari:

            sutun_ekle(
                imlec,
                "emlak_detay",
                sutun,
                tanim
            )

        print(
            "✓ emlak_detay hazır."
        )


        # =================================================
        # 5. İŞYERİ
        # =================================================

        imlec.execute(
            """
            CREATE TABLE IF NOT EXISTS isyeri_detay (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                ilan_id INTEGER NOT NULL UNIQUE,

                isyeri_tipi TEXT DEFAULT '',

                ilan_durumu TEXT DEFAULT '',

                metrekare REAL,

                bina_yasi INTEGER,

                oda_sayisi TEXT DEFAULT '',

                bulundugu_kat TEXT DEFAULT '',

                toplam_kat INTEGER,

                isitma TEXT DEFAULT '',

                banyo INTEGER DEFAULT 0,

                mutfak INTEGER DEFAULT 0,

                depo INTEGER DEFAULT 0,

                vitrin INTEGER DEFAULT 0,

                cephe TEXT DEFAULT '',

                asansor INTEGER DEFAULT 0,

                otopark INTEGER DEFAULT 0,

                aidat REAL,

                kredi_uygun INTEGER DEFAULT 0,

                tapu_durumu TEXT DEFAULT '',

                kullanim_durumu TEXT DEFAULT '',

                takas INTEGER DEFAULT 0,

                FOREIGN KEY (ilan_id)
                    REFERENCES ilanlar(id)
                    ON DELETE CASCADE

            )
            """
        )

        isyeri_sutunlari = [

            ("isyeri_tipi", "TEXT DEFAULT ''"),
            ("ilan_durumu", "TEXT DEFAULT ''"),
            ("metrekare", "REAL"),
            ("bina_yasi", "INTEGER"),
            ("oda_sayisi", "TEXT DEFAULT ''"),
            ("bulundugu_kat", "TEXT DEFAULT ''"),
            ("toplam_kat", "INTEGER"),
            ("isitma", "TEXT DEFAULT ''"),
            ("banyo", "INTEGER DEFAULT 0"),
            ("mutfak", "INTEGER DEFAULT 0"),
            ("depo", "INTEGER DEFAULT 0"),
            ("vitrin", "INTEGER DEFAULT 0"),
            ("cephe", "TEXT DEFAULT ''"),
            ("asansor", "INTEGER DEFAULT 0"),
            ("otopark", "INTEGER DEFAULT 0"),
            ("aidat", "REAL"),
            ("kredi_uygun", "INTEGER DEFAULT 0"),
            ("tapu_durumu", "TEXT DEFAULT ''"),
            ("kullanim_durumu", "TEXT DEFAULT ''"),
            ("takas", "INTEGER DEFAULT 0")

        ]

        for sutun, tanim in isyeri_sutunlari:

            sutun_ekle(
                imlec,
                "isyeri_detay",
                sutun,
                tanim
            )

        print(
            "✓ isyeri_detay hazır."
        )


        # =================================================
        # 6. ARSA / TARLA
        # =================================================

        imlec.execute(
            """
            CREATE TABLE IF NOT EXISTS arsa_detay (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                ilan_id INTEGER NOT NULL UNIQUE,

                ilan_durumu TEXT DEFAULT '',

                metrekare REAL,

                imar_durumu TEXT DEFAULT '',

                ada_no TEXT DEFAULT '',

                parsel_no TEXT DEFAULT '',

                tapu_durumu TEXT DEFAULT '',

                kredi_uygun INTEGER DEFAULT 0,

                takas INTEGER DEFAULT 0,

                kat_karsiligi INTEGER DEFAULT 0,

                ifrazli INTEGER DEFAULT 0,

                kaks TEXT DEFAULT '',

                emsal TEXT DEFAULT '',

                gabari TEXT DEFAULT '',

                cephe TEXT DEFAULT '',

                yol_durumu TEXT DEFAULT '',

                elektrik INTEGER DEFAULT 0,

                su INTEGER DEFAULT 0,

                kanalizasyon INTEGER DEFAULT 0,

                dogalgaz INTEGER DEFAULT 0,

                kadastro_yolu INTEGER DEFAULT 0,

                merkeze_uzaklik TEXT DEFAULT '',

                FOREIGN KEY (ilan_id)
                    REFERENCES ilanlar(id)
                    ON DELETE CASCADE

            )
            """
        )

        arsa_sutunlari = [

            ("ilan_durumu", "TEXT DEFAULT ''"),
            ("metrekare", "REAL"),
            ("imar_durumu", "TEXT DEFAULT ''"),
            ("ada_no", "TEXT DEFAULT ''"),
            ("parsel_no", "TEXT DEFAULT ''"),
            ("tapu_durumu", "TEXT DEFAULT ''"),
            ("kredi_uygun", "INTEGER DEFAULT 0"),
            ("takas", "INTEGER DEFAULT 0"),
            ("kat_karsiligi", "INTEGER DEFAULT 0"),
            ("ifrazli", "INTEGER DEFAULT 0"),
            ("kaks", "TEXT DEFAULT ''"),
            ("emsal", "TEXT DEFAULT ''"),
            ("gabari", "TEXT DEFAULT ''"),
            ("cephe", "TEXT DEFAULT ''"),
            ("yol_durumu", "TEXT DEFAULT ''"),
            ("elektrik", "INTEGER DEFAULT 0"),
            ("su", "INTEGER DEFAULT 0"),
            ("kanalizasyon", "INTEGER DEFAULT 0"),
            ("dogalgaz", "INTEGER DEFAULT 0"),
            ("kadastro_yolu", "INTEGER DEFAULT 0"),
            ("merkeze_uzaklik", "TEXT DEFAULT ''")

        ]

        for sutun, tanim in arsa_sutunlari:

            sutun_ekle(
                imlec,
                "arsa_detay",
                sutun,
                tanim
            )

        print(
            "✓ arsa_detay hazır."
        )


        # =================================================
        # 7. İLAN FOTOĞRAFLARI
        # =================================================

        imlec.execute(
            """
            CREATE TABLE IF NOT EXISTS ilan_resimleri (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                ilan_id INTEGER NOT NULL,

                dosya_adi TEXT NOT NULL,

                sira INTEGER DEFAULT 1,

                kapak INTEGER DEFAULT 0,

                FOREIGN KEY (ilan_id)
                    REFERENCES ilanlar(id)
                    ON DELETE CASCADE

            )
            """
        )

        resim_sutunlari = [

            ("ilan_id", "INTEGER"),
            ("dosya_adi", "TEXT DEFAULT ''"),
            ("sira", "INTEGER DEFAULT 1"),
            ("kapak", "INTEGER DEFAULT 0")

        ]

        for sutun, tanim in resim_sutunlari:

            sutun_ekle(
                imlec,
                "ilan_resimleri",
                sutun,
                tanim
            )

        print(
            "✓ ilan_resimleri hazır."
        )


        # =================================================
        # 8. İLAN SAYAÇLARI
        # =================================================

        imlec.execute(
            """
            CREATE TABLE IF NOT EXISTS ilan_sayaclari (

                kategori TEXT PRIMARY KEY,

                son_numara INTEGER NOT NULL
                    DEFAULT 0

            )
            """
        )

        for kategori in KATEGORILER:

            imlec.execute(
                """
                INSERT OR IGNORE INTO
                ilan_sayaclari
                (
                    kategori,
                    son_numara
                )
                VALUES (?, 0)
                """,
                (kategori,)
            )

        print(
            "✓ ilan_sayaclari hazır."
        )


        # =================================================
        # 9. ABONELİKLER
        # =================================================

        imlec.execute(
            """
            CREATE TABLE IF NOT EXISTS abonelikler (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                kullanici_adi TEXT NOT NULL UNIQUE,

                paket TEXT NOT NULL
                    DEFAULT 'Ucretsiz',

                durum TEXT NOT NULL
                    DEFAULT 'aktif',

                baslangic_tarihi TEXT NOT NULL,

                bitis_tarihi TEXT NOT NULL,

                olusturma_tarihi TEXT NOT NULL

            )
            """
        )

        abonelik_sutunlari = [

            (
                "kullanici_adi",
                "TEXT DEFAULT ''"
            ),

            (
                "paket",
                "TEXT DEFAULT 'Ucretsiz'"
            ),

            (
                "durum",
                "TEXT DEFAULT 'aktif'"
            ),

            (
                "baslangic_tarihi",
                "TEXT DEFAULT ''"
            ),

            (
                "bitis_tarihi",
                "TEXT DEFAULT ''"
            ),

            (
                "olusturma_tarihi",
                "TEXT DEFAULT ''"
            )

        ]

        for sutun, tanim in abonelik_sutunlari:

            sutun_ekle(
                imlec,
                "abonelikler",
                sutun,
                tanim
            )

        print(
            "✓ abonelikler hazır."
        )


        # =================================================
        # 10. ESKİ VERİLERİ DÜZELT
        # =================================================

        kategorileri_duzelt(
            imlec
        )

        tarihleri_doldur(
            imlec
        )


        # =================================================
        # 11. ESKİ İLAN KODLARINI TAMAMLA
        # =================================================

        eski_ilan_kodlarini_tamamla(
            imlec
        )


        # =================================================
        # 12. İNDEKSLER
        # =================================================

        indeks_olustur(
            imlec,
            "idx_ilanlar_kategori",
            "ilanlar",
            "kategori"
        )

        indeks_olustur(
            imlec,
            "idx_ilanlar_aktif",
            "ilanlar",
            "aktif"
        )

        indeks_olustur(
            imlec,
            "idx_ilanlar_sahibi",
            "ilanlar",
            "ilan_sahibi"
        )

        indeks_olustur(
            imlec,
            "idx_resimler_ilan",
            "ilan_resimleri",
            "ilan_id"
        )

        indeks_olustur(
            imlec,
            "idx_resimler_sira",
            "ilan_resimleri",
            "ilan_id, sira"
        )

        indeks_olustur(
            imlec,
            "idx_abonelik_kullanici",
            "abonelikler",
            "kullanici_adi"
        )

        indeks_olustur(
            imlec,
            "idx_ilanlar_kod",
            "ilanlar",
            "ilan_kodu"
        )

        print(
            "✓ Veritabanı indeksleri hazır."
        )


        # =================================================
        # 13. VARSAYILAN YÖNETİCİ
        # =================================================

        yonetici_kontrol(
            imlec
        )


        # =================================================
        # 14. ESKİ KULLANICILARA ABONELİK
        # =================================================

        eski_kullanicilara_abonelik_ver(
            imlec
        )


        # =================================================
        # 15. COMMIT
        # =================================================

        baglanti.commit()


        # =================================================
        # 16. SON KONTROL
        # =================================================

        tablolar = [

            "kullanicilar",
            "ilanlar",
            "otomobil_detay",
            "emlak_detay",
            "isyeri_detay",
            "arsa_detay",
            "ilan_resimleri",
            "ilan_sayaclari",
            "abonelikler"

        ]

        print()
        print(
            "=========================================="
        )
        print(
            "✓ VERİTABANI BAŞARIYLA HAZIRLANDI"
        )
        print(
            "=========================================="
        )

        print()
        print(
            f"Veritabanı: {DB_YOLU}"
        )

        print()
        print(
            "Tablolar:"
        )

        for sira, tablo in enumerate(
            tablolar,
            start=1
        ):

            mevcut = tablo_var_mi(
                imlec,
                tablo
            )

            print(
                f"{sira}. {tablo} "
                f"{'✓' if mevcut else '✗'}"
            )

        print()
        print(
            "Kategoriler:"
        )

        for kategori in KATEGORILER:

            print(
                f"- {kategori}"
            )

        print()
        print(
            "=========================================="
        )


    except Exception as hata:

        baglanti.rollback()

        print()
        print(
            "=========================================="
        )
        print(
            "!!! VERİTABANI HATASI !!!"
        )
        print(
            "=========================================="
        )
        print(
            hata
        )

        raise

    finally:

        baglanti.close()


# =========================================================
# DOĞRUDAN ÇALIŞTIRMA
# =========================================================

if __name__ == "__main__":

    kur()