/* ============================================================
   KOZAN İLANLARI
   ANA JAVASCRIPT
   app.py + veritabanini_kur.py + HTML şablonları ile uyumlu
   ============================================================ */

"use strict";


/* ============================================================
   1. GENEL DEĞİŞKENLER
   ============================================================ */

let urunler = [];
let filtrelenmisUrunler = [];
let urun_index = 0;


/* ============================================================
   2. SABİTLER
   ============================================================ */

const KAYIT_URL = "/kaydol";

const VARSAYILAN_RESIM =
    "/static/uploads/varsayilan_araba.jpg";

const MAX_FOTO = 10;


/* ============================================================
   3. MARKA / MODEL
   ============================================================ */

const modelEslesmeleri = {

    "Alfa Romeo": [
        "Giulia",
        "Giulietta",
        "159",
        "156",
        "147",
        "Tonale",
        "Stelvio",
        "Mito"
    ],

    "Audi": [
        "A1",
        "A3",
        "A4",
        "A5",
        "A6",
        "A7",
        "A8",
        "Q2",
        "Q3",
        "Q5",
        "Q7",
        "Q8",
        "TT",
        "R8",
        "e-tron"
    ],

    "BMW": [
        "116i",
        "118i",
        "120i",
        "316i",
        "318i",
        "320i",
        "320d",
        "520i",
        "520d",
        "530i",
        "730d",
        "X1",
        "X3",
        "X5",
        "X6",
        "i3",
        "i4",
        "iX"
    ],

    "Chery": [
        "Tiggo 2",
        "Tiggo 4",
        "Tiggo 7",
        "Tiggo 8",
        "Omoda 5"
    ],

    "Chevrolet": [
        "Aveo",
        "Cruze",
        "Captiva",
        "Spark",
        "Lacetti"
    ],

    "Citroen": [
        "C1",
        "C3",
        "C4",
        "C5",
        "C-Elysee",
        "Berlingo",
        "Jumpy"
    ],

    "Cupra": [
        "Formentor",
        "Leon",
        "Born",
        "Ateca"
    ],

    "Dacia": [
        "Sandero",
        "Sandero Stepway",
        "Logan",
        "Logan MCV",
        "Duster",
        "Jogger",
        "Spring",
        "Dokker",
        "Lodgy"
    ],

    "DS": [
        "DS3",
        "DS4",
        "DS7"
    ],

    "Fiat": [
        "Egea Sedan",
        "Egea Hatchback",
        "Egea Cross",
        "Egea SW",
        "Punto",
        "Grande Punto",
        "Tipo",
        "Tipo Sedan",
        "Tipo SW",
        "500",
        "500X",
        "500L",
        "Doblo",
        "Doblo Cargo",
        "Fiorino",
        "Linea",
        "Albea",
        "Panda",
        "Bravo"
    ],

    "Ford": [
        "Fiesta",
        "Focus",
        "Focus Sedan",
        "Focus Wagon",
        "Mondeo",
        "Mondeo Wagon",
        "Puma",
        "Kuga",
        "EcoSport",
        "Tourneo Courier",
        "Tourneo Connect",
        "Ranger",
        "Ranger Raptor",
        "Transit",
        "Transit Custom",
        "Custom Tourneo"
    ],

    "Honda": [
        "Civic",
        "Civic Sedan",
        "Civic HB",
        "Jazz",
        "City",
        "CR-V",
        "HR-V",
        "ZR-V",
        "Accord",
        "Insight",
        "Pilot"
    ],

    "Hyundai": [
        "i10",
        "i20",
        "i30",
        "Accent",
        "Elantra",
        "Bayon",
        "Kona",
        "Tucson",
        "Santa Fe"
    ],

    "Isuzu": [
        "D-Max"
    ],

    "Jaguar": [
        "XE",
        "XF",
        "F-Pace",
        "E-Pace"
    ],

    "Jeep": [
        "Renegade",
        "Compass",
        "Cherokee",
        "Wrangler",
        "Avenger"
    ],

    "Kia": [
        "Picanto",
        "Rio",
        "Ceed",
        "Cerato",
        "Stonic",
        "Sportage",
        "Sorento",
        "EV6"
    ],

    "Land Rover": [
        "Defender",
        "Discovery",
        "Range Rover Evoque",
        "Range Rover Sport"
    ],

    "Lexus": [
        "CT200h",
        "IS",
        "ES",
        "NX",
        "RX",
        "UX"
    ],

    "Mazda": [
        "2",
        "3",
        "6",
        "CX-3",
        "CX-5",
        "CX-60"
    ],

    "Mercedes-Benz": [
        "A180",
        "A200",
        "B180",
        "C180",
        "C200",
        "E200",
        "E220",
        "S350",
        "GLA",
        "GLC",
        "GLE",
        "Vito",
        "Sprinter"
    ],

    "MG": [
        "ZS",
        "HS",
        "MG4"
    ],

    "Mini": [
        "Cooper",
        "Countryman",
        "Clubman"
    ],

    "Mitsubishi": [
        "L200",
        "ASX",
        "Outlander",
        "Colt"
    ],

    "Nissan": [
        "Micra",
        "Note",
        "Juke",
        "Qashqai",
        "X-Trail",
        "Navara"
    ],

    "Opel": [
        "Corsa",
        "Astra",
        "Astra Sedan",
        "Astra Sports Tourer",
        "Insignia",
        "Insignia Sports Tourer",
        "Mokka",
        "Crossland",
        "Grandland",
        "Combo",
        "Vivaro",
        "Movano",
        "Vectra",
        "Omega"
    ],

    "Peugeot": [
        "108",
        "208",
        "208 GT",
        "308",
        "308 SW",
        "408",
        "508",
        "508 SW",
        "2008",
        "3008",
        "5008",
        "Partner",
        "Rifter",
        "Expert",
        "Boxer"
    ],

    "Porsche": [
        "Macan",
        "Cayenne",
        "Panamera",
        "911",
        "Taycan"
    ],

    "Renault": [
        "TX",
        "Toros",
        "Clio",
        "Clio HB",
        "Clio Sedan",
        "Megane",
        "Megane HB",
        "Megane Sedan",
        "Megane Sport Tourer",
        "Symbol",
        "Fluence",
        "Talisman",
        "Captur",
        "Kadjar",
        "Arkana",
        "Austral",
        "Kangoo",
        "Express",
        "Trafic",
        "Master",
        "Duster",
        "Laguna",
        "Latitude"
    ],

    "Seat": [
        "Ibiza",
        "Leon",
        "Arona",
        "Ateca"
    ],

    "Skoda": [
        "Fabia",
        "Rapid",
        "Scala",
        "Octavia",
        "Octavia Combi",
        "Superb",
        "Superb Combi",
        "Kamiq",
        "Karoq",
        "Kodiaq",
        "Roomster",
        "Yeti"
    ],

    "Suzuki": [
        "Swift",
        "Vitara",
        "SX4",
        "Jimny",
        "S-Cross"
    ],

    "Tesla": [
        "Model 3",
        "Model Y",
        "Model S",
        "Model X"
    ],

    "Tofaş": [
        "Doğan",
        "Şahin",
        "Kartal",
        "Murat 131"
    ],

    "Toyota": [
        "Corolla",
        "Corolla Sedan",
        "Corolla HB",
        "Corolla Cross",
        "Yaris",
        "Yaris Hybrid",
        "C-HR",
        "RAV4",
        "Hilux",
        "Auris",
        "Avensis",
        "Camry",
        "Prius",
        "Proace City",
        "Proace Verso",
        "Land Cruiser"
    ],

    "Volkswagen": [
        "Polo",
        "Golf",
        "Golf GTI",
        "Golf Variant",
        "Passat",
        "Passat Variant",
        "Jetta",
        "Bora",
        "Arteon",
        "T-Cross",
        "Taigo",
        "Tiguan",
        "Tiguan Allspace",
        "Touareg",
        "Caddy",
        "Transporter",
        "Caravelle",
        "Amarok",
        "Beetle",
        "Up"
    ],

    "Volvo": [
        "S60",
        "S90",
        "V40",
        "XC40",
        "XC60",
        "XC90"
    ]
};


/* ============================================================
   4. KATEGORİ NORMALİZASYONU
   ============================================================ */

