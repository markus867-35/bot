import asyncio
import json
import os
import logging
from playwright.async_api import async_playwright
from telegram import Bot

# Konfigurasi
TOKEN = '7846319907:AAGVXkwvn0f4tm8bJaHNsAAlz19qEM-T8Hg'
CHAT_ID = '-1004458222776'
HISTORY_FILE = 'history.json'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DAFTAR_PASARAN = [
    {"nama": "TURKI", "url": "https://naiktoto.com/market-result/698/TURKI"},
    {"nama": "CAMBODIA", "url": "https://naiktoto.com/market-result/1166/CAMBODIA"},
    {"nama": "MAROKO", "url": "https://naiktoto.com/market-result/762/MAROKO"},
    {"nama": "TASMANIA_06", "url": "https://naiktoto.com/market-result/766/TASMANIA_06"},      
    {"nama": "CHICAGO_NIGHT", "url": "https://naiktoto.com/market-result/764/CHICAGO_NIGHT"},      
    {"nama": "TASMANIA_10", "url": "https://naiktoto.com/market-result/767/TASMANIA_10"},      
    {"nama": "FUJIAN_12", "url": "https://naiktoto.com/market-result/770/FUJIAN_12"},      
    {"nama": "TASMANIA_13", "url": "https://naiktoto.com/market-result/768/TASMANIA_13"},
    {"nama": "LIBANON", "url": "https://naiktoto.com/market-result/774/LIBANON"},
    {"nama": "FUJIAN_15", "url": "https://naiktoto.com/market-result/771/FUJIAN_15"},
    {"nama": "TASMANIA_16", "url": "https://naiktoto.com/market-result/769/TASMANIA_16"},
    {"nama": "SINGAPORE", "url": "https://naiktoto.com/market-result/775/SINGAPORE"},
    {"nama": "KAMBOJA", "url": "https://naiktoto.com/market-result/773/KAMBOJA"},
    {"nama": "CHICAGO_DAY", "url": "https://naiktoto.com/market-result/760/CHICAGO_DAY"},
    {"nama": "YORDANIA4D", "url": "https://naiktoto.com/market-result/763/YORDANIA4D"},
    {"nama": "FUJIAN_20", "url": "https://naiktoto.com/market-result/772/FUJIAN_20"},
    {"nama": "FUJIAN_23", "url": "https://naiktoto.com/market-result/761/FUJIAN_23"},
    {"nama": "TOTOMACAU4D_24", "url": "https://naiktoto.com/market-result/1175/TOTOMACAU4D_24"},
    {"nama": "TENNESSE_MID", "url": "https://naiktoto.com/market-result/1149/TENNESSE_MID"},
    {"nama": "KENTUCKY_MID", "url": "https://naiktoto.com/market-result/1150/KENTUCKY_MID"},
    {"nama": "FLORIDA_MID", "url": "https://naiktoto.com/market-result/1151/FLORIDA_MID"},
    {"nama": "ILLINOIS_MID", "url": "https://naiktoto.com/market-result/1152/ILLINOIS_MID"},
    {"nama": "NEWYORK_MID", "url": "https://naiktoto.com/market-result/1153/NEWYORK_MID"},
    {"nama": "CAROLINA_DAY", "url": "https://naiktoto.com/market-result/1154/CAROLINA_DAY"},
    {"nama": "OREGON_03", "url": "https://naiktoto.com/market-result/1155/OREGON_03"},
    {"nama": "OREGON_06", "url": "https://naiktoto.com/market-result/1156/OREGON_06"},
    {"nama": "TENNESSE_EVE", "url": "https://naiktoto.com/market-result/1157/TENNESSE_EVE"},
    {"nama": "OHIO_EVE", "url": "https://naiktoto.com/market-result/1158/OHIO_EVE"},
    {"nama": "OREGON_09", "url": "https://naiktoto.com/market-result/1161/OREGON_09"},
    {"nama": "ILLINOIS_EVE", "url": "https://naiktoto.com/market-result/1162/ILLINOIS_EVE"},
    {"nama": "NEWYORK_EVE", "url": "https://naiktoto.com/market-result/1163/NEWYORK_EVE"},
    {"nama": "KENTUCKY_EVE", "url": "https://naiktoto.com/market-result/1164/KENTUCKY_EVE"},
    {"nama": "CAROLINA_EVE", "url": "https://naiktoto.com/market-result/1165/CAROLINA_EVE"},
    {"nama": "OREGON_12", "url": "https://naiktoto.com/market-result/1168/OREGON_12"},
    {"nama": "BULLSEYE", "url": "https://naiktoto.com/market-result/1167/BULLSEYE"},
    {"nama": "TOTOMACAU4D_13", "url": "https://naiktoto.com/market-result/1180/TOTOMACAU4D_13"},
    {"nama": "SYDNEY_POOLS", "url": "https://naiktoto.com/market-result/1146/SYDNEY_POOLS"},
    {"nama": "SYDNEY_LOTTO", "url": "https://naiktoto.com/market-result/1147/SYDNEY_LOTTO"},
    {"nama": "CHINA", "url": "https://naiktoto.com/market-result/1169/CHINA"},
    {"nama": "TOTOMACAU4D_16", "url": "https://naiktoto.com/market-result/1179/TOTOMACAU4D_16"},
    {"nama": "JEPANG", "url": "https://naiktoto.com/market-result/1170/JEPANG"},
    {"nama": "TOTOMACAU4D_19", "url": "https://naiktoto.com/market-result/1178/TOTOMACAU4D_19"},
    {"nama": "PCSO", "url": "https://naiktoto.com/market-result/1171/PCSO"},
    {"nama": "TAIWAN", "url": "https://naiktoto.com/market-result/1172/TAIWAN"},
    {"nama": "TENNESSE_MOR", "url": "https://naiktoto.com/market-result/1173/TENNESSE_MOR"},
    {"nama": "TOTOMACAU4D_22", "url": "https://naiktoto.com/market-result/1177/TOTOMACAU4D_22"},
    {"nama": "HONGKONG_POOLS", "url": "https://naiktoto.com/market-result/1145/HONGKONG_POOLS"},
    {"nama": "TOTOMACAU4D_23", "url": "https://naiktoto.com/market-result/1176/TOTOMACAU4D_23"},
    {"nama": "HONGKONG_LOTTO", "url": "https://naiktoto.com/market-result/1144/HONGKONG_LOTTO"},
    {"nama": "OHIO_MID", "url": "https://naiktoto.com/market-result/1148/OHIO_MID"},
    {"nama": "JAKARTA", "url": "https://naiktoto.com/market-result/1174/JAKARTA"},
]

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

