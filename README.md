
# Downloader de Vídeos e Áudios do YouTube

Este aplicativo em Python oferece uma interface simples para baixar vídeos e áudios do YouTube usando `yt-dlp` e `Tkinter`. O aplicativo suporta download de vídeos e áudios, incluindo a extração de áudio em MP3 de arquivos de vídeo.

- Nota: Você pode apenas instalar o arquivos executável e utilizá-lo normalmente, se preferir.

## Funcionalidades
- Baixa vídeos no melhor formato disponível.
- Extrai e baixa áudios como MP3.
- Interface gráfica simples para selecionar um arquivo contendo URLs do YouTube.
- Integração local com `ffmpeg` para processamento de mídia.

## Requisitos
- Python 3.x
- `yt-dlp` (Pode ser instalado via `pip install yt-dlp`)
- `Tkinter` (geralmente incluído com as instalações do Python)
- `ffmpeg` (incluído no diretório `bin` deste repositório)

## Como Usar

1. **Clone o Repositório**:
    ```bash
    git clone https://github.com/rochamaatheus/Baixar_mp3_mp4.git
    ```

2. **Certifique-se de que os pacotes Python necessários estão instalados**:
    ```bash
    pip install yt-dlp
    ```

3. **Execute o Aplicativo**:
    ```bash
    python baixar_mp3_mp4.py
    ```

4. **Selecione um Arquivo de Texto Contendo URLs do YouTube**:
    - Crie um arquivo `.txt` com cada URL do YouTube em uma nova linha.
    - Adicione `-mp3` ao final de qualquer URL para baixar apenas o áudio em formato MP3.

5. **Downloads**:
    - Os vídeos serão salvos no diretório `videos`.
    - Os áudios serão salvos no diretório `audios`.

## Exemplo de Arquivo .txt
```
https://www.youtube.com/watch?v=video
https://www.youtube.com/watch?v=video2 -mp3
```

## Notas
- Certifique-se de que `ffmpeg.exe` está localizado no diretório `bin` conforme fornecido neste repositório.
- Este aplicativo lida com tentativas automáticas de download de fragmentos de arquivos grandes para garantir a confiabilidade.
- Você pode usar apenas o arquivo executável (sendo assim, pode ignorar as configurações fornecidas)

## Contato

Se você tiver alguma dúvida ou precisar de assistência adicional, fique à vontade para entrar em contato através do LinkedIn, Instagram ou por e-mail. As informações de contato estão disponíveis na minha página principal do GitHub.

---

👨‍💻 Criado por [rochamaatheus](https://github.com/rochamaatheus).
