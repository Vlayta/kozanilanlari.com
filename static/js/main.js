const urunler = [
  {
    kod: "A1",
    ad:"Audi",
    fiyat:300_000,
    resim: "static/resimler/audi.jpeg"
  },
  {
    kod: "A2",
    ad:"BMW",
    fiyat:600_000,
    resim: "static/resimler/bmw.jpeg"
  },
  {
    kod: "A3",
    ad:"Ford",
    fiyat:500_000,
    resim: "static/resimler/ford.jpeg"
  },
  {
    kod: "K01",
    ad:"Kettttt",
    fiyat:570_000,
    resim: "static/resimler/kedi.jpg"
  }  
]

// butonların kontrolünü eline al
const onceki = document.getElementById("onceki")
const sonraki = document.getElementById("sonraki")
const rastgele = document.getElementById("rastgele")

// ürün bilgilerini kontrollerini eline al
const urun_resim = document.getElementById("urun_resim")
const urun_isim = document.getElementById("urun_isim")
const urun_kod = document.getElementById("urun_kod")
const urun_fiyat = document.getElementById("urun_fiyat")

let urun_index = 0

function urun_goster(idx)
{
  const urun = urunler[idx]
  urun_resim.src = urun.resim
  urun_isim.textContent = urun.ad
  urun_kod.textContent = urun.kod
  urun_fiyat.textContent = urun.fiyat
}

function sonrakini_goster(){
  if (urun_index < urunler.length-1){
    urun_index++
  } else{
    urun_index = 0
  }
  urun_goster(urun_index)
}

function oncekini_goster(){
  if (urun_index > 0 ){
    urun_index--
  }else{
    urun_index = urunler.length -1
  }
  urun_goster(urun_index)
}

urun_goster(urun_index)

sonraki.addEventListener("click", sonrakini_goster)
onceki.addEventListener("click", oncekini_goster)
rastgele.addEventListener("click", function (){
  let urun_index_aday ;
  do {
    urun_index_aday = Math.floor(Math.random() * urunler.length)
  } while(urun_index_aday == urun_index)
  urun_index = urun_index_aday
  urun_goster(urun_index)
})