function kategoriNormalize(kategori) {

    const deger =
        String(kategori || "")
            .trim();

    if (
        deger === "Dükkan" ||
        deger === "Dükkan/İşyeri" ||
        deger === "Dukkan/İşyeri" ||
        deger === "İşyeri" ||
        deger === "Isyeri"
    ) {

        return "Dukkan";
    }

    return deger;
}


/* ============================================================
   5. GÖRÜNÜR KATEGORİ ADI
   ============================================================ */

function kategoriGorunenAdi(kategori) {

    const temiz =
        kategoriNormalize(
            kategori
        );

    if (temiz === "Dukkan") {
        return "Dükkan";
    }

    if (temiz === "Otomobil") {
        return "Otomobil";
    }

    if (temiz === "Daire") {
        return "Daire";
    }

    if (temiz === "Ev") {
        return "Müstakil Ev";
    }

    if (temiz === "Arsa") {
        return "Arsa";
    }

    if (temiz === "Tarla") {
        return "Tarla";
    }

    return temiz || "İlan";
}


/* ============================================================
   6. KATEGORİ İKONU
   ============================================================ */

function kategoriIkonu(kategori) {

    switch (
        kategoriNormalize(
            kategori
        )
    ) {

        case "Otomobil":
            return "🚗";

        case "Daire":
            return "🏢";

        case "Ev":
            return "🏡";

        case "Dukkan":
            return "🏪";

        case "Arsa":
            return "🌍";

        case "Tarla":
            return "🌾";

        default:
            return "📋";
    }
}


/* ============================================================
   7. KATEGORİ RENGİ
   ============================================================ */

function kategoriRengi(kategori) {

    switch (
        kategoriNormalize(
            kategori
        )
    ) {

        case "Otomobil":
            return "#3498db";

        case "Daire":
            return "#2ecc71";

        case "Ev":
            return "#16a085";

        case "Dukkan":
            return "#e67e22";

        case "Arsa":
            return "#9b59b6";

        case "Tarla":
            return "#27ae60";

        default:
            return "#ff9f43";
    }
}


/* ============================================================
   8. DEĞER
   ============================================================ */

function deger(
    degerDegeri,
    varsayilan = ""
) {

    if (
        degerDegeri === null ||
        degerDegeri === undefined ||
        String(
            degerDegeri
        ).trim() === ""
    ) {

        return varsayilan;
    }

    return degerDegeri;
}


/* ============================================================
   9. SAYI FORMATLA
   ============================================================ */

function sayiFormatla(
    degerDegeri
) {

    if (
        degerDegeri === null ||
        degerDegeri === undefined ||
        String(
            degerDegeri
        ).trim() === ""
    ) {

        return "-";
    }


    let metin =
        String(
            degerDegeri
        ).trim();


    let sayi =
        Number(
            metin
        );


    if (
        !Number.isFinite(
            sayi
        )
    ) {

        sayi =
            Number(
                metin
                    .replace(
                        /\./g,
                        ""
                    )
                    .replace(
                        ",",
                        "."
                    )
            );
    }


    if (
        !Number.isFinite(
            sayi
        )
    ) {

        return "-";
    }


    return sayi.toLocaleString(
        "tr-TR"
    );
}


/* ============================================================
   10. TELEFON NUMARASI
   ============================================================ */

function telefonNumarasiniDuzenle(
    telefon
) {

    if (
        telefon === null ||
        telefon === undefined
    ) {

        return "";
    }


    let numara =
        String(
            telefon
        )
            .replace(
                /\D/g,
                ""
            );


    if (!numara) {
        return "";
    }


    if (
        numara.startsWith("00")
    ) {

        numara =
            numara.substring(
                2
            );
    }


    if (
        numara.startsWith("0") &&
        numara.length === 11
    ) {

        return (
            "90" +
            numara.substring(
                1
            )
        );
    }


    if (
        numara.startsWith("90") &&
        numara.length === 12
    ) {

        return numara;
    }


    if (
        numara.length === 10
    ) {

        return (
            "90" +
            numara
        );
    }


    return numara;
}


/* ============================================================
   11. TELEFON GÖRÜNÜMÜ
   ============================================================ */

function telefonGorunumu(
    telefon
) {

    const temiz =
        telefonNumarasiniDuzenle(
            telefon
        );


    if (!temiz) {
        return "Telefon bilgisi yok";
    }


    if (
        temiz.startsWith("90") &&
        temiz.length === 12
    ) {

        const yerel =
            "0" +
            temiz.substring(
                2
            );


        return (
            yerel.substring(0, 4) +
            " " +
            yerel.substring(4, 7) +
            " " +
            yerel.substring(7, 9) +
            " " +
            yerel.substring(9, 11)
        );
    }


    return String(
        telefon
    );
}


/* ============================================================
   12. RESİM URL
   ============================================================ */

function resimUrlOlustur(
    dosyaAdi
) {

    if (!dosyaAdi) {

        return VARSAYILAN_RESIM;
    }


    const temiz =
        String(
            dosyaAdi
        )
            .trim()
            .replace(
                /^\/+/,
                ""
            );


    if (
        temiz.startsWith(
            "http://"
        ) ||
        temiz.startsWith(
            "https://"
        )
    ) {

        return temiz;
    }


    if (
        temiz.startsWith(
            "/"
        )
    ) {

        return temiz;
    }


    if (
        temiz.startsWith(
            "static/"
        )
    ) {

        return (
            "/" +
            temiz
        );
    }


    if (
        temiz.startsWith(
            "uploads/"
        )
    ) {

        return (
            "/" +
            temiz
        );
    }


    return (
        "/static/uploads/" +
        encodeURIComponent(
            temiz
        )
    );
}


/* ============================================================
   13. RESİM LİSTESİ
   ============================================================ */

function resimListesiGetir(
    ilan
) {

    if (!ilan) {
        return [];
    }


    let liste = [];


    if (
        Array.isArray(
            ilan.resimler_liste
        )
    ) {

        liste =
            ilan.resimler_liste
                .map(
                    function(resim) {

                        if (
                            typeof resim ===
                            "string"
                        ) {

                            return resim;
                        }


                        return (
                            resim?.url ||
                            resim?.dosya_adi ||
                            ""
                        );
                    }
                )
                .filter(
                    Boolean
                );
    }


    if (
        liste.length === 0 &&
        Array.isArray(
            ilan.resimler
        )
    ) {

        liste =
            ilan.resimler
                .map(
                    function(resim) {

                        if (
                            typeof resim ===
                            "string"
                        ) {

                            return resim;
                        }


                        return (
                            resim?.url ||
                            resim?.dosya_adi ||
                            ""
                        );
                    }
                )
                .filter(
                    Boolean
                );
    }


    if (
        liste.length === 0 &&
        ilan.resim
    ) {

        liste.push(
            ilan.resim
        );
    }


    return liste;
}


/* ============================================================
   14. İLAN KAPAK RESMİ
   ============================================================ */

function ilanKapakResmi(
    ilan
) {

    if (!ilan) {
        return VARSAYILAN_RESIM;
    }


    if (
        ilan.resim_url
    ) {

        return ilan.resim_url;
    }


    if (
        Array.isArray(
            ilan.resimler_liste
        ) &&
        ilan.resimler_liste.length > 0
    ) {

        const kapak =
            ilan.resimler_liste.find(
                function(resim) {

                    return (
                        Number(
                            resim?.kapak || 0
                        ) === 1
                    );
                }
            ) ||
            ilan.resimler_liste[0];


        if (
            kapak?.url
        ) {

            return kapak.url;
        }


        if (
            kapak?.dosya_adi
        ) {

            return resimUrlOlustur(
                kapak.dosya_adi
            );
        }
    }


    const liste =
        resimListesiGetir(
            ilan
        );


    if (
        liste.length > 0
    ) {

        return resimUrlOlustur(
            liste[0]
        );
    }


    return VARSAYILAN_RESIM;
}


/* ============================================================
   15. DETAY DEĞERİ
   ============================================================ */

