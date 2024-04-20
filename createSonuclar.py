from pymongo import MongoClient

# MongoDB bağlantısı
client = MongoClient("mongodb://localhost:27017/")
db = client["DenemeDB"]

# 'sonuclar2' koleksiyonunu oluştur
db.create_collection("sonuclar", validator={
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["Ad", "Soyad", "TC", "Telefon", "EnBuyukIhtimal", "EnBuyukSonucIndex"],
        "properties": {
            "Ad": {"bsonType": "string"},
            "Soyad": {"bsonType": "string"},
            "TC": {"bsonType": "string"},
            "Telefon": {"bsonType": "string"},
            "EnBuyukIhtimal": {"bsonType": "double"},
            "EnBuyukSonucIndex": {"bsonType": "int"}
        }
    }
})

# MongoDB bağlantısını kapat
client.close()
