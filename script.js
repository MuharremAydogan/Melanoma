
function veritabaninaYaz(veri) {
    fetch('http://127.0.0.1:3000/veriEkle', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(veri),
    })
      .then(response => response.json())
      .then(sonuc => {
        console.log(sonuc);
      })
      .catch(hata => {
        console.error('Hata:', hata);
      });
  }
  
  function formuIsleVeMongoDBEkle() {
    var ad = document.getElementById("ad").value;
    var soyad = document.getElementById("soyad").value;
    var tc = document.getElementById("tc").value;
    var telefon = document.getElementById("telefon").value;
    var foto1 = document.getElementById("foto1").files[0];
    var foto2 = document.getElementById("foto2").files[0];
    var foto3 = document.getElementById("foto3").files[0];
    var foto4 = document.getElementById("foto4").files[0];
  
    
    window['dizi1'] = [];
    window['dizi2'] = [];
    window['dizi3'] = [];
    window['dizi4'] = [];
  
    // Resim işleme
    function processImagePromise(file, arrayName) {
      return new Promise((resolve, reject) => {
        var okuyucu = new FileReader();
        okuyucu.onload = function (e) {
          var img = new Image();
          img.src = e.target.result;
          img.onload = function () {
            var canvas = document.createElement('canvas');
            canvas.width = 28;
            canvas.height = 28;
            var ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0, 28, 28);
  
            var imageData = ctx.getImageData(0, 0, 28, 28).data;
  
            var normalizeDizi = [];
            for (var i = 0; i < imageData.length; i += 4) {
              var normalizeDeger = (imageData[i] + imageData[i + 1] + imageData[i + 2]) / 3 / 255.0;
              normalizeDizi.push(normalizeDeger);
            }
  
            
            window[arrayName] = normalizeDizi;
            console.log(arrayName, normalizeDizi);
            resolve(); 
          };
        };
        okuyucu.readAsDataURL(file);
      });
    }
  
    
    processImagePromise(foto1, 'dizi1')
      .then(() => processImagePromise(foto2, 'dizi2'))
      .then(() => processImagePromise(foto3, 'dizi3'))
      .then(() => processImagePromise(foto4, 'dizi4'))
      .then(() => {
        
        var yeniVeri = {
          "Ad": ad,
          "Soyad": soyad,
          "TC": tc,
          "Telefon": telefon,
        };
  
        
        for (var i = 1; i <= 4; i++) {
          if (!window['dizi' + i] || window['dizi' + i].length !== 784) {
            console.error('Dizi' + i + ' tanımlı değil veya eleman sayısı hatalı.');
            return; // Hata durumunda işlemi durdur
          }
  
          // Diziyi veri objesine ekleme
          yeniVeri['pixel' + i] = window['dizi' + i];
        }
  
        // Veriyi MongoDB'ye yaz
        veritabaninaYaz(yeniVeri);
      })
      .catch((hata) => {
        console.error('Hata:', hata);
      });
  }
  


  