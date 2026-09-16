import os
import json
import asyncio
import logging
from datetime import datetime
from playwright.async_api import async_playwright
from telegram import Bot


# Konfigurasi
TOKEN = '8616632525:AAH595OilsnQ6HBbenmte9ogJdjp4x35KiY'
CHAT_ID = '-1003827054184'
TARGET_URL = 'https://ai.tahunhoki.biz/wap'
SENT_FILE = 'sent_results.json'
INTERVAL = 30 # Detik

# Setup Logging
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)

# Load data hasil yang sudah pernah dikirim
if os.path.exists(SENT_FILE):
    with open(SENT_FILE, 'r') as f:
        sent_results = json.load(f)
else:
    sent_results = {}

async def fetch_pasaran():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(TARGET_URL, timeout=60000)
            await page.wait_for_selector('.lottery-list', timeout=30000)
            
            data = await page.evaluate('''() => {
                const results = [];
                document.querySelectorAll('.lottery-list').forEach(div => {
                    const name = div.querySelector('div[style*="font-size: 18px"]')?.innerText.trim();
                    const angka = div.querySelector('div[style*="color: #FFD700"]')?.innerText.trim();
                    if (name && angka) results.push({ name, angka });
                });
                return results;
            }''')
            return data
        except Exception as e:
            logging.error(f"Error scraping: {e}")
            return []
        finally:
            await browser.close()

async def send_new_results():
    global sent_results
    
    pasarans = await fetch_pasaran()
    new_data_found = False
    
    for p in pasarans:
        key = f"{p['name']}_{p['angka']}"
        
        if key in sent_results:
            continue
            
        message = (
            f"<pre>🎯 HASIL RESULT TAHUNHOKI\n"
            f"------------------------------\n"
            f"📅 Tanggal    : {datetime.now().strftime('%d/%m/%Y')}\n"
            f"🏁 Pasaran    : {p['name'].upper()}\n"
            f"🏆 Nomor      : {p['angka']}\n\n"
            f"🔥 Selamat kepada pemenang!\n"
            f"            TAHUNHOKI\n"
            f"------------------------------</pre>"
        )
        
        try:
            await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='HTML')
            logging.info(f"✅ Dikirim: {p['name']} -> {p['angka']}")
            await asyncio.sleep(1) # Delay antar pesan
        except Exception as e:
            logging.error(f"Gagal kirim: {e}")
        
        sent_results[key] = True
        new_data_found = True

    if new_data_found:
        with open(SENT_FILE, 'w') as f:
            json.dump(sent_results, f)

async def main():
    logging.info("🚀 AutoResult TahunHoki Python Mode Aktif...")
    while True:
        await send_new_results()
        await asyncio.sleep(INTERVAL)

if __name__ == '__main__':
    asyncio.run(main())