@echo off
:: Beri jeda 20 detik jika diperlukan saat komputer baru menyala
timeout /t 5 /nobreak

echo 🚀 Menjalankan semua bot...

:: 1. Menjalankan bot.js (Node.js di dalam subfolder botchaport)
start cmd /k "cd /d C:\Users\marku\Downloads\Markus-Pc\robot\botchaport && node bot.js"

:: 2. Menjalankan promojala.py (Python)
start cmd /k "cd /d C:\Users\marku\Downloads\Markus-Pc\robot\promojala && python promojala.py"

:: 3. Menjalankan promonaik.py (Python)
start cmd /k "cd /d C:\Users\marku\Downloads\Markus-Pc\robot\promonaik && python promonaik.py"

:: 4. Menjalankan promotahun.py (Python)
start cmd /k "cd /d C:\Users\marku\Downloads\Markus-Pc\robot\promotahun && python promotahun.py"

:: 5. Menjalankan resultnaik.py (Python)
start cmd /k "cd /d C:\Users\marku\Downloads\Markus-Pc\robot\resultnaik && python resultnaik.py"

:: 6. Menjalankan tahunresult.py (Python)
start cmd /k "cd /d C:\Users\marku\Downloads\Markus-Pc\robot\tahunresult && python tahunresult.py"

:: 7. Menjalankan bot.js (Node.js di dalam subfolder togelbot)
start cmd /k "cd /d C:\Users\marku\Downloads\Markus-Pc\robot\togelbot && node bot.js"

:: 8. Menjalankan tombolresult.py (Python)
start cmd /k "cd /d C:\Users\marku\Downloads\Markus-Pc\robot\tombolresult && python tombolresult.py"

exit