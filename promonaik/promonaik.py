import os
from telegram.ext import ApplicationBuilder
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.request import HTTPXRequest  # <-- Diperbaiki (huruf e-nya pas)

# Inisialisasi request dengan timeout yang lebih panjang untuk mencegah ConnectTimeout
request = HTTPXRequest(connect_timeout=30.0, read_timeout=30.0)

TOKEN = '8861673032:AAE6S0HdJF9y8avDfMgpSAbn_2vj71yPczo'
CHAT_ID = '-1004458222776'
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

    teks = '''👋 SELAMAT DATANG DI NAIKTOTO OFFICIAL 👋

🎁 BONUS NEW MEMBER 20%
🎁 BONUS SLOT NEW MEMBER 100%
🎁 BONUS HARIAN 5%
🎁 BONUS DOWNLOAD APLIKASI
🎁 BONUS ROLLINGAN SlOT 3%
🎁 BONUS REFFERAL ALL GAMES 10%
🎁 BONUS CASHBACK SLOT 10%
🎁 BONUS CASHBACK ALLSPORT GAME 10%
🎁 BONUS CASHBACK LIVEGAMES 10%
🎁 BONUS FREESPIN 25% & BUYSPIN 15%
🎁 EVENT SLOT SPECIAL MAHJONG WAYS
🎁 EVENT JOKER'S JEWELS
🎁 EVENT SCATTER PRAGMATIC PLAY
🎁 EVENT SCATTER HITAM MAHJONG WIN'S 3

Main sekarang dan raih jackpotmu 🚀🚀'''

    keyboard = [
        [InlineKeyboardButton("📝 DAFTAR", url="https://link.naiktoto.net/register"), InlineKeyboardButton("🌐 LINK ALTERNATIF", url="https://ok1.naiktoto-nih.com")],
        [InlineKeyboardButton("📱 APK", url="https://takenlink.eu/NaikTOTO-APK"), InlineKeyboardButton("📊 RTP", url="https://mobile.ofclrtpnaik.com/")],
        [InlineKeyboardButton("🎁 PROMOSI", url="https://link.naiktoto.net/promosi"), InlineKeyboardButton("🚀 PREDIKSI", url="https://angkanaikterus.com/")],
        [InlineKeyboardButton("🎧 CS TELE", url="https://telegram.me/Naiktoto11")]
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
    # Masukkan custom request object ke dalam ApplicationBuilder agar timeout teratasi
    application = ApplicationBuilder().token(TOKEN).request(request).build()
    job_queue = application.job_queue

    job_queue.run_repeating(kirim_pesan, interval=7200, first=5)

    print("Bot berhasil dijalankan. Sedang menunggu pengiriman pesan...")
    application.run_polling()

if __name__ == '__main__':
    main()