function ilanDegeri(
    ilan,
    alan
) {

    if (!ilan) {
        return "";
    }


    const detay =
        ilan.detay ||
        {};


    if (
        detay[alan] !== undefined &&
        detay[alan] !== null &&
        String(
            detay[alan]
        ).trim() !== ""
    ) {

        return detay[alan];
    }


    if (
        ilan[alan] !== undefined &&
        ilan[alan] !== null &&
        String(
            ilan[alan]
        ).trim() !== ""
    ) {

        return ilan[alan];
    }


    const alternatifler = {

        metrekare: [
            "metrekare",
            "isyeri_metrekare",
            "arsa_metrekare",
            "metrekare_arsa"
        ],

        bina_yasi: [
            "bina_yasi",
            "isyeri_bina_yasi"
        ],

        bulundugu_kat: [
            "bulundugu_kat",
            "isyeri_kat"
        ],

        oda_sayisi: [
            "oda_sayisi",
            "isyeri_oda_sayisi"
        ],

        isitma: [
            "isitma",
            "isyeri_isitma"
        ],

        ilan_durumu: [
            "ilan_durumu",
            "isyeri_ilan_durumu",
            "arsa_ilan_durumu"
        ],

        kredi_uygun: [
            "kredi_uygun",
            "kredi_uygun_emlak",
            "kredi_uygun_isyeri",
            "kredi_uygun_arsa"
        ]

    };


    const adaylar =
        alternatifler[
            alan
        ] || [];


    for (
        const aday of adaylar
    ) {

        if (
            ilan[aday] !== undefined &&
            ilan[aday] !== null &&
            String(
                ilan[aday]
            ).trim() !== ""
        ) {

            return ilan[aday];
        }


        if (
            detay[aday] !== undefined &&
            detay[aday] !== null &&
            String(
                detay[aday]
            ).trim() !== ""
        ) {

            return detay[aday];
        }
    }


    return "";
}


/* ============================================================
   16. TEKNİK PARÇA
   ============================================================ */

function teknikParcaEkle(
    liste,
    ikon,
    baslik,
    degerDegeri,
    sonEk = ""
) {

    if (
        degerDegeri === null ||
        degerDegeri === undefined ||
        String(
            degerDegeri
        ).trim() === ""
    ) {

        return;
    }


    let metin = "";


    if (ikon) {
        metin += ikon + " ";
    }


    if (baslik) {
        metin +=
            baslik +
            ": ";
    }


    metin +=
        String(
            degerDegeri
        ) +
        sonEk;


    liste.push(
        metin
    );
}

/* ============================================================
   17. TEKNİK DETAY
   ============================================================ */

function teknikDetayOlustur(
    ilan
) {

    if (!ilan) {
        return "";
    }

    const kategori =
        kategoriNormalize(
            ilan.kategori
        );

    const bilgiler = [];


    /* ========================================================
       YARDIMCI FONKSİYON
       Boş değerleri eklemez.
       ======================================================== */

    function ekle(
        ikon,
        baslik,
        deger,
        sonEk = ""
    ) {

        if (
            deger === undefined ||
            deger === null ||
            String(deger).trim() === ""
        ) {
            return;
        }

        teknikParcaEkle(
            bilgiler,
            ikon,
            baslik,
            deger,
            sonEk
        );
    }


    /* ========================================================
       OTOMOBİL
       En önemli bilgiler:
       Marka + Model + Yıl + KM + Yakıt
       ======================================================== */

    if (
        kategori === "Otomobil"
    ) {

        ekle(
            "🚗",
            "",
            ilanDegeri(
                ilan,
                "marka"
            )
        );

        ekle(
            "🔹",
            "",
            ilanDegeri(
                ilan,
                "model"
            )
        );

        ekle(
            "📅",
            "",
            ilanDegeri(
                ilan,
                "yil"
            )
        );

        const km =
            ilanDegeri(
                ilan,
                "km"
            );

        if (km !== "") {

            ekle(
                "🛣️",
                "",
                sayiFormatla(km),
                " KM"
            );
        }

        ekle(
            "⛽",
            "",
            ilanDegeri(
                ilan,
                "yakit"
            )
        );

        /*
         * 5 bilgiden az kaldıysa vites eklenir.
         */
        if (bilgiler.length < 5) {

            ekle(
                "⚙️",
                "",
                ilanDegeri(
                    ilan,
                    "vites"
                )
            );
        }
    }


    /* ========================================================
       DAİRE / EV
       En önemli bilgiler:
       m² + Oda + Kat + Bina yaşı + Isıtma
       ======================================================== */

    else if (
        kategori === "Daire" ||
        kategori === "Ev"
    ) {

        const metrekare =
            ilanDegeri(
                ilan,
                "metrekare"
            );

        if (metrekare !== "") {

            ekle(
                "📐",
                "",
                sayiFormatla(
                    metrekare
                ),
                " m²"
            );
        }

        ekle(
            "🚪",
            "Oda",
            ilanDegeri(
                ilan,
                "oda_sayisi"
            )
        );

        ekle(
            "🛋️",
            "Salon",
            ilanDegeri(
                ilan,
                "salon_sayisi"
            )
        );

        ekle(
            "🏢",
            "Kat",
            ilanDegeri(
                ilan,
                "bulundugu_kat"
            )
        );

        ekle(
            "🔥",
            "Isıtma",
            ilanDegeri(
                ilan,
                "isitma"
            )
        );

        /*
         * Bina yaşı önemli ancak kartta yer kalmazsa
         * otomatik olarak sonraki bilgiye geçilmez.
         *
         * Öncelik:
         * m²
         * oda
         * salon
         * kat
         * ısıtma
         */
    }


    /* ========================================================
       DÜKKAN
       En önemli bilgiler:
       m² + Bölüm + Kat + Isıtma + Bina yaşı
       ======================================================== */

    else if (
        kategori === "Dukkan"
    ) {

        const metrekare =
            ilanDegeri(
                ilan,
                "metrekare"
            );

        if (metrekare !== "") {

            ekle(
                "📐",
                "",
                sayiFormatla(
                    metrekare
                ),
                " m²"
            );
        }

        ekle(
            "🚪",
            "Bölüm",
            ilanDegeri(
                ilan,
                "oda_sayisi"
            )
        );

        ekle(
            "🏢",
            "Kat",
            ilanDegeri(
                ilan,
                "bulundugu_kat"
            )
        );

        ekle(
            "🔥",
            "Isıtma",
            ilanDegeri(
                ilan,
                "isitma"
            )
        );

        ekle(
            "📅",
            "Bina yaşı",
            ilanDegeri(
                ilan,
                "bina_yasi"
            )
        );
    }


    /* ========================================================
       ARSA
       En önemli bilgiler:
       m² + İmar + Ada + Parsel + Yol
       ======================================================== */

    else if (
        kategori === "Arsa"
    ) {

        const metrekare =
            ilanDegeri(
                ilan,
                "metrekare"
            );

        if (metrekare !== "") {

            ekle(
                "📐",
                "",
                sayiFormatla(
                    metrekare
                ),
                " m²"
            );
        }

        ekle(
            "🌍",
            "İmar",
            ilanDegeri(
                ilan,
                "imar_durumu"
            )
        );

        const ada =
            ilanDegeri(
                ilan,
                "ada_no"
            );

        const parsel =
            ilanDegeri(
                ilan,
                "parsel_no"
            );

        let adaParsel = "";

        if (ada) {

            adaParsel =
                "Ada: " +
                ada;
        }

        if (parsel) {

            if (adaParsel) {

                adaParsel +=
                    " / ";
            }

            adaParsel +=
                "Parsel: " +
                parsel;
        }

        if (adaParsel) {

            ekle(
                "📍",
                "",
                adaParsel
            );
        }

        ekle(
            "🛣️",
            "Yol",
            ilanDegeri(
                ilan,
                "yol_durumu"
            )
        );
    }


    /* ========================================================
       TARLA
       En önemli bilgiler:
       m² + Ada + Parsel + Yol + İlan durumu
       ======================================================== */

    else if (
        kategori === "Tarla"
    ) {

        const metrekare =
            ilanDegeri(
                ilan,
                "metrekare"
            );

        if (metrekare !== "") {

            ekle(
                "🌾",
                "",
                sayiFormatla(
                    metrekare
                ),
                " m²"
            );
        }

        ekle(
            "📍",
            "Ada",
            ilanDegeri(
                ilan,
                "ada_no"
            )
        );

        ekle(
            "📍",
            "Parsel",
            ilanDegeri(
                ilan,
                "parsel_no"
            )
        );

        ekle(
            "🛣️",
            "Yol",
            ilanDegeri(
                ilan,
                "yol_durumu"
            )
        );

        ekle(
            "📋",
            "",
            ilanDegeri(
                ilan,
                "ilan_durumu"
            )
        );
    }


    /* ========================================================
       SONUÇ
       ======================================================== */

    if (
        bilgiler.length === 0
    ) {

        return "";
    }


    /*
     * Maksimum 5 bilgi.
     */
    const sinirliBilgiler =
        bilgiler.slice(
            0,
            5
        );


    return sinirliBilgiler.join(
        ' <span class="teknik-ayrac">|</span> '
    );
}

