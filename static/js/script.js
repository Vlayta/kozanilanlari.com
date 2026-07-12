let urunler = [];
let urun_index = 0;
let galeriListesi = [];
let galeriMevcutIdx = 0;
// BURAYA EKLEDİK:
const SABIT_TELEFON = "905534016336"; 

const modelEslesmeleri = {
  
    "Alfa Romeo": ["Giulia","Giulietta","159","156","147","Tonale","Stelvio","Mito"],
    "Audi": ["A1","A3","A4","A5","A6","A7","A8","Q2","Q3","Q5","Q7","Q8","TT","R8","e-tron"],
    "BMW": ["116i","118i","120i","316i","318i","320i","320d","520i","520d","530i","730d","X1","X3","X5","X6","i3","i4","iX"],
    "Chery": ["Tiggo 2","Tiggo 4","Tiggo 7","Tiggo 8","Omoda 5"],
    "Chevrolet": ["Aveo","Cruze","Captiva","Spark","Lacetti"],
    "Citroen": ["C1","C3","C4","C5","C-Elysee","Berlingo","Jumpy"],
    "Cupra": ["Formentor","Leon","Born","Ateca"],

    "Dacia": [
        "Sandero","Sandero Stepway",
        "Logan","Logan MCV",
        "Duster","Jogger","Spring","Dokker","Lodgy"
    ],

    "DS": ["DS3","DS4","DS7"],

    "Fiat": [
        "Egea Sedan","Egea Hatchback","Egea Cross","Egea SW",
        "Punto","Grande Punto",
        "Tipo","Tipo Sedan","Tipo SW",
        "500","500X","500L",
        "Doblo","Doblo Cargo",
        "Fiorino","Linea","Albea","Panda","Bravo"
    ],
    
    "Ford": [
        "Fiesta","Focus","Focus Sedan","Focus Wagon",
        "Mondeo","Mondeo Wagon",
        "Puma","Kuga","EcoSport",
        "Tourneo Courier","Tourneo Connect",
        "Ranger","Ranger Raptor",
        "Transit","Transit Custom","Custom Tourneo"
    ],

    "Honda": [
        "Civic","Civic Sedan","Civic HB",
        "Jazz","City",
        "CR-V","HR-V","ZR-V",
        "Accord","Insight","Pilot"
    ],

    "Hyundai": ["i10","i20","i30","Accent","Elantra","Bayon","Kona","Tucson","Santa Fe"],
    "Isuzu": ["D-Max"],
    "Jaguar": ["XE","XF","F-Pace","E-Pace"],
    "Jeep": ["Renegade","Compass","Cherokee","Wrangler","Avenger"],
    "Kia": ["Picanto","Rio","Ceed","Cerato","Stonic","Sportage","Sorento","EV6"],
    "Land Rover": ["Defender","Discovery","Range Rover Evoque","Range Rover Sport"],
    "Lexus": ["CT200h","IS","ES","NX","RX","UX"],
    "Mazda": ["2","3","6","CX-3","CX-5","CX-60"],
    "Mercedes-Benz": ["A180","A200","B180","C180","C200","E200","E220","S350","GLA","GLC","GLE","Vito","Sprinter"],
    "MG": ["ZS","HS","MG4"],
    "Mini": ["Cooper","Countryman","Clubman"],
    "Mitsubishi": ["L200","ASX","Outlander","Colt"],
    "Nissan": ["Micra","Note","Juke","Qashqai","X-Trail","Navara"],
    "Opel": [
        "Corsa","Astra","Astra Sedan","Astra Sports Tourer",
        "Insignia","Insignia Sports Tourer",
        "Mokka","Crossland","Grandland",
        "Combo","Vivaro","Movano","Vectra","Omega"
    ],

    "Peugeot": [
        "108","208","208 GT","308","308 SW",
        "408","508","508 SW",
        "2008","3008","5008",
        "Partner","Rifter","Expert","Boxer"
    ],
    "Porsche": ["Macan","Cayenne","Panamera","911","Taycan"],

    "Renault": [
        "TX","Toros","Clio","Clio HB","Clio Sedan",
        "Megane","Megane HB","Megane Sedan","Megane Sport Tourer",
        "Symbol","Fluence","Talisman",
        "Captur","Kadjar","Arkana","Austral",
        "Kangoo","Express","Trafic","Master",
        "Duster","Laguna","Latitude"
    ],
    "Seat": ["Ibiza","Leon","Arona","Ateca"],
    "Skoda": [
        "Fabia","Rapid","Scala",
        "Octavia","Octavia Combi",
        "Superb","Superb Combi",
        "Kamiq","Karoq","Kodiaq",
        "Roomster","Yeti"
    ],
    "Suzuki": ["Swift","Vitara","SX4","Jimny","S-Cross"],
    "Tesla": ["Model 3","Model Y","Model S","Model X"],
    "Tofas": ["Doğan","Şahin","Kartal","Murat 131"],
    "Toyota": [
        "Corolla","Corolla Sedan","Corolla HB","Corolla Cross",
        "Yaris","Yaris Hybrid",
        "C-HR","RAV4","Hilux","Auris",
        "Avensis","Camry","Prius",
        "Proace City","Proace Verso","Land Cruiser"
    ],
    "Volkswagen": [
        "Polo","Golf","Golf GTI","Golf Variant",
        "Passat","Passat Variant",
        "Jetta","Bora",
        "Arteon","T-Cross","Taigo","Tiguan","Tiguan Allspace",
        "Touareg","Caddy","Transporter","Caravelle","Amarok",
        "Beetle","Up"
    ],
    "Volvo": ["S60","S90","V40","XC40","XC60","XC90"]
};

