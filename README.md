# 🎵 PELI APP - Discord Music Bot

Bot Discord modular berbasis Python yang dirancang untuk memutar musik dengan lancar menggunakan `yt_dlp` dan pendekatan pemrograman asinkron (`asyncio`).

## 🚀 Fitur Utama
* **Slash Commands (`app_commands`)**: Navigasi perintah bot yang modern dan intuitif langsung di Discord.
* **Asynchronous Processing (`asyncio.to_thread`)**: Memproses pencarian dan pengunduhan lagu di *background thread* tanpa membuat server bot *lag* atau *freeze*.
* **Music Streaming**: Mendukung pemutaran musik berkualitas tinggi menggunakan integrasi `yt_dlp` dan `FFmpeg`.

## 🛠️ Teknologi & Library yang Digunakan
* **Python** (Bahasa Pemrograman Utama)
* **discord.py** (API Wrapper untuk Discord)
* **yt_dlp** (Pengekstrak media/audio)
* **python-dotenv** (Manajemen variabel lingkungan yang aman)
