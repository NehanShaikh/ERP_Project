const express = require("express");
const router = express.Router();
const { exec } = require("child_process");
const db = require("../db");

const multer = require("multer");
const path = require("path");

const storage = multer.diskStorage({
  destination: "uploads/",
  filename: (req, file, cb) => {
    const ext = path.extname(file.originalname); // get .jpg/.pdf
    cb(null, Date.now() + ext);
  }
});

const upload = multer({ storage: storage });

router.post("/upload", upload.single("file"), (req, res) => {
  const filePath = req.file.path;
  const supplier = req.body.supplier;

  exec(`python ../python_ocr/ocr_engine.py ${filePath}`, (err, stdout) => {
    if (err) {
      console.error(err);
      return res.status(500).send("Error processing OCR");
    }

    const data = JSON.parse(stdout);

    const query = `
      INSERT INTO invoices 
      (supplier_name, product_name, quantity, price, gst, total)
      VALUES (?, ?, ?, ?, ?, ?)
    `;

    db.query(query, [
      supplier,
      data.product_name,
      data.quantity,
      data.price,
      data.gst,
      data.total
    ], (err) => {
      if (err) return res.status(500).send(err);

      res.json({
        message: "Invoice processed successfully",
        data: data
      });
    });
  });
});

module.exports = router;
