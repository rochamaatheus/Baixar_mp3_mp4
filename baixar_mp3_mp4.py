import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp
import os
import threading

ffmpeg_path = os.path.join(os.path.dirname(__file__), 'bin', 'ffmpeg.exe')

def download_videos(file_path, progress, status_label):
    ydl_video_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'videos/%(title)s.%(ext)s',
        'retries': 3,
        'fragment_retries': 5,
        'ffmpeg_location': ffmpeg_path,
        'progress_hooks': [lambda d: update_progress(d, progress, status_label)],
    }
    
    ydl_audio_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audios/%(title)s.%(ext)s',
        'retries': 3,
        'fragment_retries': 5,
        'ffmpeg_location': ffmpeg_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [lambda d: update_progress(d, progress, status_label)],
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

    messagebox.showinfo("Sucesso", "Downloads concluídos!")
    progress.pack_forget()
    status_label.pack_forget()

def update_progress(d, progress, status_label):
    if d['status'] == 'downloading':
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes', 0)
        if total > 0:
            percent = downloaded / total * 100
            progress['value'] = percent
            status_label.config(text=f"{percent:.2f}% Baixado")
        root.update_idletasks()
    elif d['status'] == 'finished':
        progress['value'] = 100
        status_label.config(text="Download Concluído")

def select_file():
    file_path = filedialog.askopenfilename(
        title="Selecione o arquivo de links",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )
    if file_path:
        try:
            progress.pack(pady=10)
            status_label.pack()
            progress['value'] = 0
            status_label.config(text="Iniciando download...")
            root.update_idletasks()
            
            download_thread = threading.Thread(target=download_videos, args=(file_path, progress, status_label))
            download_thread.start()
            
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

progress = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')

status_label = tk.Label(root, text="Aguardando...")

root.mainloop()
