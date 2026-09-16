const http = require('http');
const { exec } = require('child_process');
const path = require('path');

const PORT = 3333;

const server = http.createServer((req, res) => {
    if (req.url === '/jalankan') {
        const batchPath = path.join(__dirname, 'bot.bat');
        exec(`start "" "${batchPath}"`);
        
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end('<h3>🚀 Bot berhasil dijalankan dari jarak jauh!</h3>');
    } else {
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end('<h3>Akses URL: <a href="/jalankan">Klik di sini untuk jalankan bot</a></h3>');
    }
});

server.listen(PORT, () => {
    console.log(`Server lokal aktif di port ${PORT}`);
});