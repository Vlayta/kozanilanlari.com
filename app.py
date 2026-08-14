# -*- coding: utf-8 -*-

import os
import sqlite3
import secrets
import datetime

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    jsonify,
    flash,
    url_for,
    send_from_directory,
)

from werkzeug.utils import secure_filename

import veritabanini_kur as db


# =========================================================
# UYGULAMA
# =========================================================

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "A13Fe"
)


# =========================================================
# DİZİNLER / KALICI VERİ
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
# FOTOĞRAF DİZİNİ
# =========================================================

YEREL_UPLOAD_FOLDER = os.path.abspath(
    os.path.join(
        ANA_DIZIN,
        "static",
        "uploads"
    )
)


if os.environ.get("UPLOAD_FOLDER"):

    UPLOAD_FOLDER = os.path.abspath(
        os.environ.get("UPLOAD_FOLDER")
    )

elif (
    os.environ.get("PERSISTENT_DATA_DIR")
    or os.environ.get("DATA_DIR")
):

    UPLOAD_FOLDER = os.path.abspath(
        os.path.join(
            VERI_DIZINI,
            "uploads"
        )
    )

else:

    UPLOAD_FOLDER = YEREL_UPLOAD_FOLDER


os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# =========================================================
# DOSYA / FOTOĞRAF AYARLARI
# =========================================================

app.config["MAX_CONTENT_LENGTH"] = (
    32 * 1024 * 1024
)


IZINLI_RESIM_UZANTILARI = {
    "jpg",
    "jpeg",
    "png",
    "webp",
    "gif"
}


MAX_FOTO = 10


# =========================================================
# VERİTABANI
# =========================================================

db.kur()


# =========================================================
# SABİTLER
# =========================================================

SITE_YONETICILERI = [
    "mahir",
    "admin",
]


KATEGORILER = [
    "Otomobil",
    "Daire",
    "Ev",
    "Dukkan",
    "Arsa",
    "Tarla",
]


ILAN_KOD_ON_EKLERI = {

    "Otomobil": "OTO",
    "Daire": "DAI",
    "Ev": "EV",
    "Dukkan": "DUK",
    "Arsa": "ARS",
    "Tarla": "TAR",
}


ABONELIK_PAKETLERI = {

    "Ucretsiz": {
        "ad": "🎁 1 Aylık Ücretsiz",
        "gun": 30,
        "fiyat": 0
    },

    "Aylik": {
        "ad": "⭐ Aylık Paket",
        "gun": 30,
        "fiyat": 29
    },

    "UcAylik": {
        "ad": "🔥 3 Aylık Paket",
        "gun": 90,
        "fiyat": 69
    },

    "Yillik": {
        "ad": "👑 Yıllık Paket",
        "gun": 365,
        "fiyat": 199
    },
}


# =========================================================
# TARİH
# =========================================================

def simdi():

    return datetime.datetime.now().isoformat(
        timespec="seconds"
    )


# =========================================================
# KATEGORİ NORMALİZE
# =========================================================

def kategori_normalize(kategori):

    kategori = str(
        kategori or "Otomobil"
    ).strip()


    eslesmeler = {

        "Dükkan": "Dukkan",
        "Dükkan/İşyeri": "Dukkan",
        "Dukkan/İşyeri": "Dukkan",
        "İşyeri": "Dukkan",
        "Isyeri": "Dukkan",

    }


    return eslesmeler.get(
        kategori,
        kategori
    )


# =========================================================
# RESİM UZANTISI
# =========================================================

def resim_uzantisi_uygun(
    dosya_adi
):

    uzanti = os.path.splitext(
        dosya_adi or ""
    )[1].lower().lstrip(".")


    return (
        uzanti in
        IZINLI_RESIM_UZANTILARI
    )


# =========================================================
# TÜRKÇE SAYI
# =========================================================

def normalize_onluk_deger(
    deger
):

    if deger is None:
        return None


    metin = str(
        deger
    ).strip()


    if not metin:
        return None


    try:

        if (
            "," in metin
            and "." in metin
        ):

            metin = (
                metin
                .replace(".", "")
                .replace(",", ".")
            )

        elif "," in metin:

            metin = metin.replace(
                ",",
                "."
            )


        return float(metin)


    except (
        TypeError,
        ValueError
    ):

        return None


# =========================================================
# FORM INT
# =========================================================

def form_int(
    alan,
    varsayilan=None
):

    deger = request.form.get(
        alan,
        ""
    ).strip()


    if deger == "":
        return varsayilan


    try:

        return int(deger)

    except (
        TypeError,
        ValueError
    ):

        return varsayilan


# =========================================================
# FORM FLOAT
# =========================================================

def form_float(
    alan,
    varsayilan=None
):

    deger = request.form.get(
        alan,
        ""
    ).strip()


    if deger == "":
        return varsayilan


    sonuc = normalize_onluk_deger(
        deger
    )


    if sonuc is None:
        return varsayilan


    return sonuc


# =========================================================
# FORM TEXT
# =========================================================

def form_text(
    alan,
    varsayilan=""
):

    deger = request.form.get(
        alan
    )


    if deger is None:
        return varsayilan


    return deger.strip()


# =========================================================
# FORM BOOLEAN
# =========================================================

def form_bool(
    alan,
    varsayilan=0
):

    if alan not in request.form:
        return varsayilan


    deger = str(
        request.form.get(
            alan,
            ""
        )
    ).lower().strip()


    return (
        1
        if deger in {
            "1",
            "true",
            "on",
            "evet",
            "yes",
            "var"
        }
        else 0
    )


# =========================================================
# VERİTABANI
# =========================================================

def baglan():

    baglanti = sqlite3.connect(
        DB_YOLU,
        timeout=30
    )


    baglanti.row_factory = (
        sqlite3.Row
    )


    baglanti.execute(
        "PRAGMA foreign_keys = ON"
    )


    baglanti.execute(
        "PRAGMA busy_timeout = 30000"
    )


    return baglanti


# =========================================================
# GİRİŞ
# =========================================================

def giris_yapildi():

    return bool(
        session.get("ad")
    )


# =========================================================
# YÖNETİCİ
# =========================================================

def yonetici_mi():

    kullanici = str(
        session.get(
            "ad",
            ""
        )
    ).lower()


    return (
        kullanici in {
            x.lower()
            for x in SITE_YONETICILERI
        }
    )


# =========================================================
# İLAN YETKİSİ
# =========================================================

def ilan_yetkisi(
    ilan_sahibi
):

    mevcut_kullanici = str(
        session.get(
            "ad",
            ""
        )
    ).lower()


    sahip = str(
        ilan_sahibi or ""
    ).lower()


    return (
        yonetici_mi()
        or
        mevcut_kullanici == sahip
    )


# =========================================================
# TELEFON
# =========================================================

def kullanici_telefonu(
    kullanici_adi
):

    if not kullanici_adi:
        return ""


    baglanti = baglan()


    try:

        satir = baglanti.execute(
            """
            SELECT telefon
            FROM kullanicilar
            WHERE ad=?
            LIMIT 1
            """,
            (
                kullanici_adi,
            )
        ).fetchone()


        if satir:

            return (
                satir["telefon"]
                or ""
            )


        return ""


    finally:

        baglanti.close()


# =========================================================
# FOTOĞRAF ADI
# =========================================================

def fotoğraf_adi_olustur(
    ilan_kodu,
    sira,
    dosya_adi
):

    temiz = secure_filename(
        dosya_adi
    )


    if not temiz:
        temiz = "resim.jpg"


    return (
        f"{ilan_kodu}_"
        f"{sira}_"
        f"{temiz}"
    )


# =========================================================
# FİZİKSEL FOTOĞRAF YOLU
# =========================================================

def dosya_yolu(
    dosya_adi
):

    temiz = os.path.basename(
        str(
            dosya_adi or ""
        )
    )


    return os.path.join(
        UPLOAD_FOLDER,
        temiz
    )


# =========================================================
# FOTOĞRAF URL
# =========================================================

def foto_url(
    dosya_adi
):

    if not dosya_adi:

        return url_for(
            "static",
            filename=(
                "uploads/"
                "varsayilan_araba.jpg"
            )
        )


    if (
        os.path.abspath(
            UPLOAD_FOLDER
        )
        !=
        os.path.abspath(
            YEREL_UPLOAD_FOLDER
        )
    ):

        return url_for(
            "yuklenen_resim",
            dosya_adi=os.path.basename(
                dosya_adi
            )
        )


    return url_for(
        "static",
        filename=(
            "uploads/"
            +
            os.path.basename(
                dosya_adi
            )
        )
    )


# =========================================================
# İLAN KODU
# =========================================================

def yeni_ilan_kodu(
    baglanti,
    kategori
):

    kategori = kategori_normalize(
        kategori
    )


    if kategori not in ILAN_KOD_ON_EKLERI:

        raise ValueError(
            "Geçersiz ilan kategorisi."
        )


    imlec = baglanti.cursor()


    satir = imlec.execute(
        """
        SELECT son_numara
        FROM ilan_sayaclari
        WHERE kategori=?
        LIMIT 1
        """,
        (
            kategori,
        )
    ).fetchone()


    mevcut_numara = (
        int(
            satir["son_numara"]
        )
        if satir
        else 0
    )


    numara = (
        mevcut_numara + 1
    )


    if satir:

        imlec.execute(
            """
            UPDATE ilan_sayaclari
            SET son_numara=?
            WHERE kategori=?
            """,
            (
                numara,
                kategori
            )
        )

    else:

        imlec.execute(
            """
            INSERT INTO ilan_sayaclari
            (
                kategori,
                son_numara
            )
            VALUES (?, ?)
            """,
            (
                kategori,
                numara
            )
        )


    return (
        ILAN_KOD_ON_EKLERI[kategori]
        + "-"
        + f"{numara:06d}"
    )


# =========================================================
# FOTOĞRAFLARI KAYDET
# =========================================================