function modelleriYukle() {
    const marka = document.getElementById("marka")?.value;
    const modelBox = document.getElementById("model");
    if (!modelBox) return;

    modelBox.innerHTML = '<option value="">Seçiniz</option>';
    if (marka && modelEslesmeleri[marka]) {
        modelBox.disabled = false;
        modelEslesmeleri[marka].forEach(m => {
            let opt = document.createElement("option");
            opt.value = m; opt.textContent = m;
            modelBox.appendChild(opt);
        });
    } else {
        modelBox.disabled = true;
    }
}

function formAlanlariniGuncelle() {
    const kategoriSelect = document.getElementById("kategori_secim");
    if (!kategoriSelect) return;
    
    const kategori = kategoriSelect.value;
    
    const alanlar = [
        "alan-otomobil-ozel", "alan-otomobil-teknik", "alan-otomobil-check",
        "alan-emlak-ozel", "alan-emlak-teknik", "alan-emlak-check",
        "alan-arsa-ozel", "alan-arsa-teknik", "alan-arsa-check"
    ];
    
    alanlar.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.style.display = "none";
    });

    const zorunlular = document.querySelectorAll('.dinamik-alan input, .dinamik-alan select');
    zorunlular.forEach(el => el.removeAttribute('required'));

    if (kategori === "Otomobil") {
        const o1 = document.getElementById("alan-otomobil-ozel"); if(o1) o1.style.display = "flex";
        const o2 = document.getElementById("alan-otomobil-teknik"); if(o2) o2.style.display = "flex";
        const o3 = document.getElementById("alan-otomobil-check"); if(o3) o3.style.display = "flex";
        
        document.getElementById("marka")?.setAttribute('required', 'required');
        document.getElementById("model")?.setAttribute('required', 'required');
        document.getElementById("yil_oto")?.setAttribute('required', 'required');
        document.getElementById("km_oto")?.setAttribute('required', 'required');
    } 
    else if (kategori === "Daire" || kategori === "Ev") {
        const e1 = document.getElementById("alan-emlak-ozel"); if(e1) e1.style.display = "flex";
        const e2 = document.getElementById("alan-emlak-teknik"); if(e2) e2.style.display = "flex";
        const e3 = document.getElementById("alan-emlak-check"); if(e3) e3.style.display = "flex";
        
        document.getElementById("bina_tipi")?.setAttribute('required', 'required');
        document.getElementById("ilan_durumu")?.setAttribute('required', 'required');
        document.getElementById("bina_yasi")?.setAttribute('required', 'required');
        document.getElementById("metrekare")?.setAttribute('required', 'required');
        document.getElementById("oda_sayisi")?.setAttribute('required', 'required');
        
        const katBlok = document.getElementById("blok-daire-kat");
        const katSelect = document.getElementById("bulundugu_kat");
        if (kategori === "Daire") {
            if (katBlok) katBlok.style.display = "block";
            if (katSelect) katSelect.setAttribute('required', 'required');
        } else {
            if (katBlok) katBlok.style.display = "none";
            if (katSelect) katSelect.removeAttribute('required');
        }
    } 
    else if (kategori === "Arsa" || kategori === "Tarla") {
        const a1 = document.getElementById("alan-arsa-ozel"); if(a1) a1.style.display = "flex";
        const a2 = document.getElementById("alan-arsa-teknik"); if(a2) a2.style.display = "flex";
        const a3 = document.getElementById("alan-arsa-check"); if(a3) a3.style.display = "flex";
        
        document.getElementById("imar_durumu")?.setAttribute('required', 'required');
        document.getElementById("ilan_durumu_arsa")?.setAttribute('required', 'required');
        document.getElementById("metrekare_arsa")?.setAttribute('required', 'required');
        document.getElementById("ada_no")?.setAttribute('required', 'required');
        document.getElementById("parsel_no")?.setAttribute('required', 'required');
    }
}

