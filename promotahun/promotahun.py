import os
from telegram.ext import ApplicationBuilder
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


TOKEN = '8881044317:AAEVRTsK59pd5jCMj4IKm6TN0uF0muUpCIw'
CHAT_ID = '-1003827054184'
FOLDER_GAMBAR = 'gambar_promosi'


indeks_gambar = 0

async def kirim_pesan(context):
    global indeks_gambar 
    
    try:
        files = sorted([f for f in os.listdir(FOLDER_GAMBAR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
        
        if not files:
            print(f"Error: Tidak ada gambar di folder {FOLDER_GAMBAR}")
            return
        
        
        if indeks_gambar >= len(files):
            indeks_gambar = 0
            
        file_terpilih = files[indeks_gambar]
        path_gambar = os.path.join(FOLDER_GAMBAR, file_terpilih)
        
        # Majukan indeks
        indeks_gambar = (indeks_gambar + 1) % len(files)
        
    except FileNotFoundError:
        print(f"Error: Folder '{FOLDER_GAMBAR}' tidak ditemukan.")
        return

    
    teks = '''👋 SELAMAT DATANG DI TAHUNHOKI OFFICIAL 👋

🎁 INFO PROMO TAHUNHOKI
🎁 BONUS HARIAN SLOT 5%
🎁 BONUS DOWNLOAD APLIKASI 20 RIBU
🎁 BONUS HARIAN TOGEL 5%
🎁 BONUS NEW MEMBER 20%
🎁 BONUS HARIAN ALL GAME 5%
🎁 CASHBACK SLOT 5%
🎁 CASHBACK LIVECASINO Up To 10%
🎁 CASHBACK ALL SPORT GAME 5%
🎁 EVENT SCATTER PRAGMATIC
🎁 EVENT BLACKSCATTER MAHJONGWINS 3
🎁 EVENT SLOT SWEET BONANZA
🎁 EVENT WIN STREAK BUYSPIN
🎁 EVENT SCATTER PRAGMATIC
🎁 ROLLINGAN HARIAN 1%
🎁 REFFERAL ALL GAME 1%
🎁 LOMBA TEBAK ANGKA
🎁 GARANSI KEKALAHAN 100%

Main sekarang dan raih jackpotmu 🚀🚀'''

    
    keyboard = [
        [InlineKeyboardButton("📝 DAFTAR", url="https://dub.sh/daftar-tahunhoki"), InlineKeyboardButton("🌐 LINK ALTERNATIF", url="https://dub.sh/login-tahunhoki")],
        [InlineKeyboardButton("📱 APK", url="https://dub.link/apkcadtahunhoki"), InlineKeyboardButton("📊 RTP", url="https://dub.link/rtptahun")],
        [InlineKeyboardButton("🎁 PROMOSI", url="https://tahunhoki.link/promo-th"), InlineKeyboardButton("🚀 PREDIKSI", url="https://dub.link/prediksitahunhk")],
        [InlineKeyboardButton("💬 LIVECHAT", url="https://dub.link/livechat-tahunhk"), InlineKeyboardButton("🎧 CS TELE", url="https://tahunhoki.link/cstele-th1")],
        [InlineKeyboardButton("🔥 BUKTI JACKPOT 🔥", url="https://dub.sh/jp500juta")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    
    with open(path_gambar, 'rb') as photo:
        await context.bot.send_photo(
            chat_id=CHAT_ID,
            photo=photo,
            caption=teks,
            reply_markup=reply_markup
        )
    print(f"Berhasil mengirim gambar acak: {file_terpilih}")

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    job_queue = application.job_queue
    
    
    job_queue.run_repeating(kirim_pesan, interval=7200, first=5)
    
    print("Bot berhasil dijalankan. Sedang menunggu pengiriman pesan setiap 1 menit...")
    application.run_polling()


if __name__ == '__main__':
    main()