/* ============================================================
   18. ROZET
   ============================================================ */

function rozetBilgisi(
    ilan
) {

    if (!ilan) {

        return {
            sinif: "kazali",
            metin: "⚠️ Bilgi Yok"
        };
    }


    const kategori =
        kategoriNormalize(
            ilan.kategori
        );


    if (
        kategori === "Otomobil"
    ) {

        const hasarli =
            Number(
                ilanDegeri(
                    ilan,
                    "degisen"
                ) || 0
            ) === 1 ||

            Number(
                ilanDegeri(
                    ilan,
                    "boya"
                ) || 0
            ) === 1 ||

            Number(
                ilanDegeri(
                    ilan,
                    "tramer"
                ) || 0
            ) === 1;


        if (hasarli) {

            return {
                sinif: "kazali",
                metin: "⚠️ Hasarlı"
            };
        }


        return {
            sinif: "hatasiz",
            metin: "✨ Hatasız"
        };
    }


    const kredi =
        Number(
            ilanDegeri(
                ilan,
                "kredi_uygun"
            ) || 0
        ) === 1;


    if (kredi) {

        return {
            sinif: "hatasiz",
            metin:
                "🏦 Krediye Uygun"
        };
    }


    return {
        sinif: "kazali",
        metin:
            "⚠️ Krediye Uygun Değil"
    };
}


/* ============================================================
   19. İLETİŞİM
   ============================================================ */

function ilanIletisimVarMi(
    ilan
) {

    if (!ilan) {
        return false;
    }


    const telefon =
        ilan.telefon ||
        ilan.musteri_telefon ||
        "";


    return (
        telefonNumarasiniDuzenle(
            telefon
        ) !== ""
    );
}


/* ============================================================
   20. WHATSAPP LİNK
   ============================================================ */

function whatsappLinkOlustur(
    ilan
) {

    if (!ilan) {
        return KAYIT_URL;
    }


    const telefon =
        telefonNumarasiniDuzenle(
            ilan.telefon ||
            ilan.musteri_telefon
        );


    if (!telefon) {
        return KAYIT_URL;
    }


    const mesaj =
        "Merhaba, " +
        (
            ilan.ilan_kodu ||
            ilan.kod ||
            ""
        ) +
        ' kodlu "' +
        (
            ilan.baslik ||
            ilan.ad ||
            "ilan"
        ) +
        '" ilanınız hakkında bilgi almak istiyorum.' +
        "\n\n" +
        "İlan bağlantısı: " +
        window.location.origin +
        "/ilan/" +
        ilan.id;


    return (
        "https://wa.me/" +
        telefon +
        "?text=" +
        encodeURIComponent(
            mesaj
        )
    );
}


/* ============================================================
   21. WHATSAPP BUTONU
   ============================================================ */

function whatsappButonuHtml(
    ilan
) {

    const girisYaptiMi =
        document.body.dataset?.uyeGiris === "1";


    /*
       Kullanıcı giriş yapmadıysa
       kayıt sayfasına yönlendir.
    */

    if (!girisYaptiMi) {

        return `
            <a
                href="${KAYIT_URL}"
                class="btn-wp-aracilik uye-giris-gerekli"
            >
                🔐 İletişim için kaydol
            </a>
        `;
    }


    /*
       Kullanıcı giriş yapmış fakat
       telefon bilgisi yoksa.
    */

    if (
        !ilanIletisimVarMi(
            ilan
        )
    ) {

        return `
            <a
                href="#"
                class="btn-wp-aracilik"
                onclick="return false;"
                style="background:#777;"
            >
                📞 Telefon yok
            </a>
        `;
    }


    return `
        <a
            href="${whatsappLinkOlustur(ilan)}"
            class="btn-wp-aracilik"
            target="_blank"
            rel="noopener noreferrer"
        >
            💬 WhatsApp
        </a>
    `;
}


/* ============================================================
   22. VİTRİN WHATSAPP
   ============================================================ */

function vitrinButonuGuncelle(
    elementId,
    ilan
) {

    const btn =
        document.getElementById(
            elementId
        );


    if (!btn) {
        return;
    }


    const girisYaptiMi =
        document.body.dataset?.uyeGiris === "1";


    if (!girisYaptiMi) {

        btn.href =
            KAYIT_URL;

        btn.textContent =
            "🔐 İletişim için kaydol";

        btn.style.backgroundColor =
            "#e67e22";

        btn.removeAttribute(
            "target"
        );

        btn.removeAttribute(
            "rel"
        );

        return;
    }


    if (
        !ilanIletisimVarMi(
            ilan
        )
    ) {

        btn.href =
            "#";

        btn.textContent =
            "📞 Telefon yok";

        btn.style.backgroundColor =
            "#777";

        btn.removeAttribute(
            "target"
        );

        btn.removeAttribute(
            "rel"
        );

        return;
    }


    btn.href =
        whatsappLinkOlustur(
            ilan
        );

    btn.target =
        "_blank";

    btn.rel =
        "noopener noreferrer";

    btn.textContent =
        "💬 WhatsApp";

    btn.style.backgroundColor =
        "#20bf6b";
}


/* ============================================================
   23. VİTRİN KARTI
   ============================================================ */

function vitrinKartiniGuncelle(
    ilan,
    sagMi = false
) {

    if (!ilan) {
        return;
    }


    const ek =
        sagMi
            ? "_sag"
            : "";


    const isimEl =
        document.getElementById(
            "urun_isim" +
            ek
        );


    const kodEl =
        document.getElementById(
            "urun_kod" +
            ek
        );


    const fiyatEl =
        document.getElementById(
            "urun_fiyat" +
            ek
        );


    const resimEl =
        document.getElementById(
            "urun_resim" +
            ek
        );


    const linkResimEl =
        document.getElementById(
            "urun_link_resim" +
            ek
        );


    const linkIsimEl =
        document.getElementById(
            "urun_link_isim" +
            ek
        );


    const teknikEl =
        document.getElementById(
            "urun_teknik_detay" +
            ek
        );


    const rozetEl =
        document.getElementById(
            "urun_rozet" +
            ek
        );


    const baslik =
        ilan.baslik ||
        ilan.ad ||
        "İlan";


    if (isimEl) {

        isimEl.textContent =
            baslik;
    }


    if (kodEl) {

        kodEl.textContent =
            ilan.ilan_kodu ||
            ilan.kod ||
            "--";
    }


    if (fiyatEl) {

        fiyatEl.textContent =
            sayiFormatla(
                ilan.fiyat
            ) +
            " TL";
    }


    if (resimEl) {

        resimEl.src =
            ilanKapakResmi(
                ilan
            );


        resimEl.onerror =
            function() {

                this.onerror = null;

                this.src =
                    VARSAYILAN_RESIM;
            };
    }


    const ilanUrl =
        "/ilan/" +
        encodeURIComponent(
            ilan.id
        );


    if (linkResimEl) {

        linkResimEl.href =
            ilanUrl;
    }


    if (linkIsimEl) {

        linkIsimEl.href =
            ilanUrl;
    }


    if (teknikEl) {

        teknikEl.innerHTML =
            teknikDetayOlustur(
                ilan
            );
    }


    if (rozetEl) {

        const rozet =
            rozetBilgisi(
                ilan
            );


        rozetEl.className =
            "kart-rozet " +
            rozet.sinif;


        rozetEl.textContent =
            rozet.metin;
    }


    vitrinButonuGuncelle(
        sagMi
            ? "urun_wp_link_sag"
            : "urun_wp_link",
        ilan
    );
}


/* ============================================================
   24. VİTRİN
   ============================================================ */

