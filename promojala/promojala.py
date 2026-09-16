import os
from telegram.ext import ApplicationBuilder
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# --- KONFIGURASI ---
TOKEN = '8849504814:AAEkfJV6d59jOVAoQ77lvnCvNqti7FDsVTg'
CHAT_ID = '-1003736157130'
FOLDER_GAMBAR = 'gambar_promosi'

# TAMBAHKAN BARIS INI DI SINI agar variabelnya terdaftar
indeks_gambar = 0

async def kirim_pesan(context):
    global indeks_gambar 
    
    try:
        files = sorted([f for f in os.listdir(FOLDER_GAMBAR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
        
        if not files:
            print(f"Error: Tidak ada gambar di folder {FOLDER_GAMBAR}")
            return
        
        # Reset jika gambar di folder berubah/dihapus
        if indeks_gambar >= len(files):
            indeks_gambar = 0
            
        file_terpilih = files[indeks_gambar]
        path_gambar = os.path.join(FOLDER_GAMBAR, file_terpilih)
        
        # Majukan indeks
        indeks_gambar = (indeks_gambar + 1) % len(files)
        
    except FileNotFoundError:
        print(f"Error: Folder '{FOLDER_GAMBAR}' tidak ditemukan.")
        return

    # 2. Teks Promosi
    teks = '''👋 SELAMAT DATANG DI JALAWIN OFFICIAL 👋

🎁 INFO PROMO JALAWIN
🎁 CASHBACK SLOT 5%
🎁 REFFERAL ALL GAME 1%
🎁 BONUS DOWNLOAD APLIKASI
🎁 FREECHIP TAK TERHINGGA
🎁 EVENT BUYSPIN & FREESPIN
🎁 EVENT WIN STREAK BUYSPIN
🎁 LOMBA TEBAK ANGKA
🎁 EVENT SCATTER MAHJONG WAYS 1 - 2
🎁 BONUS NEW MEMBER 20%
🎁 CASHBACK LIVECASINO Up To 10%
🎁 CASHBACK ALL SPORT GAME 5%
🎁 ROLLINGAN HARIAN 1%
🎁 EVENT SCATTER PRAGMATIC
🎁 EVENT BLACKSCATTER MAHJONGWINS 3
🎁 EVENT SLOT SWEET BONANZA
🎁 BONUS DEPOSIT SLOT 100%

Main sekarang dan raih jackpotmu 🚀🚀'''

    # 3. Membuat Tombol
    keyboard = [
        [InlineKeyboardButton("📝 DAFTAR", url="https://dub.link/daftarjalawin"), InlineKeyboardButton("🌐 LINK ALTERNATIF", url="https://dub.link/jala-alternatif2")],
        [InlineKeyboardButton("📱 APK", url="https://dub.link/apkcadjalawin"), InlineKeyboardButton("📊 RTP", url="https://dub.link/RTP-jalawin")],
        [InlineKeyboardButton("🎁 PROMOSI", url="https://dub.link/jalawin-promo"), InlineKeyboardButton("🚀 PREDIKSI", url="https://dub.link/prediksijalawin")],
        [InlineKeyboardButton("💬 LIVECHAT", url="https://dub.link/livechatjw"), InlineKeyboardButton("🎧 CS TELE", url="https://t.me/csjalawin1")],
        [InlineKeyboardButton("🔥 BUKTI JACKPOT 🔥", url="https://dub.link/buktijp-jlw")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # 4. Mengirim file gambar lokal
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
    
    # 60 detik = 1 menit. 
    # first=5 artinya pesan pertama akan muncul 5 detik setelah bot dijalankan.
    job_queue.run_repeating(kirim_pesan, interval=7200, first=5)
    
    print("Bot berhasil dijalankan. Sedang menunggu pengiriman pesan setiap 1 menit...")
    application.run_polling()

if __name__ == '__main__':
    main()