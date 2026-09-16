const puppeteer = require('puppeteer');

// Fungsi untuk menentukan ucapan berdasarkan jam saat ini
function getGreeting() {
  const hour = new Date().getHours();
  if (hour >= 4 && hour < 11) {
    return 'Selamat pagi boskuu. Ada yang bisa kami bantu?';
  } else if (hour >= 11 && hour < 15) {
    return 'Selamat siang boskuu. Ada yang bisa kami bantu?';
  } else if (hour >= 15 && hour < 18) {
    return 'Selamat sore boskuu. Ada yang bisa kami bantu bosku?';
  } else {
    return 'Selamat malam boskuu. Ada yang bisa kami bantu?';
  }
}

async function startChaportBot() {
  const browser = await puppeteer.launch({ 
    headless: true, // Ubah ke true jika nanti sudah lancar dan ingin dijalankan tanpa muncul jendela browser
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', // Memakai Google Chrome asli yang stabil di Windows
    defaultViewport: null,
    args: [
      '--start-maximized',
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-gpu'
    ]
  });

  const page = await browser.newPage();

  console.log('Membuka halaman login Chaport...');
  await page.goto('https://app.chaport.com/#/login', { waitUntil: 'networkidle2' });

  // Tunggu sampai input email muncul
  console.log('Menunggu form login...');
  await page.waitForSelector('input[name="email"]', { visible: true, timeout: 15000 });

  // 1. PROSES LOGIN OTOMATIS
  console.log('Mengisi data login...');
  await page.type('input[name="email"]', 'sangatsuperhoki@gmail.com', { delay: 30 });
  await page.type('input[name="password"]', '4L9GF@fq6qg45HT', { delay: 30 });
  
  // Klik tombol login
  console.log('Mengklik tombol login...');
  await page.click('input[type="submit"]');

  console.log('Menunggu dashboard chat terbuka...');
  
  // Tunggu sampai URL berubah keluar dari halaman login
  try {
    await page.waitForFunction(
      () => !window.location.href.includes('login'), 
      { timeout: 30000 }
    );
  } catch (e) {
    console.log('Gagal berpindah dari halaman login, silakan cek kredensial.');
  }

  // Tunggu elemen container chat utama (`#conversations` atau `.chat-list-content`) muncul
  try {
    await page.waitForSelector('#conversations, .chat-list-content', { visible: true, timeout: 20000 });
  } catch (e) {
    console.log('Container chat lama dimuat, tapi bot akan tetap lanjut mencoba memantau...');
  }

  console.log('Berhasil login! Bot aktif dan sedang memantau pesan masuk secara real-time...');

  let isProcessing = false;

  // 2. LOOPING PEMANTAUAN PESAN MASUK
  setInterval(async () => {
    if (isProcessing) return;

    try {
      // Periksa percakapan yang memiliki indikator unread
      const unreadChatSelector = 'div.conversation-body:has(.unread), div.chat-item:has(.unread)';
      const hasNewMessage = await page.$(unreadChatSelector);

      if (hasNewMessage) {
        isProcessing = true;
        console.log('Pesan baru belum dibaca terdeteksi!');
        
        await hasNewMessage.click();
        await new Promise(r => setTimeout(r, 600));

        // Cek dan klik tombol "Join chat" jika muncul
        const joinButtonSelector = 'button.chat-join-button';
        const joinBtn = await page.$(joinButtonSelector);
        if (joinBtn) {
          console.log('Mengklik tombol "Join chat"...');
          await joinBtn.click();
          await new Promise(r => setTimeout(r, 600));
        }

        const greetingText = getGreeting();
        const inputSelector = '#chat-input';
        
        await page.waitForSelector(inputSelector, { visible: true, timeout: 4000 });
        
        await page.type(inputSelector, greetingText, { delay: 10 });
        await new Promise(r => setTimeout(r, 300));

        const sendButtonSelector = '#chaport-send-button';
        await page.waitForSelector(sendButtonSelector, { visible: true });
        await page.click(sendButtonSelector);

        console.log(`Berhasil membalas: "${greetingText}"`);

        await new Promise(r => setTimeout(r, 2000));
        isProcessing = false;
      }
    } catch (error) {
      isProcessing = false;
    }
  }, 1000);
}

startChaportBot();