function vitrinGuncelle(
    idx,
    liste = null
) {

    const kaynak =
        Array.isArray(liste)
            ? liste
            : (
                Array.isArray(
                    filtrelenmisUrunler
                )
                    ? filtrelenmisUrunler
                    : urunler
            );


    if (
        !Array.isArray(
            kaynak
        ) ||
        kaynak.length === 0
    ) {

        return;
    }


    if (
        idx < 0 ||
        idx >= kaynak.length
    ) {

        idx = 0;
    }


    urun_index =
        idx;


    const solIlan =
        kaynak[idx];


    vitrinKartiniGuncelle(
        solIlan,
        false
    );


    if (
        kaynak.length > 1
    ) {

        const sagIdx =
            (
                idx + 1
            ) %
            kaynak.length;


        const sagIlan =
            kaynak[sagIdx];


        vitrinKartiniGuncelle(
            sagIlan,
            true
        );


        return;
    }


    const sagIsim =
        document.getElementById(
            "urun_isim_sag"
        );


    const sagKod =
        document.getElementById(
            "urun_kod_sag"
        );


    const sagFiyat =
        document.getElementById(
            "urun_fiyat_sag"
        );


    const sagResim =
        document.getElementById(
            "urun_resim_sag"
        );


    const sagTeknik =
        document.getElementById(
            "urun_teknik_detay_sag"
        );


    const sagRozet =
        document.getElementById(
            "urun_rozet_sag"
        );


    if (sagIsim) {

        sagIsim.textContent =
            "Başka ilan bekleniyor...";
    }


    if (sagKod) {

        sagKod.textContent =
            "--";
    }


    if (sagFiyat) {

        sagFiyat.textContent =
            "0 TL";
    }


    if (sagResim) {

        sagResim.src =
            VARSAYILAN_RESIM;
    }


    if (sagTeknik) {

        sagTeknik.innerHTML =
            "Başka ilan bulunmuyor.";
    }


    if (sagRozet) {

        sagRozet.textContent =
            "--";

        sagRozet.className =
            "kart-rozet kazali";
    }


    const wp =
        document.getElementById(
            "urun_wp_link_sag"
        );


    if (wp) {

        wp.href =
            KAYIT_URL;

        wp.textContent =
            "🔐 İletişim için kaydol";

        wp.style.backgroundColor =
            "#e67e22";

        wp.removeAttribute(
            "target"
        );

        wp.removeAttribute(
            "rel"
        );
    }
}


/* ============================================================
   25. İLAN KARTLARI
   ============================================================ */

function ilanlariDiz(
    liste
) {

    const izgara =
        document.getElementById(
            "ilanListesiIzgara"
        );


    if (!izgara) {
        return;
    }


    izgara.innerHTML =
        "";


    if (
        !Array.isArray(
            liste
        ) ||
        liste.length === 0
    ) {

        izgara.innerHTML = `
            <div class="ilan-bulunamadi">
                Kriterlere uygun ilan bulunamadı.
            </div>
        `;

        return;
    }


    liste.forEach(
        function(ilan) {

            if (!ilan) {
                return;
            }


            const kategori =
                kategoriNormalize(
                    ilan.kategori
                );


            const renk =
                kategoriRengi(
                    kategori
                );


            const ikon =
                kategoriIkonu(
                    kategori
                );


            const kategoriAdi =
                kategoriGorunenAdi(
                    kategori
                );


            const resim =
                ilanKapakResmi(
                    ilan
                );


            const detay =
                teknikDetayOlustur(
                    ilan
                );


            const rozet =
                rozetBilgisi(
                    ilan
                );


            const baslik =
                ilan.baslik ||
                ilan.ad ||
                "İlan";


            const kod =
                ilan.ilan_kodu ||
                ilan.kod ||
                "--";


            const fiyat =
                sayiFormatla(
                    ilan.fiyat
                );


            const ilanUrl =
                "/ilan/" +
                encodeURIComponent(
                    ilan.id
                );


            const kartHtml = `

                <div
                    class="arac-kart"
                    data-ilan-id="${ilan.id}"
                >

                    <div
                        class="kart-kategori"
                        style="background:${renk};"
                    >
                        ${ikon}
                        ${kategoriAdi}
                    </div>


                    <a
                        href="${ilanUrl}"
                        class="kart-resim-link"
                    >

                        <img
                            src="${resim}"
                            class="kart-ana-resim"
                            alt="${baslik}"
                            loading="lazy"
                            onerror="
                                this.onerror=null;
                                this.src='${VARSAYILAN_RESIM}';
                            "
                        >

                    </a>


                    <div class="kart-icerik">

                        <div class="vitrin-etiket-satir">

                            <a
                                href="${ilanUrl}"
                                class="vitrin-baslik-link"
                            >

                                <h4>
                                    ${baslik}
                                </h4>

                            </a>


                            <span class="v-kod">
                                ${kod}
                            </span>

                        </div>


                        ${
                            detay
                                ? `
                                    <div class="kart-teknik">
                                        ${detay}
                                    </div>
                                  `
                                : ""
                        }


                        <div class="kart-rozet-alani">

                            <span
                                class="kart-rozet ${rozet.sinif}"
                            >
                                ${rozet.metin}
                            </span>

                        </div>


                        <div class="kart-alt-fiyat-grup">

                            <span class="k-fiyat">
                                ${fiyat} TL
                            </span>

                            ${whatsappButonuHtml(
                                ilan
                            )}

                        </div>

                    </div>

                </div>
            `;


            izgara.insertAdjacentHTML(
                "beforeend",
                kartHtml
            );
        }
    );
}


/* ============================================================
   26. ARAMA METNİ
   ============================================================ */

function ilanAramaMetni(
    ilan
) {

    if (!ilan) {
        return "";
    }


    const detay =
        ilan.detay ||
        {};


    const alanlar = [

        ilan.baslik,
        ilan.ad,
        ilan.kategori,
        ilan.aciklama,
        ilan.ilan_kodu,
        ilan.ilan_sahibi,

        detay.marka,
        detay.model,
        detay.yil,
        detay.km,
        detay.yakit,
        detay.vites,
        detay.kasa_tipi,
        detay.motor_hacmi,
        detay.motor_gucu,
        detay.renk,
        detay.hasar_durumu,

        detay.emlak_tipi,
        detay.ilan_durumu,
        detay.bina_yasi,
        detay.metrekare,
        detay.oda_sayisi,
        detay.salon_sayisi,
        detay.bulundugu_kat,
        detay.isitma,

        detay.isyeri_tipi,

        detay.imar_durumu,
        detay.ada_no,
        detay.parsel_no,
        detay.yol_durumu,
        detay.cephe,
        detay.kaks,
        detay.emsal,
        detay.gabari,
        detay.merkeze_uzaklik

    ];


    alanlar.push(

        ilan.marka,
        ilan.model,
        ilan.yil,
        ilan.km,
        ilan.yakit,
        ilan.vites,
        ilan.kasa_tipi,
        ilan.renk,

        ilan.emlak_tipi,
        ilan.ilan_durumu,
        ilan.bina_yasi,
        ilan.metrekare,
        ilan.oda_sayisi,
        ilan.bulundugu_kat,
        ilan.isitma,

        ilan.isyeri_tipi,
        ilan.isyeri_metrekare,
        ilan.isyeri_oda_sayisi,
        ilan.isyeri_kat,

        ilan.imar_durumu,
        ilan.ada_no,
        ilan.parsel_no,
        ilan.yol_durumu,
        ilan.arsa_cephe
    );


    return alanlar
        .filter(
            function(degerDegeri) {

                return (
                    degerDegeri !== null &&
                    degerDegeri !== undefined &&
                    String(
                        degerDegeri
                    ).trim() !== ""
                );
            }
        )
        .join(" ")
        .toLocaleLowerCase(
            "tr-TR"
        );
}


/* ============================================================
   27. FİLTRELEME VE SIRALAMA
   ============================================================ */