async def main():
    bot = Bot(token=TOKEN)
    history = load_history()
    
    is_initial_load = len(history) == 0
    if is_initial_load:
        logging.info("📌 File history kosong. Bot akan melakukan sinkronisasi awal (menghindari spam ke Telegram)...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        logging.info("🚀 Bot Pemantau Result Naiktoto Aktif!")
        
        while True:
            for pasaran in DAFTAR_PASARAN:
                logging.info(f"🔍 Mengecek: {pasaran['nama']}...")
                try:
                    await page.goto(pasaran['url'], timeout=60000, wait_until="networkidle")
                    
                    try:
                        await page.wait_for_selector('table tbody tr', timeout=10000)
                    except:
                        pass 
                    
                    data = await page.evaluate('''() => {
                        const rows = document.querySelectorAll('table tbody tr');
                        for (let row of rows) {
                            const cols = row.querySelectorAll('td');
                            if (cols && cols.length >= 3) {
                                const periode = cols[0].innerText.trim();
                                const tanggal = cols[1].innerText.trim();
                                const angka = cols[2].innerText.trim();
                                
                                if (angka && angka !== '-' && tanggal && tanggal !== '-') {
                                    return {
                                         periode: periode,
                                         tanggal: tanggal,
                                         angka: angka
                                    };
                                }
                            }
                        }
                        return null;
                    }''')
                    
                    print(f"DEBUG [{pasaran['nama']}] -> {data}")
                    
                    if not data: 
                        continue
                    
                    key = f"{pasaran['nama']}_{data['periode']}_{data['tanggal']}_{data['angka']}"
                    
                    if key not in history:
                        pasaran_sudah_ada = any(k.startswith(pasaran['nama'] + "_") for k in history.keys())
                        
                        if not pasaran_sudah_ada and len(history) < len(DAFTAR_PASARAN) * 2: 
                            history[key] = True
                            save_history(history)
                            logging.info(f"📥 Disimpan ke history (Inisialisasi {pasaran['nama']}): Periode {data['periode']}")
                        else:
                            # Memisahkan tanggal dan jam
                            parts = data['tanggal'].split(' ')
                            tgl_saja = parts[0] if len(parts) > 0 else data['tanggal']
                            jam_saja = parts[1] if len(parts) > 1 else ''

                            logging.info(f"🔥 Hasil Baru Ditemukan: {pasaran['nama']} - Periode {data['periode']} - {data['angka']}")
                            
                            # Teks judul yang ingin ditengah
                            judul_atas = "🎯 RESULT NAIKTOTO"
                            
                            # Menghitung spasi kiri agar pas di tengah lebar 30 karakter
                            pad_kiri = max(0, (30 - len(judul_atas)) // 2)
                            judul_centered = " " * pad_kiri + judul_atas

                            message = (
                                f"<pre>{judul_centered}\n"
                                f"------------------------------\n"
                                f"📉 Pasaran : {pasaran['nama']}\n"
                                f"📌 Periode : {data['periode']}\n"
                                f"📅 Tanggal : {tgl_saja}\n"
                                f"⏰ Jam     : {jam_saja}\n"
                                f"🏆 Prize 1 : {data['angka']}\n"
                                f"🔥 Selamat kepada pemenang!\n"
                                f"           NAIKTOTO\n"
                                f"------------------------------</pre>"
                            )
                            await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='HTML')
                            history[key] = True
                            save_history(history)
                        
                except Exception as e:
                    logging.error(f"❌ Gagal ambil {pasaran['nama']}: {str(e)[:50]}...")
                
                await asyncio.sleep(1)
            
            logging.info("⏳ Selesai satu siklus, memuat ulang pengecekan...")
            await asyncio.sleep(10)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot dihentikan oleh user.")