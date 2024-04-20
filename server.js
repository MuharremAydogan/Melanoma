

const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const Veri = require('./db');

const app = express();
const port = 3000;

app.use(cors());
app.use(bodyParser.json({ limit: '10mb' }));

app.post('/veriEkle', async (req, res) => {
  try {
    const yeniVeri = new Veri(req.body);
    await yeniVeri.save();
    res.json({ success: true, message: 'Veri başarıyla eklendi.' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ success: false, message: 'Veri eklenirken bir hata oluştu.' });
  }
});

app.listen(port, () => {
  console.log(`Server ${port} portunda çalışıyor...`);
});