function filtreleVeSirala() {

    const aramaEl =
        document.getElementById(
            "pazarAra"
        );


    const kazaEl =
        document.getElementById(
            "pazarKaza"
        );


    const siraEl =
        document.getElementById(
            "pazarSira"
        );


    const kategoriEl =
        document.getElementById(
            "pazarKategori"
        );


    const arama =
        (
            aramaEl?.value ||
            ""
        )
            .toLocaleLowerCase(
                "tr-TR"
            )
            .trim();


    const kaza =
        kazaEl?.value ||
        "hepsi";


    const sira =
        siraEl?.value ||
        "varsayilan";


    const kategori =
        kategoriNormalize(
            kategoriEl?.value ||
            "hepsi"
        );


    let liste =
        Array.isArray(
            urunler
        )
            ? [...urunler]
            : [];


    let filtrelenmis =
        liste.filter(
            function(ilan) {

                if (!ilan) {
                    return false;
                }


                const ilanKategori =
                    kategoriNormalize(
                        ilan.kategori
                    );


                const metin =
                    ilanAramaMetni(
                        ilan
                    );


                const metinUyumu =
                    !arama ||
                    metin.includes(
                        arama
                    );


                const kategoriUyumu =
                    kategori === "hepsi" ||
                    !kategori ||
                    ilanKategori ===
                        kategori;


                let kazaUyumu =
                    true;


                if (
                    ilanKategori ===
                    "Otomobil"
                ) {

                    const hasarli =
                        Number(
                            ilanDegeri(
                                ilan,
                                "degisen"
                            ) || 0
                        ) === 1 ||

                        Number(
                            ilanDegeri(
                                ilan,
                                "boya"
                            ) || 0
                        ) === 1 ||

                        Number(
                            ilanDegeri(
                                ilan,
                                "tramer"
                            ) || 0
                        ) === 1;


                    if (
                        kaza ===
                        "hatasiz"
                    ) {

                        kazaUyumu =
                            !hasarli;
                    }


                    else if (
                        kaza ===
                        "kazali"
                    ) {

                        kazaUyumu =
                            hasarli;
                    }

                }


                return (
                    metinUyumu &&
                    kategoriUyumu &&
                    kazaUyumu
                );
            }
        );


    /* FİYAT ARTAN */

    if (
        sira ===
        "fiyatArtan"
    ) {

        filtrelenmis.sort(
            function(a, b) {

                return (
                    Number(
                        a.fiyat || 0
                    ) -
                    Number(
                        b.fiyat || 0
                    )
                );
            }
        );
    }


    /* FİYAT AZALAN */

    else if (
        sira ===
        "fiyatAzalan"
    ) {

        filtrelenmis.sort(
            function(a, b) {

                return (
                    Number(
                        b.fiyat || 0
                    ) -
                    Number(
                        a.fiyat || 0
                    )
                );
            }
        );
    }


    /* YENİ MODEL YILI */

    else if (
        sira ===
        "yilYeni"
    ) {

        filtrelenmis.sort(
            function(a, b) {

                return (
                    Number(
                        ilanDegeri(
                            b,
                            "yil"
                        ) || 0
                    ) -
                    Number(
                        ilanDegeri(
                            a,
                            "yil"
                        ) || 0
                    )
                );
            }
        );
    }


    /* DÜŞÜK KM */

    else if (
        sira ===
        "kmDusuk"
    ) {

        filtrelenmis.sort(
            function(a, b) {

                return (
                    Number(
                        ilanDegeri(
                            a,
                            "km"
                        ) || 0
                    ) -
                    Number(
                        ilanDegeri(
                            b,
                            "km"
                        ) || 0
                    )
                );
            }
        );
    }


    filtrelenmisUrunler =
        filtrelenmis;


    ilanlariDiz(
        filtrelenmis
    );


    if (
        filtrelenmis.length > 0
    ) {

        urun_index =
            0;


        vitrinGuncelle(
            0,
            filtrelenmis
        );
    }
}


/* ============================================================
   28. API'DEN İLANLARI AL
   ============================================================ */

async function ilanlariYukle() {

    const izgara =
        document.getElementById(
            "ilanListesiIzgara"
        );


    try {

        const response =
            await fetch(
                "/api/ilanlar",
                {
                    method: "GET",
                    headers: {
                        "Accept":
                            "application/json"
                    },
                    cache:
                        "no-store"
                }
            );


        if (!response.ok) {

            throw new Error(
                "API HTTP " +
                response.status
            );
        }


        const data =
            await response.json();


        let liste =
            data;


        if (
            data &&
            !Array.isArray(data) &&
            Array.isArray(
                data.ilanlar
            )
        ) {

            liste =
                data.ilanlar;
        }


        if (
            data &&
            !Array.isArray(data) &&
            Array.isArray(
                data.data
            )
        ) {

            liste =
                data.data;
        }


        if (
            !Array.isArray(
                liste
            )
        ) {

            throw new Error(
                "API geçerli ilan listesi döndürmedi."
            );
        }


        urunler =
            liste
                .filter(Boolean)
                .map(
                    function(ilan) {

                        ilan.kategori =
                            kategoriNormalize(
                                ilan.kategori
                            );

                        return ilan;
                    }
                );


        filtrelenmisUrunler =
            [...urunler];


        console.log(
            "API ilan sayısı:",
            urunler.length
        );


        if (
            urunler.length === 0
        ) {

            ilanlariDiz(
                []
            );

            return;
        }


        ilanlariDiz(
            urunler
        );


        urun_index =
            0;


        vitrinGuncelle(
            0,
            urunler
        );

    }
    catch (hata) {

        console.error(
            "İlanlar yüklenirken hata:",
            hata
        );


        if (izgara) {

            izgara.innerHTML = `

                <div
                    class="ilan-bulunamadi"
                    style="
                        color:#ff7675;
                        text-align:center;
                        padding:20px;
                    "
                >

                    İlanlar yüklenirken hata oluştu.

                    <br>

                    <small>
                        ${hata.message}
                    </small>

                </div>
            `;
        }
    }
}


/* ============================================================
   29. MARKA MODEL YÜKLE
   ============================================================ */

function modelleriYukle(
    mevcutModel = ""
) {

    const markaEl =
        document.getElementById(
            "marka"
        );


    const modelEl =
        document.getElementById(
            "model"
        );


    if (!modelEl) {
        return;
    }


    const marka =
        markaEl?.value ||
        "";


    modelEl.innerHTML =
        "";


    const bos =
        document.createElement(
            "option"
        );


    bos.value =
        "";


    bos.textContent =
        "Model Seçiniz";


    modelEl.appendChild(
        bos
    );


    const modeller =
        modelEslesmeleri[
            marka
        ] || [];


    if (
        !marka ||
        modeller.length === 0
    ) {

        modelEl.disabled =
            true;

        return;
    }


    modelEl.disabled =
        false;


    modeller.forEach(
        function(modelAdi) {

            const option =
                document.createElement(
                    "option"
                );


            option.value =
                modelAdi;


            option.textContent =
                modelAdi;


            if (
                mevcutModel &&
                modelAdi ===
                    mevcutModel
            ) {

                option.selected =
                    true;
            }


            modelEl.appendChild(
                option
            );
        }
    );
}


/* ============================================================
   30. ELEMAN GÖSTER / GİZLE
   ============================================================ */

function alanGoster(
    id,
    display
) {

    const el =
        document.getElementById(
            id
        );


    if (!el) {
        return;
    }


    el.style.display =
        display;
}


/* ============================================================
   31. REQUIRED TEMİZLE
   ============================================================ */

function dinamikRequiredTemizle() {

    const alanlar =
        document.querySelectorAll(
            ".dinamik-alan input, " +
            ".dinamik-alan select, " +
            ".dinamik-alan textarea"
        );


    alanlar.forEach(
        function(el) {

            el.removeAttribute(
                "required"
            );
        }
    );
}


/* ============================================================
   32. ARSA / TARLA ÖZEL ALANLARINI AYARLA
   ============================================================ */

