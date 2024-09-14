import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import yt_dlp
import os
import threading

ffmpeg_path = os.path.join(os.path.dirname(__file__), 'bin', 'ffmpeg.exe')
root = tk.Tk()
root.title("Downloader de Vídeos e Áudios")

# Aplicando um tema para melhorar a aparência
style = ttk.Style()
style.theme_use('clam')

def download_videos(urls, progress, status_label):
    ydl_video_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'videos/%(title)s.%(ext)s',
        'retries': 3,
        'fragment_retries': 5,
        'ffmpeg_location': ffmpeg_path,
        'progress_hooks': [lambda d: root.after(0, update_progress, d, progress, status_label)],
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
        'progress_hooks': [lambda d: root.after(0, update_progress, d, progress, status_label)],
    }

    os.makedirs('videos', exist_ok=True)
    os.makedirs('audios', exist_ok=True)

    for url in urls:
        if url.endswith('-mp3'):
            url = url.replace('-mp3', '').strip()
            with yt_dlp.YoutubeDL(ydl_audio_opts) as ydl:
                ydl.download([url])
        else:
            with yt_dlp.YoutubeDL(ydl_video_opts) as ydl:
                ydl.download([url])
    
    root.after(0, progress.pack_forget)
    root.after(0, status_label.pack_forget)
    root.after(0, lambda: messagebox.showinfo("Sucesso", "Download(s) concluído(s)!"))

def update_progress(d, progress, status_label):
    if d['status'] == 'downloading':
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
        if total > 0:
            percent = downloaded / total * 100
            progress['value'] = percent
            status_label.config(text=f"{percent:.2f}% baixados")
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
            with open(file_path, 'r') as file:
                video_urls = file.readlines()
            video_urls = [url.strip() for url in video_urls if url.strip()]
            
            progress.pack(pady=10)
            status_label.pack()
            progress['value'] = 0
            status_label.config(text="Iniciando download...")
            root.update_idletasks()
            
            download_thread = threading.Thread(target=download_videos, args=(video_urls, progress, status_label))
            download_thread.start()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

def download_url():
    url = url_entry.get().strip()
    if url:
        try:
            progress.pack(pady=10)
            status_label.pack()
            progress['value'] = 0
            status_label.config(text="Iniciando download...")
            root.update_idletasks()
            
            download_thread = threading.Thread(target=download_videos, args=([url], progress, status_label))
            download_thread.start()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")
    else:
        messagebox.showwarning("Aviso", "Por favor, insira uma URL.")

# Widgets para seleção de arquivo
file_frame = ttk.Frame(root, padding=10)
file_frame.pack(padx=10, pady=5)

file_label = ttk.Label(file_frame, text="Selecione o arquivo de links (.txt):")
file_label.pack(side=tk.LEFT)

file_button = ttk.Button(file_frame, text="Selecionar arquivo", command=select_file)
file_button.pack(side=tk.LEFT, padx=10)

# Widgets para entrada de URL
url_frame = ttk.Frame(root, padding=10)
url_frame.pack(padx=10, pady=5)

url_label = ttk.Label(url_frame, text="Ou insira uma URL:")
url_label.pack(side=tk.LEFT)

url_entry = ttk.Entry(url_frame, width=50)
url_entry.pack(side=tk.LEFT, padx=5)

url_button = ttk.Button(url_frame, text="Baixar URL", command=download_url)
url_button.pack(side=tk.LEFT, padx=10)

progress = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')

status_label = ttk.Label(root, text="Aguardando...")

github_label = tk.Label(root, text="GitHub: rochamaatheus (https://github.com/rochamaatheus/)", fg="blue", cursor="hand2")
github_label.pack(side=tk.BOTTOM, pady=10)

def open_github(event):
    import webbrowser
    webbrowser.open_new("https://github.com/rochamaatheus/")

github_label.bind("<Button-1>", open_github)

root.mainloop()
