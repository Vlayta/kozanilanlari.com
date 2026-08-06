# -*- coding: utf-8 -*-
import os
import json
import sqlite3

from flask import Flask, render_template, request, redirect, session, jsonify, url_for, flash
import secrets
import datetime
from werkzeug.utils import secure_filename

import veritabanini_kur as db
if os.path.exists("veriler.db") == False:
    db.kur()

app = Flask(__name__)
app.secret_key = "A13Fe"

# Görsellerin doğrudan static/uploads altına kaydedilmesi sağlandı
ANA_DIZIN = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(ANA_DIZIN, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DB_YOLU = os.path.join(ANA_DIZIN, "veriler.db")

# YÖNETİCİ TANIMLAMA LİSTESİ
SITE_YONETICILERI = ["mahir", "admin"]

# --- HERKESE AÇIK GEZİLEBİLİR SAYFALAR ---
@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/kurumsal")
def kurumsal_sayfasi():
    return render_template('kurumsal.html')

@app.route("/mahir") 
def mahirin_sayfasi():
    return render_template('mahir.html')

# --- OTURUM YÖNETİMİ ---
@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/loginbilgileri", methods=["POST"])
def login_kontrol():
    giris = request.form["isim"]
    sifre = request.form["sifre"]

    baglanti = sqlite3.connect(DB_YOLU)
    baglanti.row_factory = sqlite3.Row
    imlec = baglanti.cursor()

    imlec.execute("""
        SELECT *
        FROM kullanicilar
        WHERE (ad=? OR telefon=? OR email=?)
        AND sifre=?
    """, (giris, giris, giris, sifre))

    kullanici = imlec.fetchone()
    baglanti.close()

    if not kullanici:
        return render_template(
            "login.html",
            hata="Kullanıcı bilgileri hatalı."
        )

    session["ad"] = kullanici["ad"]
    session["sifre"] = kullanici["sifre"]

    return redirect("/")

@app.route("/sifre_linki", methods=["POST"])
def sifre_linki():
    email = request.form["email"]
    token = secrets.token_urlsafe(32)
    sure = datetime.datetime.now() + datetime.timedelta(minutes=30)

    baglanti = sqlite3.connect(DB_YOLU)
    imlec = baglanti.cursor()

    imlec.execute("""
        UPDATE kullanicilar
        SET sifre_token=?,
            token_suresi=?
        WHERE email=?
    """, (token, str(sure), email))

    baglanti.commit()
    baglanti.close()

    print("\nŞifre yenileme linki:\n")
    print("http://127.0.0" + token)

    flash("Şifre yenileme bağlantısı oluşturuldu.")
    return redirect("/login")

@app.route("/sifre_yenile/<token>")
def sifre_yenile(token):
    baglanti = sqlite3.connect(DB_YOLU)
    baglanti.row_factory = sqlite3.Row
    imlec = baglanti.cursor()

    imlec.execute("""
        SELECT *
        FROM kullanicilar
        WHERE sifre_token=?
    """, (token,))

    kullanici = imlec.fetchone()
    baglanti.close()

    if not kullanici:
        return "Geçersiz bağlantı."

    return render_template(
        "sifre_yenile.html",
        token=token
    )

@app.route("/sifre_degistir", methods=["POST"])
def sifre_degistir():
    token = request.form["token"]
    sifre = request.form["sifre"]

    baglanti = sqlite3.connect(DB_YOLU)
    imlec = baglanti.cursor()

    imlec.execute("""
        UPDATE kullanicilar
        SET sifre=?,
            sifre_token=NULL,
            token_suresi=NULL
        WHERE sifre_token=?
    """, (sifre, token))

    baglanti.commit()
    baglanti.close()
    return redirect("/login")

@app.route("/cikis")  
def cikis():
    session["ad"] = None
    session["sifre"] = None
    return redirect("/")

@app.route("/kaydol")
def kaydol():
    return render_template('kaydol.html')

@app.route("/kayitbilgileri", methods=["POST"])
def kayit():
    isim = request.form["isim"]
    email = request.form["email"]
    sifre = request.form["sifre"]
    telefon = request.form.get("telefon", "")

    baglanti = sqlite3.connect(DB_YOLU)
    imlec = baglanti.cursor()
    imlec.execute("SELECT * FROM kullanicilar WHERE ad=?", (isim,))
    if len(imlec.fetchall()) == 0: 
        imlec.execute("INSERT INTO kullanicilar VALUES(?, ?, ?, ?)", (isim, email, sifre, telefon))
        baglanti.commit()
        baglanti.close()
        session["ad"] = isim
        return redirect("/")
    baglanti.close()
    return render_template("kaydol.html", hata="Bu kullanıcı zaten kayıtlı")

    # ... (Yukarıdaki mevcut kayıt kodlarınızın devamı)
    baglanti.close()
    return render_template("kaydol.html", hata="Bu kullanıcı zaten kayıtlı")


# =====================================================================
#  YENİ EKLENEN KISIM: ŞİFREMİ UNUTTUM SAYFASI VE TETİKLEYİCİSİ
# =====================================================================
@app.route("/sifremi-unuttum")
def sifremi_unuttum_sayfasi():
    return render_template('sifremi_unuttum.html')

@app.route("/sifremi-unuttum-gonder", methods=["POST"])
def sifremi_unuttum_gonder():
    email = request.form.get("email", "")
    token = secrets.token_urlsafe(32)
    sure = datetime.datetime.now() + datetime.timedelta(minutes=30)

    baglanti = sqlite3.connect(DB_YOLU)
    imlec = baglanti.cursor()
    imlec.execute("""
        UPDATE kullanicilar
        SET sifre_token=?,
            token_suresi=?
        WHERE email=?
    """, (token, str(sure), email))

    baglanti.commit()
    baglanti.close()

    # Link formatı yerel ağda (192.168...) test ettiğiniz için dinamik hale getirildi
    print("\nŞifre yenileme linki:\n")
    print(f"http://{request.host}/sifre_yenile/{token}")

    flash("Şifre yenileme bağlantısı oluşturuldu. Konsolu kontrol edin.")
    return redirect("/login")
# =====================================================================




# --- MÜDAHALE KORUMALI İLAN YÖNETİM ALANI ---
@app.route("/urunler")
def urunler():
    if not session.get("ad"): return redirect("/login")
    
    kategori_filtresi = request.args.get("kategori", "")
    current_user = str(session["ad"]).lower()
    
    baglanti = sqlite3.connect(DB_YOLU)
    baglanti.row_factory = sqlite3.Row
    imlec = baglanti.cursor()
    
    if current_user in SITE_YONETICILERI:
        if kategori_filtresi:
            imlec.execute("SELECT * FROM urunler WHERE kategori=?", (kategori_filtresi,))
        else:
            imlec.execute("SELECT * FROM urunler")
    else:
        if kategori_filtresi:
            imlec.execute("SELECT * FROM urunler WHERE LOWER(ilani_veren)=? AND kategori=?", (current_user, kategori_filtresi))
        else:
            imlec.execute("SELECT * FROM urunler WHERE LOWER(ilani_veren)=?", (current_user,))
        
    kayitlar = [dict(row) for row in imlec.fetchall()]
    baglanti.close()
    return render_template("urunler.html", urunler=kayitlar, yoneticiler=SITE_YONETICILERI, secilen_kategori=kategori_filtresi)

@app.route("/urunler/sil/<id>")
def urun_sil(id):
    if not session.get("ad"): return redirect("/login")
    
    current_user = str(session["ad"]).lower()
    baglanti = sqlite3.connect(DB_YOLU)
    baglanti.row_factory = sqlite3.Row
    imlec = baglanti.cursor()
    imlec.execute("SELECT ilani_veren FROM urunler WHERE id=?", (int(id),))
    ilan = imlec.fetchone()
    
    if ilan:
        ilan_sahibi = str(ilan["ilani_veren"]).lower()
        if current_user in SITE_YONETICILERI or ilan_sahibi == current_user:
            imlec.execute("DELETE FROM urunler WHERE id=?", (int(id),))
            baglanti.commit()
            
    baglanti.close()
    return redirect("/urunler")  

@app.route("/urunler/guncelle/<id>")
def urun_guncelle(id):
    if not session.get("ad"): return redirect("/login")
    
    current_user = str(session["ad"]).lower()
    baglanti = sqlite3.connect(DB_YOLU)
    baglanti.row_factory = sqlite3.Row
    imlec = baglanti.cursor()
    imlec.execute("SELECT * FROM urunler WHERE id=?", (int(id),))
    row = imlec.fetchone()
    baglanti.close()
    
    if row:
        ilan = dict(row)
        ilan_sahibi = str(ilan["ilani_veren"]).lower()
        if current_user in SITE_YONETICILERI or ilan_sahibi == current_user:
            return render_template("urun_guncelle.html", urun=ilan)
            
    return redirect("/urunler")

# --- DİNAMİK İLAN DETAY SAYFASI ---
@app.route("/ilan/<int:id>")
def ilan_detay_sayfasi(id):
    baglanti = sqlite3.connect(DB_YOLU)
    baglanti.row_factory = sqlite3.Row
    imlec = baglanti.cursor()
    imlec.execute("SELECT * FROM urunler WHERE id=?", (id,))
    row = imlec.fetchone()
    baglanti.close()
    
    if not row:
        return "Aradığınız ilan pazar havuzunda bulunamadı.", 404
        
    ilan = dict(row)
    try:
        ilan['resimler_liste'] = json.loads(ilan['resimler']) if ilan['resimler'] else [ilan['resim']]
    except:
        ilan['resimler_liste'] = [ilan['resim']] if ilan['resim'] else ["varsayilan_araba.jpg"]
        
    return render_template("ilan_detay.html", ilan=ilan, yoneticiler=SITE_YONETICILERI)

@app.route("/urunler/guncelle", methods=["POST"])
def urun_kaydet():
    if not session.get("ad"): return redirect("/login")      
    
    id_ham = request.form.get("id")
    try:
        id = int(id_ham)
    except:
        return "Geçersiz İlan ID", 400
        
    kod = request.form.get("kod", "")
    ad = request.form.get("ad", "")
    fiyat = request.form.get("fiyat", "0")
    kategori = request.form.get("kategori", "").strip()
    
    # KESİN ÇÖZÜM: Formdaki textarea name="acıklama" verisi tam olarak yakalanıyor
    acıklama = request.form.get("acıklama", "")
    current_user = str(session["ad"]).lower()

    if not kategori or kategori == "None" or kategori == "":
        kategori = "Otomobil"

    if kategori == "Otomobil":
        marka = request.form.get("marka", "")
        model = request.form.get("model", "")
        yil = request.form.get("yil", "")
        km = request.form.get("km", "")
        yakit = request.form.get("yakit", "")
        vites = request.form.get("vites", "")
        degisen = "true" if request.form.get("degisen") in ["true", "on", True] else "false"
        boya = "true" if request.form.get("boya") in ["true", "on", True] else "false"
        tramer = "true" if request.form.get("tramer") in ["true", "on", True] else "false"
    elif kategori in ["Daire", "Ev"]:
        marka = request.form.get("bina_tipi", "")
        model = request.form.get("ilan_durumu", "")
        yil = request.form.get("bina_yasi", "")
        km = request.form.get("metrekare", "")
        yakit = request.form.get("oda_sayisi", "")
        vites = request.form.get("bulundugu_kat", "") if kategori == "Daire" else "Müstakil"
        degisen = "false"
        boya = "false"
        tramer = "true" if request.form.get("kredi_uygun") in ["true", "on", True] else "false"
    else:  # Arsa ve Tarla
        marka = request.form.get("imar_durumu", "")
        model = request.form.get("ilan_durumu_arsa", "")
        yil = ""
        km = request.form.get("metrekare_arsa", "")
        yakit = ""
        vites = ""
        degisen = request.form.get("ada_no", "") if request.form.get("ada_no") else ""
        boya = request.form.get("parsel_no", "") if request.form.get("parsel_no") else ""
        tramer = "true" if request.form.get("kredi_uygun_arsa") in ["true", "on", True] else "false"

    baglanti = sqlite3.connect(DB_YOLU)
    baglanti.row_factory = sqlite3.Row
    imlec = baglanti.cursor()
    imlec.execute("SELECT ilani_veren, resim, resimler FROM urunler WHERE id=?", (id,))
    ilan_row = imlec.fetchone()
    
    if ilan_row:
        ilan_kontrol = dict(ilan_row)
        ilan_sahibi = str(ilan_kontrol["ilani_veren"]).lower()
        mevcut_resim = ilan_kontrol["resim"] if ilan_kontrol["resim"] else "varsayilan_araba.jpg"
        mevcut_resimler_json = ilan_kontrol["resimler"]
        
        if current_user in SITE_YONETICILERI or ilan_sahibi == current_user:
            try:
                if mevcut_resimler_json:
                    kayitli_resimler = json.loads(mevcut_resimler_json)
                else:
                    kayitli_resimler = [mevcut_resim]
            except:
                kayitli_resimler = [mevcut_resim] if mevcut_resim else []
                
            if not isinstance(kayitli_resimler, list):
                kayitli_resimler = [mevcut_resim]
                
            yeni_resimler = list(kayitli_resimler)
            while len(yeni_resimler) < 6:
                yeni_resimler.append("")
                
            for i in range(1, 7):
                file = request.files.get(f'resim{i}')
                if file and file.filename != '':
                    g_ad = secure_filename(file.filename)
                    b_isim = f"{i}_{secure_filename(kod)}_{g_ad}"
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], b_isim))
                    yeni_resimler[i-1] = b_isim
                    if i == 1: mevcut_resim = b_isim

            temiz_resimler = [r for r in yeni_resimler if r and r != ""]
            if not temiz_resimler:
                temiz_resimler = [mevcut_resim]
            resimler_json = json.dumps(temiz_resimler)

            # KESİN ÇÖZÜM: Sorguya 'acıklama=?' alanı eklendi ve ilan başlığını ezmesi durduruldu
            imlec.execute("""
                UPDATE urunler SET 
                    ad=?, fiyat=?, marka=?, model=?, yil=?, km=?, yakit=?, vites=?, 
                    degisen=?, boya=?, tramer=?, resim=?, resimler=?, kategori=?, acıklama=? 
                WHERE id=?
            """, (ad, float(fiyat), marka, model, yil, km, yakit, vites, degisen, boya, tramer, mevcut_resim, resimler_json, kategori, acıklama, id))
            baglanti.commit()
        
    baglanti.close()    
    return redirect("/urunler") 