function arsaTarlaAlanlariniDuzenle(
    kategori
) {

    /*
       Bu fonksiyon mevcut HTML'de
       bulunan alanları isimlerinden bulur.

       Böylece HTML'de ayrıca ID verilmemiş
       alanlarda da çalışabilir.
    */

    const alan =
        document.getElementById(
            "alan-arsa"
        );


    if (!alan) {
        return;
    }


    const elemanlar =
        alan.querySelectorAll(
            "input, select"
        );


    elemanlar.forEach(
        function(el) {

            el.closest(
                ".form-sutun"
            )?.style &&
            (el.closest(
                ".form-sutun"
            ).style.display =
                "");
        }
    );


    if (
        kategori === "Arsa"
    ) {

        /*
           Arsa:
           imar + cephe + KAKS + emsal +
           gabari + kat karşılığı + ifrazlı
        */

        alan.querySelectorAll(
            'select[name="imar_durumu"], ' +
            'input[name="kaks"], ' +
            'input[name="emsal"], ' +
            'input[name="gabari"], ' +
            'input[name="arsa_cephe"]'
        ).forEach(
            function(el) {

                const satir =
                    el.closest(
                        ".form-sutun"
                    );

                if (satir) {
                    satir.style.display =
                        "";
                }
            }
        );


        /*
           Tarla'ya ait olmayan checkboxlar:
           kat karşılığı
           ifrazlı
        */

        alan.querySelectorAll(
            'input[name="kat_karsiligi"], ' +
            'input[name="ifrazli"]'
        ).forEach(
            function(el) {

                const label =
                    el.closest(
                        "label"
                    );

                if (label) {
                    label.style.display =
                        "";
                }
            }
        );


        return;
    }


    if (
        kategori === "Tarla"
    ) {

        /*
           Tarla için:
           İmar bilgisi yok.
           Cephe yok.
           KAKS / Emsal / Gabari yok.
           Kat karşılığı yok.
           İfrazlı yok.
        */

        alan.querySelectorAll(
            'select[name="imar_durumu"], ' +
            'input[name="kaks"], ' +
            'input[name="emsal"], ' +
            'input[name="gabari"], ' +
            'input[name="arsa_cephe"]'
        ).forEach(
            function(el) {

                const satir =
                    el.closest(
                        ".form-sutun"
                    );

                if (satir) {
                    satir.style.display =
                        "none";
                }
            }
        );


        alan.querySelectorAll(
            'input[name="kat_karsiligi"], ' +
            'input[name="ifrazli"]'
        ).forEach(
            function(el) {

                const label =
                    el.closest(
                        "label"
                    );

                if (label) {
                    label.style.display =
                        "none";
                }

                el.checked =
                    false;
            }
        );
    }
}


/* ============================================================
   33. FORM ALANLARINI GÜNCELLE
   ============================================================ */

function formAlanlariniGuncelle() {

    const kategoriEl =
        document.getElementById(
            "kategori_secim"
        );


    if (!kategoriEl) {
        return;
    }


    const kategori =
        kategoriNormalize(
            kategoriEl.value
        );


    const alanlar = [

        "alan-otomobil-ozel",
        "alan-otomobil-teknik",
        "alan-otomobil-check",

        "alan-emlak",
        "alan-emlak-ozel",
        "alan-emlak-teknik",
        "alan-emlak-check",

        "alan-dukkan",
        "alan-dukkan-ozel",
        "alan-dukkan-teknik",
        "alan-dukkan-check",

        "alan-isyeri",

        "alan-arsa",
        "alan-arsa-ozel",
        "alan-arsa-teknik",
        "alan-arsa-check"

    ];


    alanlar.forEach(
        function(id) {

            alanGoster(
                id,
                "none"
            );
        }
    );


    dinamikRequiredTemizle();


    /* ========================================================
       OTOMOBİL
       ======================================================== */

    if (
        kategori ===
        "Otomobil"
    ) {

        alanGoster(
            "alan-otomobil-ozel",
            "block"
        );


        alanGoster(
            "alan-otomobil-teknik",
            "block"
        );


        alanGoster(
            "alan-otomobil-check",
            "flex"
        );


        const marka =
            document.getElementById(
                "marka"
            );


        const model =
            document.getElementById(
                "model"
            );


        const yil =
            document.getElementById(
                "yil_oto"
            );


        const km =
            document.getElementById(
                "km_oto"
            );


        marka?.setAttribute(
            "required",
            "required"
        );


        model?.setAttribute(
            "required",
            "required"
        );


        yil?.setAttribute(
            "required",
            "required"
        );


        km?.setAttribute(
            "required",
            "required"
        );


        modelleriYukle();

        return;
    }


    /* ========================================================
       DAİRE
       ======================================================== */

    if (
        kategori ===
        "Daire"
    ) {

        alanGoster(
            "alan-emlak",
            "block"
        );


        alanGoster(
            "alan-emlak-ozel",
            "flex"
        );


        alanGoster(
            "alan-emlak-teknik",
            "block"
        );


        alanGoster(
            "alan-emlak-check",
            "flex"
        );


        document
            .getElementById(
                "bina_tipi"
            )
            ?.setAttribute(
                "required",
                "required"
            );


        return;
    }


    /* ========================================================
       EV
       ======================================================== */

    if (
        kategori ===
        "Ev"
    ) {

        alanGoster(
            "alan-emlak",
            "block"
        );


        alanGoster(
            "alan-emlak-ozel",
            "flex"
        );


        alanGoster(
            "alan-emlak-teknik",
            "block"
        );


        alanGoster(
            "alan-emlak-check",
            "flex"
        );


        return;
    }


    /* ========================================================
       DÜKKAN
       ======================================================== */

    if (
        kategori ===
        "Dukkan"
    ) {

        alanGoster(
            "alan-dukkan",
            "block"
        );


        alanGoster(
            "alan-dukkan-ozel",
            "flex"
        );


        alanGoster(
            "alan-dukkan-teknik",
            "block"
        );


        alanGoster(
            "alan-dukkan-check",
            "flex"
        );


        return;
    }


    /* ========================================================
       ARSA
       ======================================================== */

    if (
        kategori ===
        "Arsa"
    ) {

        alanGoster(
            "alan-arsa",
            "block"
        );


        alanGoster(
            "alan-arsa-ozel",
            "flex"
        );


        alanGoster(
            "alan-arsa-teknik",
            "block"
        );


        alanGoster(
            "alan-arsa-check",
            "flex"
        );


        arsaTarlaAlanlariniDuzenle(
            "Arsa"
        );


        return;
    }


    /* ========================================================
       TARLA
       ======================================================== */

    if (
        kategori ===
        "Tarla"
    ) {

        alanGoster(
            "alan-arsa",
            "block"
        );


        alanGoster(
            "alan-arsa-ozel",
            "flex"
        );


        alanGoster(
            "alan-arsa-teknik",
            "block"
        );


        alanGoster(
            "alan-arsa-check",
            "flex"
        );


        arsaTarlaAlanlariniDuzenle(
            "Tarla"
        );


        return;
    }
}


/* ============================================================
   34. FORM BAŞLAT
   ============================================================ */

function kategoriFormunuBaslat() {

    const kategori =
        document.getElementById(
            "kategori_secim"
        );


    if (!kategori) {
        return;
    }


    formAlanlariniGuncelle();


    if (
        !kategori.dataset
            .scriptHazir
    ) {

        kategori.addEventListener(
            "change",
            function() {

                formAlanlariniGuncelle();

            }
        );


        kategori.dataset
            .scriptHazir =
            "1";
    }


    const marka =
        document.getElementById(
            "marka"
        );


    if (
        marka &&
        !marka.dataset
            .scriptHazir
    ) {

        marka.addEventListener(
            "change",
            function() {

                modelleriYukle();

            }
        );


        marka.dataset
            .scriptHazir =
            "1";
    }
}


/* ============================================================
   35. YENİ FOTOĞRAF SEÇİMİ
   ============================================================ */

