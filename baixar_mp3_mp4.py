import tkinter as tk
from tkinter import filedialog, messagebox
import yt_dlp
import os

# Configurar o caminho para o ffmpeg local
ffmpeg_path = os.path.join(os.path.dirname(__file__), 'bin', 'ffmpeg.exe')

def download_videos(file_path):
    ydl_video_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'videos/%(title)s.%(ext)s',
        'retries': 3,
        'fragment_retries': 5,
        'ffmpeg_location': ffmpeg_path,  # Usando o ffmpeg local
    }
    
    ydl_audio_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audios/%(title)s.%(ext)s',
        'retries': 3,
        'fragment_retries': 5,
        'ffmpeg_location': ffmpeg_path,  # Usando o ffmpeg local
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    os.makedirs('videos', exist_ok=True)
    os.makedirs('audios', exist_ok=True)

    with open(file_path, 'r') as file:
        video_urls = file.readlines()

    video_urls = [url.strip() for url in video_urls if url.strip()]

    for url in video_urls:
        if url.endswith('-mp3'):
            url = url.replace('-mp3', '').strip()
            with yt_dlp.YoutubeDL(ydl_audio_opts) as ydl:
                ydl.download([url])
        else:
            with yt_dlp.YoutubeDL(ydl_video_opts) as ydl:
                ydl.download([url])

def select_file():
    file_path = filedialog.askopenfilename(
        title="Selecione o arquivo de links",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )
    if file_path:
        try:
            download_videos(file_path)
            messagebox.showinfo("Sucesso", "Downloads concluídos!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

root = tk.Tk()
root.title("Downloader de Vídeos e Áudios")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

label = tk.Label(frame, text="Selecione o arquivo de links (.txt):")
label.pack(side=tk.LEFT)

button = tk.Button(frame, text="Selecionar arquivo", command=select_file)
button.pack(side=tk.LEFT, padx=10)

root.mainloop()
