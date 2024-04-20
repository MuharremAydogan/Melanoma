
const mongoose = require('mongoose');

mongoose.connect('mongodb://localhost:27017/DenemeDB', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

const veriSchema = new mongoose.Schema({
  Ad: String,
  Soyad: String,
  TC: String,
  Telefon: String,
  pixel1: [Number],
  pixel2: [Number],
  pixel3: [Number],
  pixel4: [Number],
});

const Veri = mongoose.model('Veri', veriSchema);

module.exports = Veri;
