import numpy as np
import pandas as pd
from pymongo import MongoClient
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout


def model_olustur():
    model = Sequential()
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.20))
    model.add(Dense(7, activation='softmax'))
    model.compile(loss=tf.keras.losses.categorical_crossentropy, optimizer=tf.optimizers.Adam(), metrics=['accuracy'])
    return model


model = model_olustur()



checkpoint_dosyasi = "my_modelweights"

try:
    model.load_weights(checkpoint_dosyasi)
except (FileNotFoundError, ValueError) as e:
    print(f"Hata: Ağırlıklar yüklenirken bir sorun oluştu: {e}")
    exit()

# MongoDB bağlantısı
client = MongoClient("mongodb://localhost:27017/")
db = client["DenemeDB"]
veri_koleksiyonu = db["veris"]

sonuc_koleksiyonu = db["sonuclar"]

# Değerlendirilmiş tc kontrol
degerlendirilen_tc_listesi = set(pd.DataFrame(list(sonuc_koleksiyonu.find({}, {"TC": 1}))).get('TC', []))

# veris koleksiyonundan verileri çek
for veri in veri_koleksiyonu.find():

    if veri["TC"] in degerlendirilen_tc_listesi:
        continue

    Dizi1 = np.array(veri["pixel1"]).reshape(1, 28, 28, 1)
    Dizi2 = np.array(veri["pixel2"]).reshape(1, 28, 28, 1)
    Dizi3 = np.array(veri["pixel3"]).reshape(1, 28, 28, 1)
    Dizi4 = np.array(veri["pixel4"]).reshape(1, 28, 28, 1)

    # tahmin
    tahmin1 = model.predict(Dizi1)
    tahmin2 = model.predict(Dizi2)
    tahmin3 = model.predict(Dizi3)
    tahmin4 = model.predict(Dizi4)                   

    en_buyuk_indeks1 = np.argmax(tahmin1)
    en_buyuk_indeks2 = np.argmax(tahmin2)
    en_buyuk_indeks3 = np.argmax(tahmin3)
    en_buyuk_indeks4 = np.argmax(tahmin4)

    
    en_buyuk_tahmin1 = tahmin1[0, en_buyuk_indeks1]
    en_buyuk_tahmin2 = tahmin2[0, en_buyuk_indeks2]
    en_buyuk_tahmin3 = tahmin3[0, en_buyuk_indeks3]
    en_buyuk_tahmin4 = tahmin4[0, en_buyuk_indeks4]

    
    en_buyuk_tahmin = max(en_buyuk_tahmin1, en_buyuk_tahmin2, en_buyuk_tahmin3, en_buyuk_tahmin4)
    en_buyuk_indeks = [en_buyuk_indeks1, en_buyuk_indeks2, en_buyuk_indeks3, en_buyuk_indeks4][
        [en_buyuk_tahmin1, en_buyuk_tahmin2, en_buyuk_tahmin3, en_buyuk_tahmin4].index(en_buyuk_tahmin)]

    # tahmin değeri 0.4 üstündeyse veriyi  ekle
    if en_buyuk_tahmin > 0.4:
        dokuman = {
            "Ad": veri["Ad"],
            "Soyad": veri["Soyad"],
            "TC": veri["TC"],
            "Telefon": veri["Telefon"],
            "EnBuyukIhtimal": float(en_buyuk_tahmin),
            "EnBuyukSonucIndex": int(en_buyuk_indeks)
        }

        # Veriyi sonuc koleksiyonuna ekle
        sonuc_koleksiyonu.insert_one(dokuman)
        print(f"{veri['TC']} TC numaralı veri 'sonuclar2' koleksiyonuna başarıyla eklendi.")
    else:
        print(f"{veri['TC']} TC numaralı veri eklenemedi, çünkü en büyük tahmin değeri 0.4'ten küçük.")


client.close()