document.addEventListener("DOMContentLoaded", function() {
    const katSelect = document.getElementById("kategori_secim");
    if (katSelect) {
        katSelect.addEventListener("change", formAlanlariniGuncelle);
        formAlanlariniGuncelle();
    }

    const izgaraKontrol = document.getElementById("ilanListesiIzgara");
    if (izgaraKontrol) {
        fetch('/api/ilanlar')
            .then(res => res.json())
            .then(data => {
                urunler = data;
                ilanlariDiz(urunler);
                if(urunler.length > 0) vitrinGuncelle(0);
            });

        document.getElementById("sonraki")?.addEventListener("click", () => {
            if (urunler.length === 0) return;
            urun_index = (urun_index + 1) % urunler.length;
            vitrinGuncelle(urun_index);
        });

        document.getElementById("onceki")?.addEventListener("click", () => {
            if (urunler.length === 0) return;
            urun_index = (urun_index - 1 + urunler.length) % urunler.length;
            vitrinGuncelle(urun_index);
        });

        document.getElementById("rastgele")?.addEventListener("click", () => {
            if (urunler.length <= 1) return;
            let aday;
            do { aday = Math.floor(Math.random() * urunler.length); } while(aday === urun_index);
            urun_index = aday;
            vitrinGuncelle(urun_index);
        });
    }
});
function filtreleVeSirala() {
    const arama = document.getElementById("pazarAra")?.value.toLowerCase();
    const kaza = document.getElementById("pazarKaza")?.value;
    const sira = document.getElementById("pazarSira")?.value;
    const katFiltre = document.getElementById("pazarKategori")?.value;

    let filtrelenmis = urunler.filter(i => {
        let metin = `${i.marka} ${i.model} ${i.ad} ${i.kategori}`.toLowerCase().includes(arama);
        
        let katUyum = !katFiltre || katFiltre === "hepsi" || i.kategori === katFiltre;
        
        let kazaUyum = true;
        if (i.kategori === "Otomobil" || !i.kategori) {
            let hasarli = i.degisen === "true" || i.boya === "true" || i.tramer === "true";
            kazaUyum = kaza === "hepsi" || (kaza === "hatasiz" && !hasarli) || (kaza === "kazali" && hasarli);
        } else {
            kazaUyum = kaza === "hepsi";
        }
        
        return metin && katUyum && kazaUyum;
    });

    if(sira === "fiyatArtan") filtrelenmis.sort((a,b) => a.fiyat - b.fiyat);
    if(sira === "fiyatAzalan") filtrelenmis.sort((a,b) => b.fiyat - a.fiyat);
    if(sira === "yilYeni") filtrelenmis.sort((a,b) => (b.yil || 0) - (a.yil || 0));
    if(sira === "kmDusuk") filtrelenmis.sort((a,b) => (a.km || 0) - (b.km || 0));

    ilanlariDiz(filtrelenmis);
}