function fotoOnizlemeKur(
    inputId,
    previewId,
    durumId,
    maxFoto = MAX_FOTO
) {

    const input =
        document.getElementById(
            inputId
        );


    const onizleme =
        document.getElementById(
            previewId
        );


    const durum =
        document.getElementById(
            durumId
        );


    if (
        !input ||
        !onizleme ||
        !durum
    ) {

        return;
    }


    if (
        input.dataset
            .fotoHazir
    ) {

        return;
    }


    input.addEventListener(
        "change",
        function() {

            let files =
                Array.from(
                    input.files || []
                );


            if (
                files.length >
                maxFoto
            ) {

                files =
                    files.slice(
                        0,
                        maxFoto
                    );


                try {

                    const dt =
                        new DataTransfer();


                    files.forEach(
                        function(file) {

                            dt.items.add(
                                file
                            );
                        }
                    );


                    input.files =
                        dt.files;

                }
                catch (hata) {

                    console.warn(
                        "Dosya listesi güncellenemedi:",
                        hata
                    );
                }
            }


            onizleme.innerHTML =
                "";


            if (
                files.length === 0
            ) {

                durum.style.display =
                    "none";

                return;
            }


            durum.style.display =
                "block";


            durum.style.background =
                "rgba(32,191,107,.12)";


            durum.style.border =
                "1px solid rgba(32,191,107,.45)";


            durum.style.color =
                "#20bf6b";


            durum.textContent =
                "✓ " +
                files.length +
                "/" +
                maxFoto +
                " fotoğraf seçildi.";


            files.forEach(
                function(
                    file,
                    index
                ) {

                    const kart =
                        document.createElement(
                            "div"
                        );


                    kart.style.position =
                        "relative";


                    kart.style.background =
                        "#1d222c";


                    kart.style.padding =
                        "5px";


                    kart.style.borderRadius =
                        "8px";


                    kart.style.border =
                        "1px solid rgba(255,255,255,.08)";


                    kart.style.overflow =
                        "hidden";


                    const img =
                        document.createElement(
                            "img"
                        );


                    img.alt =
                        file.name;


                    img.style.width =
                        "100%";


                    img.style.height =
                        "85px";


                    img.style.objectFit =
                        "cover";


                    img.style.display =
                        "block";


                    img.style.borderRadius =
                        "6px";


                    const no =
                        document.createElement(
                            "span"
                        );


                    no.textContent =
                        index + 1;


                    no.style.position =
                        "absolute";


                    no.style.top =
                        "7px";


                    no.style.left =
                        "7px";


                    no.style.width =
                        "21px";


                    no.style.height =
                        "21px";


                    no.style.lineHeight =
                        "21px";


                    no.style.textAlign =
                        "center";


                    no.style.borderRadius =
                        "50%";


                    no.style.background =
                        "#0baa55";


                    no.style.color =
                        "#fff";


                    no.style.fontWeight =
                        "900";


                    no.style.fontSize =
                        "11px";


                    const ad =
                        document.createElement(
                            "div"
                        );


                    ad.textContent =
                        file.name;


                    ad.style.color =
                        "#ddd";


                    ad.style.fontSize =
                        "9px";


                    ad.style.marginTop =
                        "4px";


                    ad.style.whiteSpace =
                        "nowrap";


                    ad.style.overflow =
                        "hidden";


                    ad.style.textOverflow =
                        "ellipsis";


                    kart.appendChild(
                        img
                    );


                    kart.appendChild(
                        no
                    );


                    kart.appendChild(
                        ad
                    );


                    onizleme.appendChild(
                        kart
                    );


                    const reader =
                        new FileReader();


                    reader.onload =
                        function(event) {

                            img.src =
                                event.target.result;
                        };


                    reader.readAsDataURL(
                        file
                    );

                }
            );

        });


    input.dataset
        .fotoHazir =
        "1";
}


/* ============================================================
   36. DOM HAZIR
   ============================================================ */

document.addEventListener(
    "DOMContentLoaded",
    function() {

        /*
           Kullanıcının giriş durumunu
           body üzerinden okuyalım.
        */

        const uyeVar =
            document.querySelector(
                ".uye-bilgi-etiketi"
            );


        document.body.dataset
            .uyeGiris =
            uyeVar
                ? "1"
                : "0";


        /*
           Formlar.
        */

        kategoriFormunuBaslat();


        /*
           Yeni ilan fotoğrafı.
        */

        fotoOnizlemeKur(
            "resimler",
            "onizleme",
            "fotoSecimDurumu",
            MAX_FOTO
        );


        /*
           Güncelleme sayfasında
           mevcut fotoğraflar nedeniyle
           ayrı önizleme alanı olabilir.
        */

        const yeniFoto =
            document.getElementById(
                "yeniFotoOnizleme"
            );


        const mevcutInput =
            document.getElementById(
                "resimler"
            );


        if (
            yeniFoto &&
            mevcutInput
        ) {

            fotoOnizlemeKur(
                "resimler",
                "yeniFotoOnizleme",
                "fotoSecimDurumu",
                Number(
                    mevcutInput
                        .dataset
                        .kalan ||
                    MAX_FOTO
                )
            );
        }


        /*
           Ana sayfa ilan ızgarası.
        */

        const izgara =
            document.getElementById(
                "ilanListesiIzgara"
            );


        if (!izgara) {
            return;
        }


        /*
           İlanları getir.
        */

        ilanlariYukle();


        /*
           SONRAKİ
        */

        const sonraki =
            document.getElementById(
                "sonraki"
            );


        if (sonraki) {

            sonraki.addEventListener(
                "click",
                function() {

                    const kaynak =
                        filtrelenmisUrunler;


                    if (
                        !Array.isArray(
                            kaynak
                        ) ||
                        kaynak.length === 0
                    ) {

                        return;
                    }


                    urun_index =
                        (
                            urun_index +
                            1
                        ) %
                        kaynak.length;


                    vitrinGuncelle(
                        urun_index,
                        kaynak
                    );
                }
            );
        }


        /*
           ÖNCEKİ
        */

        const onceki =
            document.getElementById(
                "onceki"
            );


        if (onceki) {

            onceki.addEventListener(
                "click",
                function() {

                    const kaynak =
                        filtrelenmisUrunler;


                    if (
                        !Array.isArray(
                            kaynak
                        ) ||
                        kaynak.length === 0
                    ) {

                        return;
                    }


                    urun_index =
                        (
                            urun_index -
                            1 +
                            kaynak.length
                        ) %
                        kaynak.length;


                    vitrinGuncelle(
                        urun_index,
                        kaynak
                    );
                }
            );
        }


        /*
           RASTGELE
        */

        const rastgele =
            document.getElementById(
                "rastgele"
            );


        if (rastgele) {

            rastgele.addEventListener(
                "click",
                function() {

                    const kaynak =
                        filtrelenmisUrunler;


                    if (
                        !Array.isArray(
                            kaynak
                        ) ||
                        kaynak.length <= 1
                    ) {

                        return;
                    }


                    let yeniIndex;


                    do {

                        yeniIndex =
                            Math.floor(
                                Math.random() *
                                kaynak.length
                            );

                    }

                    while (
                        yeniIndex ===
                        urun_index
                    );


                    urun_index =
                        yeniIndex;


                    vitrinGuncelle(
                        urun_index,
                        kaynak
                    );
                }
            );
        }


        /*
           ARAMA
        */

        const arama =
            document.getElementById(
                "pazarAra"
            );


        if (arama) {

            arama.addEventListener(
                "input",
                filtreleVeSirala
            );
        }


        /*
           KATEGORİ
        */

        const kategori =
            document.getElementById(
                "pazarKategori"
            );


        if (kategori) {

            kategori.addEventListener(
                "change",
                filtreleVeSirala
            );
        }


        /*
           KAZA / HASAR
        */

        const kaza =
            document.getElementById(
                "pazarKaza"
            );


        if (kaza) {

            kaza.addEventListener(
                "change",
                filtreleVeSirala
            );
        }


        /*
           SIRALAMA
        */

        const sira =
            document.getElementById(
                "pazarSira"
            );


        if (sira) {

            sira.addEventListener(
                "change",
                filtreleVeSirala
            );
        }

    }
);


/* ============================================================
   37. GLOBAL ERİŞİM
   ============================================================ */

window.kategoriNormalize =
    kategoriNormalize;

window.modelleriYukle =
    modelleriYukle;

window.formAlanlariniGuncelle =
    formAlanlariniGuncelle;

window.filtreleVeSirala =
    filtreleVeSirala;

window.vitrinGuncelle =
    vitrinGuncelle;

window.detayResimDegistir =
    detayResimDegistir;


/* ============================================================
   38. DETAY FOTOĞRAF DEĞİŞTİR
   ============================================================ */

function detayResimDegistir(
    element
) {

    const ana =
        document.getElementById(
            "anaDetayGorsel"
        );


    if (
        !ana ||
        !element
    ) {

        return;
    }


    const yeniUrl =
        element.dataset.resimUrl ||
        element.src;


    ana.src =
        yeniUrl;


    document
        .querySelectorAll(
            ".galeri-kucuk"
        )
        .forEach(
            function(el) {

                el.style.borderColor =
                    "transparent";


                el.style.opacity =
                    "0.60";
            }
        );


    element.style.borderColor =
        "#ff9f43";


    element.style.opacity =
        "1";
}


/* ============================================================
   SON
   ============================================================ */