def fotoğrafları_kaydet(
    baglanti,
    ilan_id,
    ilan_kodu,
    dosyalar
):

    imlec = baglanti.cursor()


    satir = imlec.execute(
        """
        SELECT
            COALESCE(MAX(sira), 0) AS son_sira
        FROM ilan_resimleri
        WHERE ilan_id=?
        """,
        (
            ilan_id,
        )
    ).fetchone()


    mevcut_sira = int(
        satir["son_sira"]
        or 0
    )


    kaydedilen = []


    for dosya in (
        dosyalar or []
    ):

        if mevcut_sira >= MAX_FOTO:
            break


        if not dosya:
            continue


        if not dosya.filename:
            continue


        if not resim_uzantisi_uygun(
            dosya.filename
        ):
            continue


        yeni_sira = (
            mevcut_sira + 1
        )


        dosya_adi = (
            fotoğraf_adi_olustur(
                ilan_kodu,
                yeni_sira,
                dosya.filename
            )
        )


        yol = dosya_yolu(
            dosya_adi
        )


        try:

            dosya.save(
                yol
            )


            imlec.execute(
                """
                INSERT INTO ilan_resimleri
                (
                    ilan_id,
                    dosya_adi,
                    sira,
                    kapak
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    ilan_id,
                    dosya_adi,
                    yeni_sira,
                    1
                    if yeni_sira == 1
                    else 0
                )
            )


            mevcut_sira = (
                yeni_sira
            )


            kaydedilen.append(
                dosya_adi
            )


        except Exception:

            try:

                if os.path.exists(yol):
                    os.remove(yol)

            except OSError:
                pass


            raise


    return kaydedilen


# =========================================================
# İLAN SAHİBİ TELEFONU
# =========================================================

def kullanici_icin_ilan_sahibi_telefonu(
    ilan
):

    telefon = str(
        ilan.get(
            "telefon",
            ""
        )
        or ""
    ).strip()


    if not telefon:

        telefon = (
            kullanici_telefonu(
                ilan.get(
                    "ilan_sahibi",
                    ""
                )
            )
        )


    return telefon


# =========================================================
# GLOBAL DEĞİŞKENLER
# =========================================================

@app.context_processor
def global_sablon_degiskenleri():

    return {

        "UYE_GIRIS_YAPTI_MI":
            giris_yapildi(),

        "AKTIF_KULLANICI":
            session.get(
                "ad",
                ""
            ),

        "KATEGORILER":
            KATEGORILER,

        "MAX_FOTO":
            MAX_FOTO,

        "RESIMLER_KALICI":
            (
                os.path.abspath(
                    UPLOAD_FOLDER
                )
                !=
                os.path.abspath(
                    YEREL_UPLOAD_FOLDER
                )
            )
    }


# =========================================================
# KALICI FOTOĞRAF SERVİSİ
# =========================================================

@app.route(
    "/uploads/<path:dosya_adi>"
)
def yuklenen_resim(
    dosya_adi
):

    temiz = os.path.basename(
        dosya_adi
    )


    return send_from_directory(
        UPLOAD_FOLDER,
        temiz
    )


# =========================================================
# İLAN GETİR
# =========================================================

def ilan_getir(
    ilan_id
):

    baglanti = baglan()
    imlec = baglanti.cursor()


    try:

        satir = imlec.execute(
            """
            SELECT *
            FROM ilanlar
            WHERE id=?
            LIMIT 1
            """,
            (
                ilan_id,
            )
        ).fetchone()


        if not satir:
            return None


        ilan = dict(satir)


        kategori = kategori_normalize(
            ilan.get(
                "kategori",
                ""
            )
        )


        ilan["kategori"] = kategori


        # =====================================================
        # VARSAYILAN ALANLAR
        # =====================================================

        varsayilanlar = {

            "detay": {},
            "otomobil": None,
            "emlak": None,
            "isyeri": None,
            "arsa": None,

            "marka": "",
            "model": "",
            "yil": None,
            "km": None,
            "yakit": "",
            "vites": "",
            "kasa_tipi": "",
            "motor_hacmi": "",
            "motor_gucu": "",
            "cekis": "",
            "renk": "",
            "hasar_durumu": "",
            "degisen": 0,
            "boya": 0,
            "tramer": 0,
            "takas": 0,
            "kredi_uygun": 0,

            "bina_tipi": "",
            "emlak_tipi": "",
            "ilan_durumu": "",
            "metrekare": None,
            "oda_sayisi": "",
            "salon_sayisi": "",
            "bina_yasi": None,
            "bulundugu_kat": "",
            "toplam_kat": None,
            "isitma": "",
            "banyo_sayisi": None,
            "balkon": 0,
            "asansor": 0,
            "otopark": 0,
            "esyali": 0,
            "site_icerisinde": 0,
            "aidat": None,
            "kredi_uygun_emlak": 0,
            "tapu_durumu": "",
            "kullanim_durumu": "",
            "takas_emlak": 0,

            "isyeri_tipi": "",
            "isyeri_ilan_durumu": "",
            "isyeri_metrekare": None,
            "isyeri_bina_yasi": None,
            "isyeri_oda_sayisi": "",
            "isyeri_kat": "",
            "isyeri_toplam_kat": None,
            "isyeri_isitma": "",
            "isyeri_banyo": 0,
            "isyeri_mutfak": 0,
            "isyeri_depo": 0,
            "isyeri_vitrin": 0,
            "isyeri_cephe": "",
            "isyeri_asansor": 0,
            "isyeri_otopark": 0,
            "isyeri_aidat": None,
            "kredi_uygun_isyeri": 0,
            "isyeri_tapu_durumu": "",
            "isyeri_kullanim_durumu": "",
            "takas_isyeri": 0,

            "imar_durumu": "",
            "arsa_ilan_durumu": "",
            "arsa_metrekare": None,
            "metrekare_arsa": None,
            "ada_no": "",
            "parsel_no": "",
            "arsa_tapu_durumu": "",
            "kredi_uygun_arsa": 0,
            "takas_arsa": 0,
            "kat_karsiligi": 0,
            "ifrazli": 0,
            "kaks": "",
            "emsal": "",
            "gabari": "",
            "arsa_cephe": "",
            "yol_durumu": "",
            "elektrik": 0,
            "su": 0,
            "kanalizasyon": 0,
            "dogalgaz": 0,
            "kadastro_yolu": 0,
            "merkeze_uzaklik": "",

            "tapu_hazir": 0
        }


        for anahtar, deger in varsayilanlar.items():

            ilan.setdefault(
                anahtar,
                deger
            )


        # =====================================================
        # DETAY GETİR
        # =====================================================

        def detay_getir(tablo):

            satir_detay = imlec.execute(
                f"""
                SELECT *
                FROM {tablo}
                WHERE ilan_id=?
                LIMIT 1
                """,
                (
                    ilan_id,
                )
            ).fetchone()


            if not satir_detay:
                return None


            return dict(
                satir_detay
            )


        # =====================================================
        # OTOMOBİL
        # =====================================================

        if kategori == "Otomobil":

            detay = detay_getir(
                "otomobil_detay"
            )


            if detay:

                ilan["detay"] = detay
                ilan["otomobil"] = detay


                for alan in [
                    "marka",
                    "model",
                    "yakit",
                    "vites",
                    "kasa_tipi",
                    "motor_hacmi",
                    "motor_gucu",
                    "cekis",
                    "renk",
                    "hasar_durumu"
                ]:

                    ilan[alan] = (
                        detay.get(
                            alan,
                            ""
                        )
                        or ""
                    )


                for alan in [
                    "yil",
                    "km"
                ]:

                    ilan[alan] = detay.get(
                        alan
                    )


                for alan in [
                    "degisen",
                    "boya",
                    "tramer",
                    "takas",
                    "kredi_uygun"
                ]:

                    ilan[alan] = (
                        detay.get(
                            alan,
                            0
                        )
                        or 0
                    )


        # =====================================================
        # DAİRE / EV
        # =====================================================

        elif kategori in {
            "Daire",
            "Ev"
        }:

            detay = detay_getir(
                "emlak_detay"
            )


            if detay:

                ilan["detay"] = detay
                ilan["emlak"] = detay


                ilan["emlak_tipi"] = (
                    detay.get(
                        "emlak_tipi",
                        ""
                    )
                    or ""
                )


                ilan["bina_tipi"] = (
                    ilan["emlak_tipi"]
                )


                for alan in [
                    "ilan_durumu",
                    "bulundugu_kat",
                    "isitma",
                    "oda_sayisi",
                    "salon_sayisi",
                    "tapu_durumu",
                    "kullanim_durumu"
                ]:

                    ilan[alan] = (
                        detay.get(
                            alan,
                            ""
                        )
                        or ""
                    )


                for alan in [
                    "metrekare",
                    "aidat"
                ]:

                    ilan[alan] = (
                        detay.get(
                            alan
                        )
                    )


                for alan in [
                    "bina_yasi",
                    "toplam_kat",
                    "banyo_sayisi"
                ]:

                    ilan[alan] = (
                        detay.get(
                            alan
                        )
                    )


                for alan in [
                    "balkon",
                    "asansor",
                    "otopark",
                    "esyali",
                    "site_icerisinde"
                ]:

                    ilan[alan] = (
                        detay.get(
                            alan,
                            0
                        )
                        or 0
                    )


                ilan["kredi_uygun_emlak"] = (
                    detay.get(
                        "kredi_uygun",
                        0
                    )
                    or 0
                )


                ilan["kredi_uygun"] = (
                    detay.get(
                        "kredi_uygun",
                        0
                    )
                    or 0
                )


                ilan["takas_emlak"] = (
                    detay.get(
                        "takas",
                        0
                    )
                    or 0
                )


                ilan["takas"] = (
                    detay.get(
                        "takas",
                        0
                    )
                    or 0
                )


        # =====================================================
        # DÜKKAN
        # =====================================================

        elif kategori == "Dukkan":

            detay = detay_getir(
                "isyeri_detay"
            )


            if detay:

                ilan["detay"] = detay
                ilan["isyeri"] = detay


                ilan["isyeri_tipi"] = (
                    detay.get(
                        "isyeri_tipi",
                        ""
                    )
                    or ""
                )


                ilan["isyeri_ilan_durumu"] = (
                    detay.get(
                        "ilan_durumu",
                        ""
                    )
                    or ""
                )


                alan_eslesmeleri = {

                    "metrekare":
                        "isyeri_metrekare",

                    "bina_yasi":
                        "isyeri_bina_yasi",

                    "oda_sayisi":
                        "isyeri_oda_sayisi",

                    "bulundugu_kat":
                        "isyeri_kat",

                    "toplam_kat":
                        "isyeri_toplam_kat",

                    "isitma":
                        "isyeri_isitma",

                    "banyo":
                        "isyeri_banyo",

                    "mutfak":
                        "isyeri_mutfak",

                    "depo":
                        "isyeri_depo",

                    "vitrin":
                        "isyeri_vitrin",

                    "cephe":
                        "isyeri_cephe",

                    "asansor":
                        "isyeri_asansor",

                    "otopark":
                        "isyeri_otopark",

                    "aidat":
                        "isyeri_aidat",

                    "tapu_durumu":
                        "isyeri_tapu_durumu",

                    "kullanim_durumu":
                        "isyeri_kullanim_durumu"
                }


                for kaynak, hedef in alan_eslesmeleri.items():

                    deger = detay.get(
                        kaynak
                    )


                    ilan[hedef] = (
                        deger
                        if deger is not None
                        else ""
                    )


                ilan["kredi_uygun_isyeri"] = (
                    detay.get(
                        "kredi_uygun",
                        0
                    )
                    or 0
                )


                ilan["takas_isyeri"] = (
                    detay.get(
                        "takas",
                        0
                    )
                    or 0
                )


                ilan["kredi_uygun"] = (
                    detay.get(
                        "kredi_uygun",
                        0
                    )
                    or 0
                )


                ilan["takas"] = (
                    detay.get(
                        "takas",
                        0
                    )
                    or 0
                )


                ilan["isitma"] = (
                    ilan["isyeri_isitma"]
                )


                ilan["tapu_hazir"] = (
                    1
                    if str(
                        detay.get(
                            "tapu_durumu",
                            ""
                        )
                    ).strip()
                    else 0
                )


        # =====================================================
        # ARSA / TARLA
        # =====================================================

        elif kategori in {
            "Arsa",
            "Tarla"
        }:

            detay = detay_getir(
                "arsa_detay"
            )


            if detay:

                ilan["detay"] = detay
                ilan["arsa"] = detay


                ilan["arsa_ilan_durumu"] = (
                    detay.get(
                        "ilan_durumu",
                        ""
                    )
                    or ""
                )


                ilan["imar_durumu"] = (
                    detay.get(
                        "imar_durumu",
                        ""
                    )
                    or ""
                )


                ilan["arsa_metrekare"] = (
                    detay.get(
                        "metrekare"
                    )
                )


                ilan["metrekare_arsa"] = (
                    detay.get(
                        "metrekare"
                    )
                )


                for alan in [
                    "ada_no",
                    "parsel_no",
                    "kaks",
                    "emsal",
                    "gabari",
                    "yol_durumu",
                    "merkeze_uzaklik"
                ]:

                    ilan[alan] = (
                        detay.get(
                            alan,
                            ""
                        )
                        or ""
                    )


                ilan["arsa_tapu_durumu"] = (
                    detay.get(
                        "tapu_durumu",
                        ""
                    )
                    or ""
                )


                ilan["arsa_cephe"] = (
                    detay.get(
                        "cephe",
                        ""
                    )
                    or ""
                )


                ilan["kredi_uygun_arsa"] = (
                    detay.get(
                        "kredi_uygun",
                        0
                    )
                    or 0
                )


                ilan["takas_arsa"] = (
                    detay.get(
                        "takas",
                        0
                    )
                    or 0
                )


                ilan["kredi_uygun"] = (
                    detay.get(
                        "kredi_uygun",
                        0
                    )
                    or 0
                )


                ilan["takas"] = (
                    detay.get(
                        "takas",
                        0
                    )
                    or 0
                )


                for alan in [
                    "kat_karsiligi",
                    "ifrazli",
                    "elektrik",
                    "su",
                    "kanalizasyon",
                    "dogalgaz",
                    "kadastro_yolu"
                ]:

                    ilan[alan] = (
                        detay.get(
                            alan,
                            0
                        )
                        or 0
                    )


                # -------------------------------------------------
                # TARLA İÇİN ARSA'YA ÖZGÜ ALANLARI GİZLE
                # -------------------------------------------------

                if kategori == "Tarla":

                    ilan["imar_durumu"] = ""
                    ilan["ada_no"] = ""
                    ilan["parsel_no"] = ""
                    ilan["kaks"] = ""
                    ilan["emsal"] = ""
                    ilan["gabari"] = ""
                    ilan["arsa_cephe"] = ""
                    ilan["kat_karsiligi"] = 0


        # =====================================================
        # FOTOĞRAFLAR
        # =====================================================

        resimler = [

            dict(x)

            for x in imlec.execute(
                """
                SELECT *
                FROM ilan_resimleri
                WHERE ilan_id=?
                ORDER BY
                    CASE
                        WHEN kapak=1 THEN 0
                        ELSE 1
                    END,
                    sira ASC,
                    id ASC
                """,
                (
                    ilan_id,
                )
            ).fetchall()
        ]


        ilan["resimler_liste"] = (
            resimler
        )


        ilan["resimler"] = [

            x.get(
                "dosya_adi",
                ""
            )

            for x in resimler

            if x.get(
                "dosya_adi"
            )
        ]


        if resimler:

            kapak = next(

                (
                    x
                    for x in resimler
                    if int(
                        x.get(
                            "kapak",
                            0
                        )
                        or 0
                    ) == 1
                ),

                resimler[0]
            )


            ilan["resim"] = (
                kapak.get(
                    "dosya_adi",
                    ""
                )
                or ""
            )

        else:

            ilan["resim"] = (
                "varsayilan_araba.jpg"
            )


        ilan["resim_url"] = (
            foto_url(
                ilan["resim"]
            )
        )


        for resim in ilan["resimler_liste"]:

            resim["url"] = (
                foto_url(
                    resim.get(
                        "dosya_adi",
                        ""
                    )
                )
            )


        # =====================================================
        # UYUMLULUK ALANLARI
        # =====================================================

        ilan["kod"] = (
            ilan.get(
                "ilan_kodu",
                ""
            )
            or ""
        )


        ilan["ad"] = (
            ilan.get(
                "baslik",
                ""
            )
            or ""
        )


        ilan["yil_oto"] = (
            ilan.get(
                "yil"
            )
        )


        ilan["km_oto"] = (
            ilan.get(
                "km"
            )
        )


        # =====================================================
        # TELEFON
        # =====================================================

        ilan["musteri_telefon"] = (
            kullanici_icin_ilan_sahibi_telefonu(
                ilan
            )
        )


        # Telefon giriş yapılmamış kullanıcıya verilmez.
        if not giris_yapildi():

            ilan["telefon"] = ""
            ilan["musteri_telefon"] = ""


        return ilan


    finally:

        baglanti.close()


# =========================================================
# ANA SAYFA
# =========================================================

@app.route("/")
def hello_world():

    return render_template(
        "index.html"
    )


# =========================================================
# KURUMSAL
# =========================================================

@app.route("/kurumsal")
def kurumsal_sayfasi():

    return render_template(
        "kurumsal.html"
    )


# =========================================================
# MAHİR
# =========================================================

@app.route("/mahir")
def mahirin_sayfasi():

    return render_template(
        "mahir.html"
    )


# =========================================================
# LOGIN SAYFASI
# =========================================================
# =========================================================
# LOGIN SAYFASI
# =========================================================

@app.route("/login")
def login():

    return render_template(
        "login.html"
    )


# =========================================================
# LOGIN KONTROL
# =========================================================

@app.route(
    "/loginbilgileri",
    methods=["POST"]
)
def login_kontrol():

    giris = request.form.get(
        "isim",
        ""
    ).strip()

    sifre = request.form.get(
        "sifre",
        ""
    )

    baglanti = baglan()

    try:

        kullanici = baglanti.execute(
            """
            SELECT *
            FROM kullanicilar
            WHERE
                (
                    ad=?
                    OR telefon=?
                    OR LOWER(email)=?
                )
                AND sifre=?
            LIMIT 1
            """,
            (
                giris,
                giris,
                giris.lower(),
                sifre
            )
        ).fetchone()

    finally:

        baglanti.close()

    if not kullanici:

        return render_template(
            "login.html",
            hata="Kullanıcı bilgileri hatalı."
        )

    session.clear()

    session["ad"] = (
        kullanici["ad"]
    )

    return redirect("/")


# =========================================================
# ÇIKIŞ
# =========================================================

@app.route("/cikis")
def cikis():

    session.clear()

    return redirect("/")


# =========================================================
# ŞİFREMİ UNUTTUM SAYFASI
# =========================================================

@app.route("/sifremi-unuttum")
def sifremi_unuttum():

    return render_template(
        "sifremi_unuttum.html"
    )


# =========================================================
# ŞİFRE TOKEN OLUŞTUR
# =========================================================

def sifre_tokeni_olustur(email):

    token = secrets.token_urlsafe(
        32
    )

    sure = (
        datetime.datetime.now()
        +
        datetime.timedelta(
            minutes=30
        )
    )

    baglanti = baglan()

    try:

        kullanici = baglanti.execute(
            """
            SELECT id
            FROM kullanicilar
            WHERE LOWER(email)=?
            LIMIT 1
            """,
            (
                email.lower(),
            )
        ).fetchone()

        if not kullanici:

            return None

        baglanti.execute(
            """
            UPDATE kullanicilar
            SET
                sifre_token=?,
                token_suresi=?
            WHERE id=?
            """,
            (
                token,
                sure.isoformat(
                    timespec="seconds"
                ),
                kullanici["id"]
            )
        )

        baglanti.commit()

        return token

    except Exception as hata:

        baglanti.rollback()

        print(
            "ŞİFRE TOKEN HATASI:",
            hata
        )

        raise

    finally:

        baglanti.close()


# =========================================================
# ŞİFRE YENİLEME BAĞLANTISI GÖNDER
# =========================================================

@app.route(
    "/sifremi-unuttum-gonder",
    methods=["POST"]
)
def sifremi_unuttum_gonder():

    email = request.form.get(
        "email",
        ""
    ).strip().lower()

    if not email:

        return render_template(
            "sifremi_unuttum.html",
            hata=(
                "Lütfen e-posta adresinizi girin."
            )
        )

    token = sifre_tokeni_olustur(
        email
    )

    if not token:

        return render_template(
            "sifremi_unuttum.html",
            hata=(
                "Bu e-posta adresiyle kayıtlı "
                "bir kullanıcı bulunamadı."
            )
        )

    link = (
        request.host_url.rstrip("/")
        +
        url_for(
            "sifre_yenile",
            token=token
        )
    )

    print()
    print(
        "=========================================="
    )
    print(
        "ŞİFRE YENİLEME BAĞLANTISI"
    )
    print(
        "=========================================="
    )
    print(
        link
    )
    print(
        "=========================================="
    )
    print()

    return render_template(
        "sifremi_unuttum.html",
        basarili=(
            "Şifre yenileme bağlantısı oluşturuldu. "
            "Geliştirme aşamasında bağlantı "
            "sunucu terminalinde gösterildi."
        )
    )


# =========================================================
# ESKİ ŞİFRE LİNKİ ROUTE'U
# =========================================================
# Eski formlar veya eski bağlantılar için uyumluluk sağlar.

@app.route(
    "/sifre_linki",
    methods=["POST"]
)
def sifre_linki():

    return sifremi_unuttum_gonder()


# =========================================================
# ŞİFRE YENİLEME SAYFASI
# =========================================================
# =========================================================
# ŞİFRE YENİLEME SAYFASI
# =========================================================

@app.route("/sifre_yenile/<token>", methods=["GET"])
def sifre_yenile(token):

    print()
    print("==========================================")
    print("ŞİFRE YENİLEME İSTEĞİ GELDİ")
    print("TOKEN:")
    print(token)
    print("==========================================")

    baglanti = baglan()

    try:

        kullanici = baglanti.execute(
            """
            SELECT
                id,
                email,
                token_suresi
            FROM kullanicilar
            WHERE sifre_token=?
            LIMIT 1
            """,
            (token,)
        ).fetchone()

    except Exception as hata:

        print("VERİTABANI SORGUSU HATASI:")
        print(repr(hata))

        return (
            "Şifre yenileme sırasında veritabanı hatası oluştu.",
            500
        )

    finally:

        baglanti.close()

    if not kullanici:

        print("TOKEN BULUNAMADI.")

        return (
            "Geçersiz veya kullanılmış şifre yenileme bağlantısı.",
            400
        )

    print("TOKEN SAHİBİ:")
    print(kullanici["email"])
    print("TOKEN SÜRESİ:")
    print(kullanici["token_suresi"])

    if not kullanici["token_suresi"]:

        return (
            "Şifre yenileme bağlantısı geçersiz.",
            400
        )

    try:

        son_tarih = datetime.datetime.fromisoformat(
            kullanici["token_suresi"]
        )

    except (
        TypeError,
        ValueError
    ) as hata:

        print("TOKEN TARİH HATASI:")
        print(repr(hata))

        return (
            "Şifre yenileme bağlantısı geçersiz.",
            400
        )

    simdi_tarih = datetime.datetime.now()

    print("ŞİMDİ:")
    print(simdi_tarih)

    print("SON TARİH:")
    print(son_tarih)

    if simdi_tarih > son_tarih:

        print("TOKEN SÜRESİ DOLMUŞ.")

        return (
            "Şifre yenileme bağlantısının süresi dolmuş.",
            400
        )

    print("TOKEN GEÇERLİ.")

    try:

        return render_template(
            "sifre_yenile.html",
            token=token
        )

    except Exception as hata:

        import traceback

        print()
        print("==========================================")
        print("ŞİFRE YENİLEME HTML HATASI")
        print("==========================================")

        traceback.print_exc()

        print("==========================================")
        print()

        return (
            "Şifre yenileme sayfası oluşturulamadı. "
            "Ayrıntı terminaldedir.",
            500
        )

# =========================================================
# ŞİFRE DEĞİŞTİR
# =========================================================

@app.route(
    "/sifre_degistir",
    methods=["POST"]
)
def sifre_degistir():

    token = request.form.get(
        "token",
        ""
    ).strip()

    sifre = request.form.get(
        "sifre",
        ""
    )

    if not token:

        return (
            "Geçersiz şifre yenileme bağlantısı.",
            400
        )

    if not sifre:

        return (
            "Şifre boş bırakılamaz.",
            400
        )

    if len(sifre) < 4:

        return (
            "Şifre en az 4 karakter olmalıdır.",
            400
        )

    baglanti = baglan()

    try:

        kullanici = baglanti.execute(
            """
            SELECT
                id,
                token_suresi
            FROM kullanicilar
            WHERE sifre_token=?
            LIMIT 1
            """,
            (
                token,
            )
        ).fetchone()

        if not kullanici:

            return (
                "Geçersiz veya kullanılmış "
                "şifre yenileme bağlantısı.",
                400
            )

        token_suresi = (
            kullanici["token_suresi"]
        )

        if not token_suresi:

            return (
                "Şifre yenileme bağlantısı geçersiz.",
                400
            )

        try:

            son_tarih = (
                datetime.datetime.fromisoformat(
                    token_suresi
                )
            )

        except (
            TypeError,
            ValueError
        ):

            return (
                "Şifre yenileme bağlantısı geçersiz.",
                400
            )

        if datetime.datetime.now() > son_tarih:

            return (
                "Şifre yenileme bağlantısının süresi dolmuş.",
                400
            )

        baglanti.execute(
            """
            UPDATE kullanicilar
            SET
                sifre=?,
                sifre_token=NULL,
                token_suresi=NULL
            WHERE id=?
            """,
            (
                sifre,
                kullanici["id"]
            )
        )

        baglanti.commit()

    except Exception as hata:

        baglanti.rollback()

        print(
            "ŞİFRE DEĞİŞTİRME HATASI:",
            hata
        )

        return (
            "Şifre değiştirilemedi.",
            500
        )

    finally:

        baglanti.close()

    flash(
        "Şifreniz başarıyla değiştirildi. "
        "Yeni şifrenizle giriş yapabilirsiniz."
    )

    return redirect(
        url_for("login")
    )


# =========================================================
# KAYDOL
# =========================================================

@app.route("/kaydol")
def kaydol():

    return render_template(
        "kaydol.html"
    )


# =========================================================
# KAYIT
# =========================================================

@app.route(
    "/kayitbilgileri",
    methods=["POST"]
)
def kayit():

    isim = request.form.get(
        "isim",
        ""
    ).strip()

    email = request.form.get(
        "email",
        ""
    ).strip().lower()

    sifre = request.form.get(
        "sifre",
        ""
    )

    telefon = request.form.get(
        "telefon",
        ""
    ).strip()

    sozlesme_onay = request.form.get(
        "sozlesme_onay"
    )

    if (
        not isim
        or not email
        or not sifre
        or not telefon
    ):

        return render_template(
            "kaydol.html",
            hata=(
                "Lütfen tüm alanları eksiksiz doldurun."
            )
        )

    if (
        not telefon.isdigit()
        or len(telefon) != 11
        or not telefon.startswith("0")
    ):

        return render_template(
            "kaydol.html",
            hata=(
                "Telefon numarası 0 ile başlayan "
                "11 haneli olmalıdır."
            )
        )

    if sozlesme_onay != "onaylandi":

        return render_template(
            "kaydol.html",
            hata=(
                "Üyelik sözleşmesini onaylamanız gerekiyor."
            )
        )

    baglanti = baglan()

    try:

        if baglanti.execute(
            """
            SELECT id
            FROM kullanicilar
            WHERE ad=?
            LIMIT 1
            """,
            (
                isim,
            )
        ).fetchone():

            return render_template(
                "kaydol.html",
                hata="Bu kullanıcı adı zaten kayıtlı."
            )

        if baglanti.execute(
            """
            SELECT id
            FROM kullanicilar
            WHERE LOWER(email)=?
            LIMIT 1
            """,
            (
                email,
            )
        ).fetchone():

            return render_template(
                "kaydol.html",
                hata="Bu e-posta adresi zaten kayıtlı."
            )

        if baglanti.execute(
            """
            SELECT id
            FROM kullanicilar
            WHERE telefon=?
            LIMIT 1
            """,
            (
                telefon,
            )
        ).fetchone():

            return render_template(
                "kaydol.html",
                hata="Bu telefon numarası zaten kayıtlı."
            )

        tarih = datetime.datetime.now()

        baglanti.execute(
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
            VALUES (
                ?,
                ?,
                ?,
                ?,
                NULL,
                NULL,
                ?
            )
            """,
            (
                isim,
                email,
                sifre,
                telefon,
                tarih.isoformat(
                    timespec="seconds"
                )
            )
        )

        bitis = (
            tarih
            +
            datetime.timedelta(
                days=30
            )
        )

        baglanti.execute(
            """
            INSERT OR REPLACE INTO abonelikler
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
                isim,
                tarih.isoformat(
                    timespec="seconds"
                ),
                bitis.isoformat(
                    timespec="seconds"
                ),
                tarih.isoformat(
                    timespec="seconds"
                )
            )
        )

        baglanti.commit()

        session.clear()
        session["ad"] = isim

        return redirect("/")

    except sqlite3.IntegrityError:

        baglanti.rollback()

        return render_template(
            "kaydol.html",
            hata=(
                "Bu bilgiler daha önce kayıt edilmiş olabilir."
            )
        )

    finally:

        baglanti.close()


# =========================================================
# BURADAN SONRA MEVCUT KODUNUZ AYNI KALACAK
# =========================================================
# =========================================================
# ABONELİK GETİR
# =========================================================

def abonelik_getir(
    kullanici_adi
):

    if not kullanici_adi:
        return None


    baglanti = baglan()


    try:

        satir = baglanti.execute(
            """
            SELECT *
            FROM abonelikler
            WHERE kullanici_adi=?
            LIMIT 1
            """,
            (
                kullanici_adi,
            )
        ).fetchone()


        if not satir:

            baslangic = datetime.datetime.now()


            bitis = (
                baslangic
                +
                datetime.timedelta(
                    days=30
                )
            )


            baglanti.execute(
                """
                INSERT OR IGNORE INTO abonelikler
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


            baglanti.commit()


            satir = baglanti.execute(
                """
                SELECT *
                FROM abonelikler
                WHERE kullanici_adi=?
                LIMIT 1
                """,
                (
                    kullanici_adi,
                )
            ).fetchone()


        if not satir:
            return None


        abonelik = dict(satir)


        try:

            bitis = datetime.datetime.fromisoformat(
                abonelik["bitis_tarihi"]
            )


            aktif = (
                abonelik["durum"] == "aktif"
                and
                datetime.datetime.now() < bitis
            )


        except (
            TypeError,
            ValueError
        ):

            aktif = False


        if (
            not aktif
            and
            abonelik["durum"] == "aktif"
        ):

            baglanti.execute(
                """
                UPDATE abonelikler
                SET durum='suresi_doldu'
                WHERE kullanici_adi=?
                """,
                (
                    kullanici_adi,
                )
            )


            baglanti.commit()


            abonelik["durum"] = (
                "suresi_doldu"
            )


        abonelik["aktif"] = aktif


        return abonelik


    finally:

        baglanti.close()


# =========================================================
# ABONELİK SAYFASI
# =========================================================

@app.route("/abonelik")
def abonelik_sayfasi():

    if not giris_yapildi():

        return redirect(
            url_for("kaydol")
        )


    return render_template(
        "abonelik.html",
        paketler=ABONELIK_PAKETLERI,
        abonelik=abonelik_getir(
            session["ad"]
        )
    )


# =========================================================
# DEMO ABONELİK
# =========================================================

@app.route(
    "/abonelik/demo-aktif-et",
    methods=["POST"]
)
def abonelik_demo_aktif_et():

    if not giris_yapildi():

        return redirect(
            url_for("kaydol")
        )


    paket = request.form.get(
        "paket",
        ""
    ).strip()


    if (
        paket not in ABONELIK_PAKETLERI
        or paket == "Ucretsiz"
    ):

        flash(
            "Geçersiz abonelik paketi."
        )


        return redirect(
            url_for("abonelik_sayfasi")
        )


    bilgi = (
        ABONELIK_PAKETLERI[paket]
    )


    baslangic = datetime.datetime.now()


    bitis = (
        baslangic
        +
        datetime.timedelta(
            days=bilgi["gun"]
        )
    )


    baglanti = baglan()


    try:

        baglanti.execute(
            """
            INSERT OR REPLACE INTO abonelikler
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
                ?,
                'aktif',
                ?,
                ?,
                ?
            )
            """,
            (
                session["ad"],
                paket,
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


        baglanti.commit()


    finally:

        baglanti.close()


    flash(
        "Demo abonelik etkinleştirildi. "
        "Gerçek ödeme alınmamıştır."
    )


    return redirect(
        url_for("abonelik_sayfasi")
    )


# =========================================================
# İLAN YÖNETİMİ
# =========================================================

@app.route("/urunler")
def urunler():

    if not giris_yapildi():

        return redirect("/login")


    ham_kategori = request.args.get(
        "kategori",
        ""
    ).strip()


    kategori = (
        kategori_normalize(
            ham_kategori
        )
        if ham_kategori
        else ""
    )


    kullanici = session["ad"]


    baglanti = baglan()


    try:

        sorgu = """
            SELECT *
            FROM ilanlar
            WHERE aktif=1
        """


        parametreler = []


        if not yonetici_mi():

            sorgu += """
                AND LOWER(ilan_sahibi)=?
            """


            parametreler.append(
                kullanici.lower()
            )


        if (
            kategori
            and
            kategori in KATEGORILER
        ):

            sorgu += """
                AND kategori=?
            """


            parametreler.append(
                kategori
            )


        sorgu += """
            ORDER BY id DESC
        """


        ilanlar = [

            dict(x)

            for x in (
                baglanti.execute(
                    sorgu,
                    tuple(parametreler)
                ).fetchall()
            )
        ]


    finally:

        baglanti.close()


    for ilan in ilanlar:

        tam_ilan = ilan_getir(
            ilan["id"]
        )


        if tam_ilan:

            ilan.update(
                tam_ilan
            )


    return render_template(
        "urunler.html",
        urunler=ilanlar,
        ilanlar=ilanlar,
        yoneticiler=SITE_YONETICILERI,
        secilen_kategori=kategori
    )


# =========================================================
# YENİ İLAN SAYFASI
# =========================================================

@app.route("/urun_ekle_sayfa")
def urun_ekle_sayfa():

    if not giris_yapildi():

        return redirect("/login")


    return render_template(
        "urun_ekle.html",
        ilan_kodu_atandi=(
            request.args.get(
                "kod",
                ""
            ).strip()
        )
    )


# =========================================================
# YENİ İLAN EKLE
# =========================================================

@app.route(
    "/urun_ekle",
    methods=["POST"]
)
def urun_ekle():

    if not giris_yapildi():

        return redirect(
            url_for("login")
        )


    kategori = kategori_normalize(
        request.form.get(
            "kategori",
            "Otomobil"
        )
    )


    if kategori not in KATEGORILER:

        return (
            "Geçersiz ilan kategorisi.",
            400
        )


    baslik = request.form.get(
        "ad",
        ""
    ).strip()


    aciklama = request.form.get(
        "aciklama"
    )


    if aciklama is None:

        aciklama = request.form.get(
            "acıklama",
            ""
        )


    aciklama = (
        aciklama
        or ""
    ).strip()


    if not baslik:

        return render_template(
            "urun_ekle.html",
            hata="İlan başlığı boş bırakılamaz.",
            ilan_kodu_atandi=""
        )


    fiyat = (
        normalize_onluk_deger(
            request.form.get(
                "fiyat",
                "0"
            )
        )
        or 0
    )


    fiyat = max(
        fiyat,
        0
    )


    baglanti = baglan()
    fiziksel_dosyalar = []


    try:

        tarih = simdi()


        ilan_kodu = yeni_ilan_kodu(
            baglanti,
            kategori
        )


        ilan_sahibi = (
            session.get(
                "ad",
                ""
            ).strip()
        )


        telefon = kullanici_telefonu(
            ilan_sahibi
        )


        imlec = baglanti.cursor()


        # =====================================================
        # ANA İLAN
        # =====================================================

        imlec.execute(
            """
            INSERT INTO ilanlar
            (
                ilan_kodu,
                kategori,
                baslik,
                fiyat,
                aciklama,
                ilan_sahibi,
                telefon,
                aktif,
                olusturma_tarihi,
                guncelleme_tarihi
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
            """,
            (
                ilan_kodu,
                kategori,
                baslik,
                fiyat,
                aciklama,
                ilan_sahibi,
                telefon,
                tarih,
                tarih
            )
        )


        ilan_id = imlec.lastrowid


        # =====================================================
        # OTOMOBİL
        # =====================================================

        if kategori == "Otomobil":

            imlec.execute(
                """
                INSERT INTO otomobil_detay
                (
                    ilan_id,
                    marka,
                    model,
                    yil,
                    km,
                    yakit,
                    vites,
                    kasa_tipi,
                    motor_hacmi,
                    motor_gucu,
                    cekis,
                    renk,
                    hasar_durumu,
                    degisen,
                    boya,
                    tramer,
                    takas,
                    kredi_uygun
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?
                )
                """,
                (
                    ilan_id,
                    form_text("marka"),
                    form_text("model"),
                    form_int(
                        "yil",
                        form_int("yil_oto")
                    ),
                    form_int(
                        "km",
                        form_int("km_oto")
                    ),
                    form_text("yakit"),
                    form_text("vites"),
                    form_text("kasa_tipi"),
                    form_text("motor_hacmi"),
                    form_text("motor_gucu"),
                    form_text("cekis"),
                    form_text("renk"),
                    form_text("hasar_durumu"),
                    form_bool("degisen"),
                    form_bool("boya"),
                    form_bool("tramer"),
                    form_bool("takas"),
                    form_bool("kredi_uygun")
                )
            )


        # =====================================================
        # DAİRE / EV
        # =====================================================

        elif kategori in {
            "Daire",
            "Ev"
        }:

            imlec.execute(
                """
                INSERT INTO emlak_detay
                (
                    ilan_id,
                    emlak_tipi,
                    ilan_durumu,
                    metrekare,
                    oda_sayisi,
                    salon_sayisi,
                    bina_yasi,
                    bulundugu_kat,
                    toplam_kat,
                    isitma,
                    banyo_sayisi,
                    balkon,
                    asansor,
                    otopark,
                    esyali,
                    site_icerisinde,
                    aidat,
                    kredi_uygun,
                    tapu_durumu,
                    kullanim_durumu,
                    takas
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
                """,
                (
                    ilan_id,
                    form_text(
                        "bina_tipi",
                        form_text("emlak_tipi")
                    ),
                    form_text(
                        "ilan_durumu",
                        "Satılık"
                    ),
                    form_float("metrekare"),
                    form_text("oda_sayisi"),
                    form_text("salon_sayisi"),
                    form_int("bina_yasi"),
                    form_text("bulundugu_kat"),
                    form_int("toplam_kat"),
                    form_text("isitma"),
                    form_int("banyo_sayisi"),
                    form_bool("balkon"),
                    form_bool("asansor"),
                    form_bool("otopark"),
                    form_bool("esyali"),
                    form_bool("site_icerisinde"),
                    form_float("aidat"),
                    form_bool("kredi_uygun"),
                    form_text("tapu_durumu"),
                    form_text("kullanim_durumu"),
                    form_bool("takas")
                )
            )


        # =====================================================
        # DÜKKAN
        # =====================================================

        elif kategori == "Dukkan":

            imlec.execute(
                """
                INSERT INTO isyeri_detay
                (
                    ilan_id,
                    isyeri_tipi,
                    ilan_durumu,
                    metrekare,
                    bina_yasi,
                    oda_sayisi,
                    bulundugu_kat,
                    toplam_kat,
                    isitma,
                    banyo,
                    mutfak,
                    depo,
                    vitrin,
                    cephe,
                    asansor,
                    otopark,
                    aidat,
                    kredi_uygun,
                    tapu_durumu,
                    kullanim_durumu,
                    takas
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
                """,
                (
                    ilan_id,
                    form_text(
                        "dukkan_tipi",
                        form_text("isyeri_tipi")
                    ),
                    form_text(
                        "ilan_durumu_dukkan",
                        "Satılık"
                    ),
                    form_float(
                        "dukkan_metrekare",
                        form_float("metrekare")
                    ),
                    form_int(
                        "dukkan_bina_yasi",
                        form_int("bina_yasi")
                    ),
                    form_text(
                        "dukkan_oda_sayisi",
                        form_text("oda_sayisi")
                    ),
                    form_text(
                        "dukkan_bulundugu_kat",
                        form_text("bulundugu_kat")
                    ),
                    form_int(
                        "dukkan_toplam_kat",
                        form_int("toplam_kat")
                    ),
                    form_text(
                        "dukkan_isitma",
                        form_text("isitma")
                    ),
                    form_bool("dukkan_banyo"),
                    form_bool("dukkan_mutfak"),
                    form_bool("dukkan_depo"),
                    form_bool("dukkan_vitrin"),
                    form_text(
                        "dukkan_cephe",
                        form_text("cephe")
                    ),
                    form_bool("dukkan_asansor"),
                    form_bool("dukkan_otopark"),
                    form_float(
                        "dukkan_aidat",
                        form_float("aidat")
                    ),
                    form_bool(
                        "dukkan_kredi_uygun"
                    ),
                    form_text(
                        "dukkan_tapu_durumu",
                        form_text("tapu_durumu")
                    ),
                    form_text(
                        "dukkan_kullanim_durumu",
                        form_text("kullanim_durumu")
                    ),
                    form_bool("dukkan_takas")
                )
            )


        # =====================================================
        # ARSA
        # =====================================================

        elif kategori == "Arsa":

            imlec.execute(
                """
                INSERT INTO arsa_detay
                (
                    ilan_id,
                    ilan_durumu,
                    metrekare,
                    imar_durumu,
                    ada_no,
                    parsel_no,
                    tapu_durumu,
                    kredi_uygun,
                    takas,
                    kat_karsiligi,
                    ifrazli,
                    kaks,
                    emsal,
                    gabari,
                    cephe,
                    yol_durumu,
                    elektrik,
                    su,
                    kanalizasyon,
                    dogalgaz,
                    kadastro_yolu,
                    merkeze_uzaklik
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
                """,
                (
                    ilan_id,
                    form_text(
                        "ilan_durumu_arsa",
                        "Satılık"
                    ),
                    form_float("metrekare_arsa"),
                    form_text("imar_durumu"),
                    form_text("ada_no"),
                    form_text("parsel_no"),
                    form_text("arsa_tapu_durumu"),
                    form_bool("kredi_uygun_arsa"),
                    form_bool("takas_arsa"),
                    form_bool("kat_karsiligi"),
                    form_bool("ifrazli"),
                    form_text("kaks"),
                    form_text("emsal"),
                    form_text("gabari"),
                    form_text("arsa_cephe"),
                    form_text("yol_durumu"),
                    form_bool("elektrik"),
                    form_bool("su"),
                    form_bool("kanalizasyon"),
                    form_bool("dogalgaz"),
                    form_bool("kadastro_yolu"),
                    form_text("merkeze_uzaklik")
                )
            )


        # =====================================================
        # TARLA
        # =====================================================

        elif kategori == "Tarla":

            # Tarla için arsa'ya özgü alanları
            # bilinçli olarak boş bırakıyoruz.
            imlec.execute(
                """
                INSERT INTO arsa_detay
                (
                    ilan_id,
                    ilan_durumu,
                    metrekare,
                    imar_durumu,
                    ada_no,
                    parsel_no,
                    tapu_durumu,
                    kredi_uygun,
                    takas,
                    kat_karsiligi,
                    ifrazli,
                    kaks,
                    emsal,
                    gabari,
                    cephe,
                    yol_durumu,
                    elektrik,
                    su,
                    kanalizasyon,
                    dogalgaz,
                    kadastro_yolu,
                    merkeze_uzaklik
                )
                VALUES (
                    ?, ?, ?, '', '', '', ?, ?, ?, 0, ?,
                    '', '', '', '', ?, ?, ?, ?, ?, ?, ?
                )
                """,
                (
                    ilan_id,
                    form_text(
                        "ilan_durumu_arsa",
                        "Satılık"
                    ),
                    form_float("metrekare_arsa"),
                    form_text("arsa_tapu_durumu"),
                    form_bool("kredi_uygun_arsa"),
                    form_bool("takas_arsa"),
                    form_bool("ifrazli"),
                    form_text("yol_durumu"),
                    form_bool("elektrik"),
                    form_bool("su"),
                    form_bool("kanalizasyon"),
                    form_bool("dogalgaz"),
                    form_bool("kadastro_yolu"),
                    form_text("merkeze_uzaklik")
                )
            )


        # =====================================================
        # FOTOĞRAFLAR
        # =====================================================

        fiziksel_dosyalar = (
            fotoğrafları_kaydet(
                baglanti,
                ilan_id,
                ilan_kodu,
                request.files.getlist(
                    "resimler"
                )
            )
        )


        baglanti.commit()


        return redirect(
            url_for(
                "ilan_detay_sayfasi",
                id=ilan_id
            )
        )


    except Exception as hata:

        baglanti.rollback()


        for dosya_adi in fiziksel_dosyalar:

            try:

                yol = dosya_yolu(
                    dosya_adi
                )


                if os.path.exists(yol):
                    os.remove(yol)

            except OSError:
                pass


        print(
            "İLAN EKLEME HATASI:",
            hata
        )


        return (
            "İlan eklenirken hata oluştu: "
            f"{hata}",
            500
        )


    finally:

        baglanti.close()


# =========================================================
# İLAN DETAY
# =========================================================

@app.route(
    "/ilan/<int:id>"
)
def ilan_detay_sayfasi(
    id
):

    ilan = ilan_getir(id)


    if not ilan:

        return (
            "Aradığınız ilan bulunamadı.",
            404
        )


    return render_template(
        "ilan_detay.html",
        ilan=ilan,
        yoneticiler=SITE_YONETICILERI
    )


# =========================================================
# İLAN SİL
# =========================================================

@app.route(
    "/urunler/sil/<int:id>"
)
def urun_sil(
    id
):

    if not giris_yapildi():

        return redirect("/login")


    baglanti = baglan()
    fotoğraflar = []


    try:

        ilan = baglanti.execute(
            """
            SELECT *
            FROM ilanlar
            WHERE id=?
            LIMIT 1
            """,
            (
                id,
            )
        ).fetchone()


        if not ilan:

            return redirect("/urunler")


        if not ilan_yetkisi(
            ilan["ilan_sahibi"]
        ):

            return redirect("/urunler")


        fotoğraflar = baglanti.execute(
            """
            SELECT dosya_adi
            FROM ilan_resimleri
            WHERE ilan_id=?
            """,
            (
                id,
            )
        ).fetchall()


        baglanti.execute(
            """
            DELETE FROM ilanlar
            WHERE id=?
            """,
            (
                id,
            )
        )


        baglanti.commit()


    except Exception as hata:

        baglanti.rollback()


        print(
            "İLAN SİLME HATASI:",
            hata
        )


        return (
            "İlan silinirken hata oluştu.",
            500
        )


    finally:

        baglanti.close()


    for foto in fotoğraflar:

        yol = dosya_yolu(
            foto["dosya_adi"]
        )


        try:

            if os.path.exists(yol):
                os.remove(yol)

        except OSError as hata:

            print(
                "Fotoğraf silinemedi:",
                hata
            )


    return redirect("/urunler")


# =========================================================
# İLAN GÜNCELLE SAYFASI
# =========================================================

@app.route(
    "/urunler/guncelle/<int:id>"
)
def urun_guncelle(
    id
):

    if not giris_yapildi():

        return redirect("/login")


    ilan = ilan_getir(id)


    if not ilan:

        return redirect("/urunler")


    if not ilan_yetkisi(
        ilan.get(
            "ilan_sahibi",
            ""
        )
    ):

        return redirect("/urunler")


    return render_template(
        "urun_guncelle.html",
        urun=ilan,
        ilan=ilan
    )


# =========================================================
# YARDIMCI: DETAY TABLOLARINI TEMİZLE
# =========================================================

def detay_tablolarini_temizle(
    imlec,
    ilan_id
):

    for tablo in [
        "otomobil_detay",
        "emlak_detay",
        "isyeri_detay",
        "arsa_detay"
    ]:

        imlec.execute(
            f"""
            DELETE FROM {tablo}
            WHERE ilan_id=?
            """,
            (
                ilan_id,
            )
        )


# =========================================================
# İLAN GÜNCELLE
# =========================================================

@app.route(
    "/urunler/guncelle",
    methods=["POST"]
)
def urun_kaydet():

    if not giris_yapildi():

        return redirect("/login")


    try:

        ilan_id = int(
            request.form.get(
                "id",
                "0"
            )
        )

    except (
        TypeError,
        ValueError
    ):

        return (
            "Geçersiz ilan ID.",
            400
        )


    ilan = ilan_getir(
        ilan_id
    )


    if not ilan:

        return (
            "İlan bulunamadı.",
            404
        )


    if not ilan_yetkisi(
        ilan.get(
            "ilan_sahibi",
            ""
        )
    ):

        return (
            "Bu ilanı güncelleme yetkiniz yok.",
            403
        )


    eski_kategori = kategori_normalize(
        ilan.get(
            "kategori",
            "Otomobil"
        )
    )


    kategori = kategori_normalize(
        request.form.get(
            "kategori",
            eski_kategori
        )
    )


    if kategori not in KATEGORILER:

        kategori = eski_kategori


    baslik = request.form.get(
        "ad",
        ilan.get(
            "baslik",
            ""
        )
    ).strip()


    if not baslik:

        return render_template(
            "urun_guncelle.html",
            urun=ilan,
            ilan=ilan,
            hata="İlan başlığı boş bırakılamaz."
        )


    aciklama = request.form.get(
        "aciklama"
    )


    if aciklama is None:

        aciklama = request.form.get(
            "acıklama",
            ilan.get(
                "aciklama",
                ""
            )
        )


    aciklama = (
        aciklama
        or ""
    ).strip()


    fiyat = normalize_onluk_deger(
        request.form.get(
            "fiyat"
        )
    )


    if fiyat is None:

        fiyat = float(
            ilan.get(
                "fiyat",
                0
            )
            or 0
        )


    fiyat = max(
        fiyat,
        0
    )


    baglanti = baglan()
    fiziksel_dosyalar = []


    try:

        imlec = baglanti.cursor()


        # =====================================================
        # ANA İLAN
        # =====================================================

        imlec.execute(
            """
            UPDATE ilanlar
            SET
                kategori=?,
                baslik=?,
                fiyat=?,
                aciklama=?,
                guncelleme_tarihi=?
            WHERE id=?
            """,
            (
                kategori,
                baslik,
                fiyat,
                aciklama,
                simdi(),
                ilan_id
            )
        )


        # =====================================================
        # KATEGORİ DEĞİŞTİYSE ESKİ DETAYI TEMİZLE
        # =====================================================

        if kategori != eski_kategori:

            detay_tablolarini_temizle(
                imlec,
                ilan_id
            )


        # =====================================================
        # OTOMOBİL
        # =====================================================

        if kategori == "Otomobil":

            imlec.execute(
                """
                INSERT INTO otomobil_detay
                (
                    ilan_id,
                    marka,
                    model,
                    yil,
                    km,
                    yakit,
                    vites,
                    kasa_tipi,
                    motor_hacmi,
                    motor_gucu,
                    cekis,
                    renk,
                    hasar_durumu,
                    degisen,
                    boya,
                    tramer,
                    takas,
                    kredi_uygun
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?
                )
                ON CONFLICT(ilan_id)
                DO UPDATE SET
                    marka=excluded.marka,
                    model=excluded.model,
                    yil=excluded.yil,
                    km=excluded.km,
                    yakit=excluded.yakit,
                    vites=excluded.vites,
                    kasa_tipi=excluded.kasa_tipi,
                    motor_hacmi=excluded.motor_hacmi,
                    motor_gucu=excluded.motor_gucu,
                    cekis=excluded.cekis,
                    renk=excluded.renk,
                    hasar_durumu=excluded.hasar_durumu,
                    degisen=excluded.degisen,
                    boya=excluded.boya,
                    tramer=excluded.tramer,
                    takas=excluded.takas,
                    kredi_uygun=excluded.kredi_uygun
                """,
                (
                    ilan_id,
                    form_text("marka"),
                    form_text("model"),
                    form_int("yil"),
                    form_int("km"),
                    form_text("yakit"),
                    form_text("vites"),
                    form_text("kasa_tipi"),
                    form_text("motor_hacmi"),
                    form_text("motor_gucu"),
                    form_text("cekis"),
                    form_text("renk"),
                    form_text("hasar_durumu"),
                    form_bool("degisen"),
                    form_bool("boya"),
                    form_bool("tramer"),
                    form_bool("takas"),
                    form_bool("kredi_uygun")
                )
            )


        # =====================================================
        # DAİRE / EV
        # =====================================================

        elif kategori in {
            "Daire",
            "Ev"
        }:

            imlec.execute(
                """
                INSERT INTO emlak_detay
                (
                    ilan_id,
                    emlak_tipi,
                    ilan_durumu,
                    metrekare,
                    oda_sayisi,
                    salon_sayisi,
                    bina_yasi,
                    bulundugu_kat,
                    toplam_kat,
                    isitma,
                    banyo_sayisi,
                    balkon,
                    asansor,
                    otopark,
                    esyali,
                    site_icerisinde,
                    aidat,
                    kredi_uygun,
                    tapu_durumu,
                    kullanim_durumu,
                    takas
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
                ON CONFLICT(ilan_id)
                DO UPDATE SET
                    emlak_tipi=excluded.emlak_tipi,
                    ilan_durumu=excluded.ilan_durumu,
                    metrekare=excluded.metrekare,
                    oda_sayisi=excluded.oda_sayisi,
                    salon_sayisi=excluded.salon_sayisi,
                    bina_yasi=excluded.bina_yasi,
                    bulundugu_kat=excluded.bulundugu_kat,
                    toplam_kat=excluded.toplam_kat,
                    isitma=excluded.isitma,
                    banyo_sayisi=excluded.banyo_sayisi,
                    balkon=excluded.balkon,
                    asansor=excluded.asansor,
                    otopark=excluded.otopark,
                    esyali=excluded.esyali,
                    site_icerisinde=excluded.site_icerisinde,
                    aidat=excluded.aidat,
                    kredi_uygun=excluded.kredi_uygun,
                    tapu_durumu=excluded.tapu_durumu,
                    kullanim_durumu=excluded.kullanim_durumu,
                    takas=excluded.takas
                """,
                (
                    ilan_id,
                    form_text(
                        "bina_tipi",
                        form_text("emlak_tipi")
                    ),
                    form_text(
                        "ilan_durumu",
                        "Satılık"
                    ),
                    form_float("metrekare"),
                    form_text("oda_sayisi"),
                    form_text("salon_sayisi"),
                    form_int("bina_yasi"),
                    form_text("bulundugu_kat"),
                    form_int("toplam_kat"),
                    form_text("isitma"),
                    form_int("banyo_sayisi"),
                    form_bool("balkon"),
                    form_bool("asansor"),
                    form_bool("otopark"),
                    form_bool("esyali"),
                    form_bool("site_icerisinde"),
                    form_float("aidat"),
                    form_bool("kredi_uygun"),
                    form_text("tapu_durumu"),
                    form_text("kullanim_durumu"),
                    form_bool("takas")
                )
            )


        # =====================================================
        # DÜKKAN
        # =====================================================

        elif kategori == "Dukkan":

            imlec.execute(
                """
                INSERT INTO isyeri_detay
                (
                    ilan_id,
                    isyeri_tipi,
                    ilan_durumu,
                    metrekare,
                    bina_yasi,
                    oda_sayisi,
                    bulundugu_kat,
                    toplam_kat,
                    isitma,
                    banyo,
                    mutfak,
                    depo,
                    vitrin,
                    cephe,
                    asansor,
                    otopark,
                    aidat,
                    kredi_uygun,
                    tapu_durumu,
                    kullanim_durumu,
                    takas
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
                ON CONFLICT(ilan_id)
                DO UPDATE SET
                    isyeri_tipi=excluded.isyeri_tipi,
                    ilan_durumu=excluded.ilan_durumu,
                    metrekare=excluded.metrekare,
                    bina_yasi=excluded.bina_yasi,
                    oda_sayisi=excluded.oda_sayisi,
                    bulundugu_kat=excluded.bulundugu_kat,
                    toplam_kat=excluded.toplam_kat,
                    isitma=excluded.isitma,
                    banyo=excluded.banyo,
                    mutfak=excluded.mutfak,
                    depo=excluded.depo,
                    vitrin=excluded.vitrin,
                    cephe=excluded.cephe,
                    asansor=excluded.asansor,
                    otopark=excluded.otopark,
                    aidat=excluded.aidat,
                    kredi_uygun=excluded.kredi_uygun,
                    tapu_durumu=excluded.tapu_durumu,
                    kullanim_durumu=excluded.kullanim_durumu,
                    takas=excluded.takas
                """,
                (
                    ilan_id,
                    form_text(
                        "dukkan_tipi",
                        form_text("isyeri_tipi")
                    ),
                    form_text(
                        "ilan_durumu_dukkan",
                        "Satılık"
                    ),
                    form_float(
                        "dukkan_metrekare",
                        form_float("metrekare")
                    ),
                    form_int(
                        "dukkan_bina_yasi",
                        form_int("bina_yasi")
                    ),
                    form_text(
                        "dukkan_oda_sayisi",
                        form_text("oda_sayisi")
                    ),
                    form_text(
                        "dukkan_bulundugu_kat",
                        form_text("bulundugu_kat")
                    ),
                    form_int(
                        "dukkan_toplam_kat",
                        form_int("toplam_kat")
                    ),
                    form_text(
                        "dukkan_isitma",
                        form_text("isitma")
                    ),
                    form_bool("dukkan_banyo"),
                    form_bool("dukkan_mutfak"),
                    form_bool("dukkan_depo"),
                    form_bool("dukkan_vitrin"),
                    form_text(
                        "dukkan_cephe",
                        form_text("cephe")
                    ),
                    form_bool("dukkan_asansor"),
                    form_bool("dukkan_otopark"),
                    form_float(
                        "dukkan_aidat",
                        form_float("aidat")
                    ),
                    form_bool("dukkan_kredi_uygun"),
                    form_text(
                        "dukkan_tapu_durumu",
                        form_text("tapu_durumu")
                    ),
                    form_text(
                        "dukkan_kullanim_durumu",
                        form_text("kullanim_durumu")
                    ),
                    form_bool("dukkan_takas")
                )
            )


        # =====================================================
        # ARSA
        # =====================================================

        elif kategori == "Arsa":

            imlec.execute(
                """
                INSERT INTO arsa_detay
                (
                    ilan_id,
                    ilan_durumu,
                    metrekare,
                    imar_durumu,
                    ada_no,
                    parsel_no,
                    tapu_durumu,
                    kredi_uygun,
                    takas,
                    kat_karsiligi,
                    ifrazli,
                    kaks,
                    emsal,
                    gabari,
                    cephe,
                    yol_durumu,
                    elektrik,
                    su,
                    kanalizasyon,
                    dogalgaz,
                    kadastro_yolu,
                    merkeze_uzaklik
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
                ON CONFLICT(ilan_id)
                DO UPDATE SET
                    ilan_durumu=excluded.ilan_durumu,
                    metrekare=excluded.metrekare,
                    imar_durumu=excluded.imar_durumu,
                    ada_no=excluded.ada_no,
                    parsel_no=excluded.parsel_no,
                    tapu_durumu=excluded.tapu_durumu,
                    kredi_uygun=excluded.kredi_uygun,
                    takas=excluded.takas,
                    kat_karsiligi=excluded.kat_karsiligi,
                    ifrazli=excluded.ifrazli,
                    kaks=excluded.kaks,
                    emsal=excluded.emsal,
                    gabari=excluded.gabari,
                    cephe=excluded.cephe,
                    yol_durumu=excluded.yol_durumu,
                    elektrik=excluded.elektrik,
                    su=excluded.su,
                    kanalizasyon=excluded.kanalizasyon,
                    dogalgaz=excluded.dogalgaz,
                    kadastro_yolu=excluded.kadastro_yolu,
                    merkeze_uzaklik=excluded.merkeze_uzaklik
                """,
                (
                    ilan_id,
                    form_text(
                        "ilan_durumu_arsa",
                        "Satılık"
                    ),
                    form_float("metrekare_arsa"),
                    form_text("imar_durumu"),
                    form_text("ada_no"),
                    form_text("parsel_no"),
                    form_text("arsa_tapu_durumu"),
                    form_bool("kredi_uygun_arsa"),
                    form_bool("takas_arsa"),
                    form_bool("kat_karsiligi"),
                    form_bool("ifrazli"),
                    form_text("kaks"),
                    form_text("emsal"),
                    form_text("gabari"),
                    form_text("arsa_cephe"),
                    form_text("yol_durumu"),
                    form_bool("elektrik"),
                    form_bool("su"),
                    form_bool("kanalizasyon"),
                    form_bool("dogalgaz"),
                    form_bool("kadastro_yolu"),
                    form_text("merkeze_uzaklik")
                )
            )


        # =====================================================
        # TARLA
        # =====================================================

        elif kategori == "Tarla":

            imlec.execute(
                """
                INSERT INTO arsa_detay
                (
                    ilan_id,
                    ilan_durumu,
                    metrekare,
                    imar_durumu,
                    ada_no,
                    parsel_no,
                    tapu_durumu,
                    kredi_uygun,
                    takas,
                    kat_karsiligi,
                    ifrazli,
                    kaks,
                    emsal,
                    gabari,
                    cephe,
                    yol_durumu,
                    elektrik,
                    su,
                    kanalizasyon,
                    dogalgaz,
                    kadastro_yolu,
                    merkeze_uzaklik
                )
                VALUES (
                    ?, ?, ?, '', '', '', ?, ?, ?, 0, ?, '',
                    '', '', '', ?, ?, ?, ?, ?, ?, ?
                )
                ON CONFLICT(ilan_id)
                DO UPDATE SET
                    ilan_durumu=excluded.ilan_durumu,
                    metrekare=excluded.metrekare,
                    imar_durumu='',
                    ada_no='',
                    parsel_no='',
                    tapu_durumu=excluded.tapu_durumu,
                    kredi_uygun=excluded.kredi_uygun,
                    takas=excluded.takas,
                    kat_karsiligi=0,
                    ifrazli=excluded.ifrazli,
                    kaks='',
                    emsal='',
                    gabari='',
                    cephe='',
                    yol_durumu=excluded.yol_durumu,
                    elektrik=excluded.elektrik,
                    su=excluded.su,
                    kanalizasyon=excluded.kanalizasyon,
                    dogalgaz=excluded.dogalgaz,
                    kadastro_yolu=excluded.kadastro_yolu,
                    merkeze_uzaklik=excluded.merkeze_uzaklik
                """,
                (
                    ilan_id,
                    form_text(
                        "ilan_durumu_arsa",
                        "Satılık"
                    ),
                    form_float("metrekare_arsa"),
                    form_text("arsa_tapu_durumu"),
                    form_bool("kredi_uygun_arsa"),
                    form_bool("takas_arsa"),
                    form_bool("ifrazli"),
                    form_text("yol_durumu"),
                    form_bool("elektrik"),
                    form_bool("su"),
                    form_bool("kanalizasyon"),
                    form_bool("dogalgaz"),
                    form_bool("kadastro_yolu"),
                    form_text("merkeze_uzaklik")
                )
            )


        # =====================================================
        # YENİ FOTOĞRAFLAR
        # =====================================================

        fiziksel_dosyalar = (
            fotoğrafları_kaydet(
                baglanti,
                ilan_id,
                ilan.get(
                    "ilan_kodu",
                    ""
                ),
                request.files.getlist(
                    "resimler"
                )
            )
        )


        baglanti.commit()


    except Exception as hata:

        baglanti.rollback()


        for dosya_adi in fiziksel_dosyalar:

            try:

                yol = dosya_yolu(
                    dosya_adi
                )


                if os.path.exists(yol):
                    os.remove(yol)

            except OSError:
                pass


        print(
            "İLAN GÜNCELLEME HATASI:",
            hata
        )


        return (
            "İlan güncellenirken hata oluştu: "
            f"{hata}",
            500
        )


    finally:

        baglanti.close()


    return redirect(
        url_for(
            "ilan_detay_sayfasi",
            id=ilan_id
        )
    )


# =========================================================
# FOTOĞRAF SİL
# =========================================================

@app.route(
    "/ilan/<int:ilan_id>/resim-sil/<int:resim_id>"
)
def resim_sil(
    ilan_id,
    resim_id
):

    if not giris_yapildi():

        return redirect("/login")


    baglanti = baglan()
    fiziksel_yol = None


    try:

        ilan = baglanti.execute(
            """
            SELECT *
            FROM ilanlar
            WHERE id=?
            LIMIT 1
            """,
            (
                ilan_id,
            )
        ).fetchone()


        if not ilan:

            return redirect("/urunler")


        if not ilan_yetkisi(
            ilan["ilan_sahibi"]
        ):

            return redirect("/urunler")


        resim = baglanti.execute(
            """
            SELECT *
            FROM ilan_resimleri
            WHERE
                id=?
                AND ilan_id=?
            LIMIT 1
            """,
            (
                resim_id,
                ilan_id
            )
        ).fetchone()


        if not resim:

            return redirect(
                url_for(
                    "urun_guncelle",
                    id=ilan_id
                )
            )


        fiziksel_yol = dosya_yolu(
            resim["dosya_adi"]
        )


        eski_kapak = (
            int(
                resim["kapak"]
                or 0
            ) == 1
        )


        baglanti.execute(
            """
            DELETE FROM ilan_resimleri
            WHERE id=?
            """,
            (
                resim_id,
            )
        )


        if eski_kapak:

            yeni_kapak = baglanti.execute(
                """
                SELECT id
                FROM ilan_resimleri
                WHERE ilan_id=?
                ORDER BY sira ASC, id ASC
                LIMIT 1
                """,
                (
                    ilan_id,
                )
            ).fetchone()


            if yeni_kapak:

                baglanti.execute(
                    """
                    UPDATE ilan_resimleri
                    SET kapak=0
                    WHERE ilan_id=?
                    """,
                    (
                        ilan_id,
                    )
                )


                baglanti.execute(
                    """
                    UPDATE ilan_resimleri
                    SET kapak=1
                    WHERE id=?
                    """,
                    (
                        yeni_kapak["id"],
                    )
                )


        baglanti.commit()


    except Exception as hata:

        baglanti.rollback()


        print(
            "RESİM SİLME HATASI:",
            hata
        )


        return (
            "Resim silinirken hata oluştu.",
            500
        )


    finally:

        baglanti.close()


    try:

        if (
            fiziksel_yol
            and
            os.path.exists(
                fiziksel_yol
            )
        ):

            os.remove(
                fiziksel_yol
            )


    except OSError as hata:

        print(
            "Resim fiziksel olarak silinemedi:",
            hata
        )


    return redirect(
        url_for(
            "urun_guncelle",
            id=ilan_id
        )
    )


# =========================================================
# KAPAK FOTOĞRAFI
# =========================================================

@app.route(
    "/ilan/<int:ilan_id>/resim-kapak/<int:resim_id>"
)
def resim_kapak_yap(
    ilan_id,
    resim_id
):

    if not giris_yapildi():

        return redirect("/login")


    baglanti = baglan()


    try:

        ilan = baglanti.execute(
            """
            SELECT *
            FROM ilanlar
            WHERE id=?
            LIMIT 1
            """,
            (
                ilan_id,
            )
        ).fetchone()


        if not ilan:

            return redirect("/urunler")


        if not ilan_yetkisi(
            ilan["ilan_sahibi"]
        ):

            return redirect("/urunler")


        resim = baglanti.execute(
            """
            SELECT id
            FROM ilan_resimleri
            WHERE
                id=?
                AND ilan_id=?
            LIMIT 1
            """,
            (
                resim_id,
                ilan_id
            )
        ).fetchone()


        if not resim:

            return redirect(
                url_for(
                    "urun_guncelle",
                    id=ilan_id
                )
            )


        baglanti.execute(
            """
            UPDATE ilan_resimleri
            SET kapak=0
            WHERE ilan_id=?
            """,
            (
                ilan_id,
            )
        )


        baglanti.execute(
            """
            UPDATE ilan_resimleri
            SET kapak=1
            WHERE
                id=?
                AND ilan_id=?
            """,
            (
                resim_id,
                ilan_id
            )
        )


        baglanti.commit()


    except Exception as hata:

        baglanti.rollback()


        print(
            "KAPAK FOTOĞRAFI HATASI:",
            hata
        )


        return (
            "Kapak fotoğrafı değiştirilemedi.",
            500
        )


    finally:

        baglanti.close()


    return redirect(
        url_for(
            "urun_guncelle",
            id=ilan_id
        )
    )


# =========================================================
# API - TÜM İLANLAR
# =========================================================

@app.route("/api/ilanlar")
def api_ilanlar():

    baglanti = baglan()


    try:

        ilanlar = [

            dict(x)

            for x in (
                baglanti.execute(
                    """
                    SELECT *
                    FROM ilanlar
                    WHERE aktif=1
                    ORDER BY id DESC
                    """
                ).fetchall()
            )
        ]


    finally:

        baglanti.close()


    for ilan in ilanlar:

        tam_ilan = ilan_getir(
            ilan["id"]
        )


        if tam_ilan:

            ilan.update(
                tam_ilan
            )


    return jsonify(
        ilanlar
    )


# =========================================================
# API - TEK İLAN
# =========================================================

@app.route(
    "/api/ilan/<int:id>"
)
def api_ilan(
    id
):

    ilan = ilan_getir(id)


    if not ilan:

        return jsonify(
            {
                "hata":
                    "İlan bulunamadı."
            }
        ), 404


    return jsonify(
        ilan
    )


# =========================================================
# 413
# =========================================================

@app.errorhandler(413)
def dosya_cok_buyuk(
    hata
):

    return (
        "Yüklenen dosyaların toplam boyutu "
        "32 MB sınırını aşamaz.",
        413
    )


# =========================================================
# 404
# =========================================================

@app.errorhandler(404)
def sayfa_bulunamadi(
    hata
):

    return (
        "Aradığınız sayfa bulunamadı.",
        404
    )


# =========================================================
# 500
# =========================================================

@app.errorhandler(500)
def sunucu_hatasi(hata):

    import traceback

    print()
    print("==========================================")
    print("500 SUNUCU HATASI")
    print("==========================================")
    print("HATA:", repr(hata))
    print()
    print("TRACEBACK:")
    traceback.print_exc()
    print("==========================================")
    print()

    return (
        "Sunucu tarafında bir hata oluştu. "
        "Ayrıntılı hata terminalde gösterildi.",
        500
    )
# =========================================================
# UYGULAMA
# =========================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )


    debug = (
        os.environ.get(
            "FLASK_DEBUG",
            "0"
        )
        == "1"
    )


    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug
    )