function vitrinGuncelle(idx) {
    if (urunler.length === 0) return;

    // 1. SOL KUTU LİNK VE VERİ GÜNCELLEMESİ
    const solArac = urunler[idx];
    const solEk = solArac.kategori === "Otomobil" ? ` (${solArac.yil})` : "";
    
    const solIsimEl = document.getElementById("urun_isim");
    const solKodEl = document.getElementById("urun_kod");
    const solFiyatEl = document.getElementById("urun_fiyat");
    const solResimEl = document.getElementById("urun_resim");
    
    // HTML üzerindeki a href kapsayıcı linkleri yakalanıyor
    const urunLinkResim = document.getElementById("urun_link_resim");
    const urunLinkIsim = document.getElementById("urun_link_isim");

    if (solIsimEl) solIsimEl.textContent = solArac.ad + solEk;
    if (solKodEl) solKodEl.textContent = solArac.kod;
    if (solFiyatEl) solFiyatEl.textContent = Number(solArac.fiyat).toLocaleString('tr-TR') + " TL";
    if (solResimEl) solResimEl.src = solArac.resim ? "/static/uploads/" + solArac.resim : "/static/uploads/varsayilan_araba.jpg";
    
    // KESİN ÇÖZÜM: Sol vitrin kartı resmine veya başlığına basıldığında detay sayfasına gider

    if (urunLinkResim) urunLinkResim.href = `/ilan/${solArac.id}`;
    if (urunLinkIsim) urunLinkIsim.href = `/ilan/${solArac.id}`;

    // BURAYA EKLEDİK:
    const solWpBtn = document.getElementById("urun_wp_link");
    if (solWpBtn) {
        if (typeof UYE_GIRIS_YAPTI_MI !== 'undefined' && UYE_GIRIS_YAPTI_MI) {
            let mesaj = encodeURIComponent(`Merhaba, ${solArac.kod || ''} kodlu "${solArac.ad}" ilanınız için alıcı olmak ve randevu oluşturmak istiyorum.`);
            solWpBtn.href = `https://wa.me/${SABIT_TELEFON}?text=${mesaj}`;
            solWpBtn.target = "_blank";
            solWpBtn.textContent = "🤝 Alıcı Ol / Randevu Al";
            solWpBtn.style.backgroundColor = "";
        } else {
            solWpBtn.href = "/kaydol";
            solWpBtn.removeAttribute("target");
            solWpBtn.textContent = "🔒 İletişim İçin Kaydol";
            solWpBtn.style.backgroundColor = "#e67e22";
        }
    }

    // 2. SAĞ KUTU LİNK VE VERİ GÜNCELLEMESİ
    if (urunler.length > 1) {
        let sagIdx = (idx + 1) % urunler.length;
        const sagArac = urunler[sagIdx];
        const sagEk = sagArac.kategori === "Otomobil" ? ` (${sagArac.yil})` : "";
        
        const sagIsimEl = document.getElementById("urun_isim_sag");
        const sagKodEl = document.getElementById("urun_kod_sag");
        const sagFiyatEl = document.getElementById("urun_fiyat_sag");
        const sagResimEl = document.getElementById("urun_resim_sag");
        
        // HTML üzerindeki a href kapsayıcı sağ linkleri yakalanıyor
        const urunLinkResimSag = document.getElementById("urun_link_resim_sag");
        const urunLinkIsimSag = document.getElementById("urun_link_isim_sag");

        if (sagIsimEl) sagIsimEl.textContent = sagArac.ad + sagEk;
        if (sagKodEl) sagKodEl.textContent = sagArac.kod;
        if (sagFiyatEl) sagFiyatEl.textContent = Number(sagArac.fiyat).toLocaleString('tr-TR') + " TL";
        if (sagResimEl) sagResimEl.src = sagArac.resim ? "/static/uploads/" + sagArac.resim : "/static/uploads/varsayilan_araba.jpg";
        
        // KESİN ÇÖZÜM: Sağ vitrin kartı resmine veya başlığına basıldığında detay sayfasına gider
        if (urunLinkResimSag) urunLinkResimSag.href = `/ilan/${sagArac.id}`;
        if (urunLinkIsimSag) urunLinkIsimSag.href = `/ilan/${sagArac.id}`;

        // BURAYA EKLEDİK:
        const sagWpBtn = document.getElementById("urun_wp_link_sag");
        if (sagWpBtn) {
            if (typeof UYE_GIRIS_YAPTI_MI !== 'undefined' && UYE_GIRIS_YAPTI_MI) {
                let mesaj = encodeURIComponent(`Merhaba, ${sagArac.kod || ''} kodlu "${sagArac.ad}" ilanınız için alıcı olmak ve randevu oluşturmak istiyorum.`);
                sagWpBtn.href = `https://wa.me{SABIT_TELEFON}?text=${mesaj}`;
                sagWpBtn.target = "_blank";
                sagWpBtn.textContent = "🤝 Alıcı Ol / Randevu Al";
                sagWpBtn.style.backgroundColor = "";
            } else {
                sagWpBtn.href = "/kaydol";
                sagWpBtn.removeAttribute("target");
                sagWpBtn.textContent = "🔒 İletişim İçin Kaydol";
                sagWpBtn.style.backgroundColor = "#e67e22";
            }
        }

    } else {
        if (document.getElementById("urun_isim_sag")) document.getElementById("urun_isim_sag").textContent = "Fırsat İlanı Bekleniyor...";
        if (document.getElementById("urun_kod_sag")) document.getElementById("urun_kod_sag").textContent = "--";
        if (document.getElementById("urun_fiyat_sag")) document.getElementById("urun_fiyat_sag").textContent = "0 TL";
        if (document.getElementById("urun_resim_sag")) document.getElementById("urun_resim_sag").src = "/static/uploads/varsayilan_araba.jpg";
    }
}