@app.route("/urun_ekle_sayfa")
def urun_ekle_sayfa():
    if not session.get("ad"): 
        return redirect("/login")
    return render_template("urun_ekle.html")

@app.route("/urun_ekle", methods=["POST"])
def urun_ekle():
    if not session.get("ad"): 
        return redirect("/login")
        
    kod = request.form["kod"]
    ad = request.form["ad"]
    fiyat = request.form["fiyat"]
    kategori = request.form.get("kategori", "Otomobil")
    # KESİN ÇÖZÜM: Yeni eklenen ilandaki açıklama metni çekiliyor
    acıklama = request.form.get("acıklama", "")
    
    if kategori == "Otomobil":
        marka = request.form["marka"]
        model = request.form["model"]
        yil = request.form["yil"]
        km = request.form["km"]
        yakit = request.form["yakit"]
        vites = request.form["vites"]
        degisen = "true" if request.form.get("degisen") in ["true", "on", True] else "false"
        boya = "true" if request.form.get("boya") in ["true", "on", True] else "false"
        tramer = "true" if request.form.get("tramer") in ["true", "on", True] else "false"
    elif kategori in ["Daire", "Ev"]:
        marka = request.form.get("bina_tipi", "")
        model = request.form.get("ilan_durumu", "")
        yil = request.form.get("bina_yasi", "")
        km = request.form.get("metrekare", "")
        yakit = request.form.get("oda_sayisi", "")
        vites = request.form.get("bulundugu_kat", "") if kategori == "Daire" else "Müstakil"
        degisen = "false"
        boya = "false"
        tramer = "true" if request.form.get("kredi_uygun") in ["true", "on", True] else "false"
    else:
        marka = request.form.get("imar_durumu", "")
        model = request.form.get("ilan_durumu_arsa", "")
        yil = ""
        km = request.form.get("metrekare_arsa", "")
        yakit = ""
        vites = ""
        degisen = request.form.get("ada_no") if request.form.get("ada_no") else ""
        boya = request.form.get("parsel_no") if request.form.get("parsel_no") else ""
        tramer = "true" if request.form.get("kredi_uygun_arsa") in ["true", "on", True] else "false"
    
    baglanti = sqlite3.connect(DB_YOLU)
    imlec = baglanti.cursor()
    
    imlec.execute("SELECT telefon FROM kullanicilar WHERE ad=?", (session["ad"],))
    user_row = imlec.fetchone()
    
    if user_row and len(user_row) > 0:
        telefon = user_row[0] or ""
    else:
        telefon = ""


    kaydedilen_resimler = []
    kapak = "varsayilan_araba.jpg"

    dosyalar = request.files.getlist("resimler")

    for i, file in enumerate(dosyalar, start=1):

        if file and file.filename:

            g_ad = secure_filename(file.filename)
            b_isim = f"{i}_{secure_filename(kod)}_{g_ad}"

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], b_isim))

            kaydedilen_resimler.append(b_isim)

            if i == 1:
                kapak = b_isim

    if not kaydedilen_resimler:
        kaydedilen_resimler.append(kapak)

    resimler_json = json.dumps(kaydedilen_resimler)
    ilani_veren = session["ad"]

    imlec.execute("""
        INSERT INTO urunler (
            kod, ad, fiyat, resim, marka, model, yil, km,
            yakit, vites, degisen, boya, tramer,
            telefon, resimler, ilani_veren, kategori, acıklama
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        kod, ad, float(fiyat), kapak,
        marka, model, yil, km,
        yakit, vites, degisen, boya, tramer,
        telefon, resimler_json, ilani_veren,
        kategori, acıklama
    ))

    baglanti.commit()
    baglanti.close()
    return redirect("/urunler")
@app.route("/api/ilanlar")
def api_ilanlar():
    baglanti = sqlite3.connect(DB_YOLU)
    baglanti.row_factory = sqlite3.Row
    imlec = baglanti.cursor()
    imlec.execute("SELECT * FROM urunler ORDER BY id DESC")
    ilanlar = [dict(row) for row in imlec.fetchall()]
    baglanti.close()
    
    for ilan in ilanlar:
        try:
            ilan['resimler'] = json.loads(ilan['resimler']) if ilan['resimler'] else []
        except:
            ilan['resimler'] = [ilan['resim']] if ilan['resim'] else []
    return jsonify(ilanlar)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


"""if __name__ == "__main__":
    import webbrowser
    # Tarayıcıyı direkt ana sayfaya yönlendirecek şekilde güncellendi. borvserde açmak için kullanılacak
    webbrowser.open("http://192.168.1.114:5000/")
    app.run(debug=True, host="0.0.0.0", port=5000)"""

