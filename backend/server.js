const express = require("express");
const mysql = require("mysql");
const cors = require("cors");

const app = express();
app.use(cors());

const db = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "your_password",
    database: "erp_ai"
});

db.connect(err => {
    if (err) throw err;
    console.log("MySQL Connected");
});

app.get("/products", (req, res) => {
    db.query("SELECT * FROM inventory", (err, result) => {
        if (err) throw err;
        res.json(result);
    });
});

// API to get alerts
app.get("/alerts", (req, res) => {
    db.query(`
        SELECT a.*, i.product_name
        FROM alerts a
        JOIN inventory i ON a.product_id = i.product_id
        ORDER BY a.created_at DESC
    `, (err, result) => {
        if (err) {
            console.error(err);
            return res.status(500).json({ error: "Database error" });
        }
        res.json(result);
    });
});

app.listen(5000, () => {
    console.log("Server running on port 5000");
});
