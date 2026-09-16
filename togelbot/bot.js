require('dotenv').config();
const { chromium } = require('playwright');
const { createClient } = require('@supabase/supabase-js');

// Konfigurasi Supabase
const SUPABASE_URL = 'https://hdmropvysyextiirgafz.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhkbXJvcHZ5c3lleHRpaXJnYWZ6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODQzMzcxMzMsImV4cCI6MjA5OTkxMzEzM30.PrVI5s6CuGsCqy_xQESD3VpKYCPIkgqYNkI1aOBdmtQ';
const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

async function scrapeAndSaveTogel() {
  console.log('🤖 Memulai bot pengambilan result...');

  // Jalankan browser menggunakan Playwright (menggantikan Puppeteer agar tidak error di Windows)
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    // Buka website target
    await page.goto('https://on.kamuskeluaran.live/', {
      waitUntil: 'networkidle',
      timeout: 60000,
    });

    console.log('🌐 Berhasil membuka situs, sedang mengambil data...');

    // Scraping data dari halaman sesuai struktur HTML target (Logika tetap sama persis)
    const resultsData = await page.evaluate(() => {
      const items = [];
      const cards = document.querySelectorAll('.card'); 

      cards.forEach((card) => {
        const pasaran = card.querySelector('.card-title')?.innerText?.trim() || '';
        const cardTextElem = card.querySelector('.card-text');
        
        if (pasaran && cardTextElem) {
          const lines = cardTextElem.innerText.split('\n').map(l => l.trim()).filter(Boolean);
          const tanggal = lines[0] || null; 
          let rawResult = lines[1] || '';   

          if (pasaran && rawResult) {
            let finalResult = rawResult;
            if (rawResult.length > 4) {
              finalResult = rawResult.slice(-4);
            }

            items.push({
              pasaran: pasaran.toUpperCase(),
              tanggal: tanggal,
              result: finalResult, 
              status: 'SUDAH DCAIRKAN',
              waktu_dibuat: new Date().toLocaleString('id-ID', { timeZone: 'Asia/Jakarta' })
            });
          }
        }
      });

      return items;
    });

    console.log(`📊 Ditemukan ${resultsData.length} data result.`);

    if (resultsData.length === 0) {
      console.log('⚠️ Tidak ada data yang berhasil di-scrape. Periksa kembali selector CSS elemen HTML web.');
      await browser.close();
      return;
    }

    // Proses penyimpanan ke Supabase dengan penomoran periode otomatis & cek duplikat (Logika tetap sama persis)
    for (const data of resultsData) {
      // 1. Cek apakah data dengan pasaran dan tanggal yang sama sudah ada
      const { data: existingData, error: checkError } = await supabase
        .from('togel_results')
        .select('id')
        .eq('pasaran', data.pasaran)
        .eq('tanggal', data.tanggal)
        .maybeSingle();

      if (checkError) {
        console.error(`❌ Gagal mengecek data ${data.pasaran}:`, checkError.message);
        continue;
      }

      // Jika data belum ada, kita hitung periode ke berapa berdasarkan jumlah data pasaran tersebut sebelumnya
      if (!existingData) {
        // Hitung berapa banyak data yang sudah tersimpan untuk pasaran ini di database
        const { count, error: countError } = await supabase
          .from('togel_results')
          .select('*', { count: 'exact', head: true })
          .eq('pasaran', data.pasaran);

        if (countError) {
          console.error(`❌ Gagal menghitung periode ${data.pasaran}:`, countError.message);
          continue;
        }

        // Tentukan nomor periode (jumlah data sebelumnya + 1)
        const nextPeriodeNumber = (count || 0) + 1;
        data.periode = `Periode ${nextPeriodeNumber}`; // Hasil: "Periode 1", "Periode 2", dst.

        // Lakukan Insert ke database
        const { error: insertError } = await supabase
          .from('togel_results')
          .insert([data]);

        if (insertError) {
          console.error(`❌ Gagal menyimpan pasaran ${data.pasaran}:`, insertError.message);
        } else {
          console.log(`✅ Berhasil menyimpan ${data.pasaran} - ${data.periode} (${data.tanggal}) - Result: ${data.result}`);
        }
      } else {
        console.log(`⏭️ Lewati: ${data.pasaran} (${data.tanggal}) sudah ada di database.`);
      }
    }

    console.log('✨ Proses scraping dan sinkronisasi ke Supabase selesai!');

  } catch (err) {
    console.error('❌ Terjadi kesalahan pada bot:', err);
  } finally {
    await browser.close();
  }
}

// --- Pengaturan Waktu Otomatis (Setiap 2 Menit sesuai script awal Anda) ---
const INTERVAL_WAKTU = 2 * 60 * 1000;

console.log('🚀 Bot otomatis diaktifkan! Akan mengecek pembaruan setiap 2 menit.');

// Jalankan pertama kali saat script dinyalakan
scrapeAndSaveTogel();

// Jalankan secara berulang setiap 2 menit
setInterval(() => {
  console.log('\n----------------------------------------');
  console.log('⏰ Waktunya bot mengecek pembaruan data...');
  scrapeAndSaveTogel();
}, INTERVAL_WAKTU);