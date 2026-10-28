import asyncio
import discord
from discord import app_commands
import yt_dlp
import os
from dotenv import load_dotenv

load_dotenv()
Token = os.getenv("Discord_Token")

intents =  discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

YDL_OPTS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "default_search": "ytsearch",
}
FFMPEG_OPTS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}

def cari_lagu(Judul_lagu):
    with yt_dlp.YoutubeDL(YDL_OPTS) as ydl :
        info = ydl.extract_info(Judul_lagu, download=False)
        if "entries" in info :
            info = info["entries"][0]
        return info["title"], info["url"]

@tree.command(name="halo", description="Menyapa Anda")
async def halo(interaction: discord.Interaction):
    await interaction.response.send_message(f"Halo, {interaction.user.name}!")

@tree.command(name="author", description="Menanyakan Siapa Pembuat")
async def author(interaction: discord.Interaction):
    await interaction.response.send_message("Pembuat Saya Bernama Zenles")

@tree.command(name="join", description="Bot masuk ke voice channel Anda")
async def join(interaction: discord.Interaction):
    if interaction.user.voice is None:
        await interaction.response.send_message("Masuk dulu ke voice channel ya!")
        return
    await interaction.user.voice.channel.connect()
    await interaction.response.send_message("Sudah masuk! 🎧")

@tree.command(name="leave", description="Bot keluar dari voice channel")
async def leave(interaction: discord.Interaction):
    if interaction.guild.voice_client is None:
        await interaction.response.send_message("Saya tidak sedang di voice channel.")
        return
    await interaction.guild.voice_client.disconnect()
    await interaction.response.send_message("Sampai jumpa! 👋")

@tree.command(name="play", description="Putar lagu (judul atau link)")
async def play(interaction: discord.Interaction, song: str):
    if interaction.user.voice is None:
        await interaction.response.send_message("Masuk dulu ke voice channel ya!")
        return

    await interaction.response.defer()

    vc = interaction.guild.voice_client
    if vc is None:
        vc = await interaction.user.voice.channel.connect()

    judul, url = await asyncio.to_thread(cari_lagu, song)
    vc.play(discord.FFmpegPCMAudio(url, **FFMPEG_OPTS))
    await interaction.followup.send(f"🎶 Memutar: **{judul}**")

@tree.command(name="pause", description="Jeda lagu")
async def pause(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc is not None and vc.is_playing():
        vc.pause()
        await interaction.response.send_message("⏸️ Lagu dijeda")
    else:
        await interaction.response.send_message("Tidak ada lagu yang sedang diputar.")

@tree.command(name="resume", description="Lanjutkan lagu")
async def resume(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc is not None and vc.is_paused():
        vc.resume()
        await interaction.response.send_message("▶️ Lagu dilanjutkan")
    else:
        await interaction.response.send_message("Tidak ada lagu yang dijeda.")

@tree.command(name="stop", description="Hentikan lagu")
async def stop(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc is not None and (vc.is_playing() or vc.is_paused()):
        vc.stop()
        await interaction.response.send_message("⏹️ Lagu dihentikan")
    else:
        await interaction.response.send_message("Tidak ada lagu yang sedang diputar.")

@client.event
async def on_ready():
    hasil = await tree.sync()
    print(f"Terkirim {len(hasil)} perintah: {[c.name for c in hasil]}")
    print(f"Bot Aktivited Sebagai {client.user}")

client.run(Token)