// Alt kısımdaki canlı arama ızgarası ilan kartı oluşturma döngüsü
function ilanlariDiz(liste) {
    const izgara = document.getElementById("ilanListesiIzgara");
    if(!izgara) return;
    izgara.innerHTML = "";

    if(liste.length === 0) {
        izgara.innerHTML = "<p style='grid-column:1/-1; text-align:center;'>Kriterlere uygun ilan bulunamadı.</p>";
        return;
    }

    liste.forEach(ilan => {
        const kategori = ilan.kategori || "Otomobil";
        let altDetayHtml = "";
        let rozetHtml = '<span class="kart-rozet hatasiz">✨ Hatasız</span>';
        
        if (kategori === "Otomobil") {
            let hasar = ilan.degisen === "true" || ilan.boya === "true" || ilan.tramer === "true";
            rozetHtml = hasar ? '<span class="kart-rozet kazali">⚠️ Hasarlı</span>' : '<span class="kart-rozet hatasiz">✨ Hatasız</span>';
            altDetayHtml = `📅 ${ilan.yil} | 🛣️ ${Number(ilan.km).toLocaleString('tr-TR')} KM | ⚙️ ${ilan.vites}`;
        } else if (kategori === "Daire" || kategori === "Ev") {
            let kredi = ilan.tramer === "true";
            rozetHtml = kredi ? '<span class="kart-rozet hatasiz">🏦 Krediye Uygun</span>' : '<span class="kart-rozet kazali">⚠️ Krediye Uygun Değil</span>';
            altDetayHtml = `📐 ${ilan.km} m² | 🚪 Oda: ${ilan.yakit} | 🏢 Kat: ${ilan.vites}`;
        } else {
            let krediArsa = ilan.tramer === "true";
            rozetHtml = krediArsa ? '<span class="kart-rozet hatasiz">🏦 Krediye Uygun</span>' : '<span class="kart-rozet kazali">⚠️ Krediye Uygun Değil</span>';
            altDetayHtml = `📐 ${ilan.km} m² | 🌍 İmar: ${ilan.marka} | 📍 Ada/Parsel: ${ilan.degisen}/${ilan.boya}`;
        }

        let anaImg = ilan.resim ? "/static/uploads/" + ilan.resim : "/static/uploads/varsayilan_araba.jpg";

        // KESİN ÇÖZÜM: Canlı arama listesindeki ilan kartı şablonu güncellenerek detay linki bağlandı
        
        let renk = "#ff9f43";

if (kategori === "Otomobil") renk = "#3498db";
else if (kategori === "Daire") renk = "#53d318";
else if (kategori === "Ev") renk = "#393ff2";
else if (kategori === "Arsa") renk = "#9b59b6";
else if (kategori === "Tarla") renk = "#b81313";

let kartHtml = `
<div class="vitrin-kutusu arac-kart" style="position:relative;">

    <div style="
        position:absolute;
        top:10px;
        left:10px;
        z-index:20;
        background:${renk};
        color:#fff;
        padding:5px 10px;
        border-radius:6px;
        font-size:12px;
        font-weight:bold;
        box-shadow:0 2px 8px rgba(0,0,0,.35);">
        ${kategori}
    </div>

    <!-- Resme tıklayınca detay sayfasına gider -->
    <a href="/ilan/${ilan.id}" class="vitrin-kart-link">
        <img src="${anaImg}" class="kart-ana-resim">
    </a>

    <div class="kart-icerik">

        <div class="vitrin-etiket-satir">

            <!-- Başlığa tıklayınca detay sayfasına gider -->
            <a href="/ilan/${ilan.id}" class="vitrin-baslik-link">
                <h4>${ilan.ad}</h4>
            </a>

            <span class="v-kod">${ilan.kod}</span>

        </div>

        <p style="color:#bbb;font-size:12px;margin:4px 0;text-align:left;">
            ${altDetayHtml}
        </p>

        <div style="text-align:left;margin-top:5px;margin-bottom:5px;">
            ${rozetHtml}
        </div>





        <div class="kart-alt-fiyat-grup">
            <span class="k-fiyat">
                ${Number(ilan.fiyat).toLocaleString('tr-TR')} TL
            </span>

            <!-- ESKİ REHBER LİNKİ SİLİNDİ, YERİNE BU GELDI: -->
                <a href="${(typeof UYE_GIRIS_YAPTI_MI !== 'undefined' && UYE_GIRIS_YAPTI_MI) ? `https://wa.me/${SABIT_TELEFON}?text=${encodeURIComponent('Merhaba, ' + (ilan.kod || '') + ' kodlu \"' + ilan.ad + '\" ilanınız için alıcı olmak ve randevu oluşturmak istiyorum.')}` : '/kaydol'}" 
               class="btn-wp-aracilik" 
               ${(typeof UYE_GIRIS_YAPTI_MI !== 'undefined' && UYE_GIRIS_YAPTI_MI) ? 'target="_blank"' : ''}
               style="${(typeof UYE_GIRIS_YAPTI_MI !== 'undefined' && UYE_GIRIS_YAPTI_MI) ? '' : 'background-color: #e67e22;'}">
                ${(typeof UYE_GIRIS_YAPTI_MI !== 'undefined' && UYE_GIRIS_YAPTI_MI) ? '🤝 Alıcı Ol / Randevu Al' : '🔒 İletişim İçin Kaydol'}
            </a>
        </div>

    </div>

</div>
`;

        izgara.innerHTML += kartHtml;
    });
}



function lightboxAc(id, idx) {
    const ilan = urunler.find(x => x.id === id);
    if(ilan) {
        let resimListesi = [];
        try {
            resimListesi = typeof ilan.resimler === 'string' ? JSON.parse(ilan.resimler) : ilan.resimler;
        } catch(e) {
            resimListesi = [ilan.resim];
        }
        
        if(Array.isArray(resimListesi) && resimListesi.length > 0) {
            galeriListesi = resimListesi.filter(r => r != "");
            galeriMevcutIdx = idx >= galeriListesi.length ? 0 : idx;
            document.getElementById("pazarLightbox").style.display = "flex";
            lightboxGoster();
        }
    }
}
function lightboxGoster() { document.getElementById("lightboxGorsel").src = "/static/uploads/" + galeriListesi[galeriMevcutIdx]; }
function lightboxKapat() { document.getElementById("pazarLightbox").style.display = "none"; }
function lightboxGez(yon) { galeriMevcutIdx = (galeriMevcutIdx + yon + galeriListesi.length) % galeriListesi.length; lightboxGoster(); }
