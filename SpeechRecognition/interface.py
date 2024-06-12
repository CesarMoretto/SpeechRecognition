import tkinter as tk
from tkinter import ttk
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import threading

class CapturaAudioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Captura de Áudio e Transcrição")

        # Cores personalizadas
        self.bg_color = "#1871C2"  
        self.btn_color = "#4682B4" 
        self.btn_hover_color = "#5CACEE"  
        self.btn_text_color = "#000000" 
        self.text_color = "#FFFFFF"  
        self.entry_bg_color = "#FFFFFF"  
        self.frame_color = "#1E4363"  
        self.frame_text_color = "#FFFFFF" 

        # Configuração da janela
        self.root.geometry("500x400")
        self.root.configure(bg=self.bg_color)

        # Imagem
        self.img = tk.PhotoImage(file="imgsa.png")
        self.img_label = tk.Label(root, image=self.img, bg=self.bg_color)
        self.img_label.pack(pady=5)

        # Widgets
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Helvetica', 12), background=self.bg_color, foreground=self.text_color)
        self.style.configure('TButton', font=('Helvetica', 12), background=self.btn_color, foreground=self.btn_text_color)
        self.style.map('TButton', background=[('active', self.btn_hover_color)])
        self.style.configure('TEntry', font=('Helvetica', 12), background=self.entry_bg_color)
        self.style.configure('TFrame', background=self.frame_color)

        # Configuração dos widgets
        self.lbl_status = ttk.Label(root, text="", style='TLabel')
        self.lbl_status.pack(pady=(0, 5))

        self.lbl_duracao = ttk.Label(root, text="Duração (segundos):", style='TLabel')
        self.lbl_duracao.pack()

        self.ent_duracao = ttk.Entry(root, style='TEntry')
        self.ent_duracao.pack()

        self.btn_iniciar = ttk.Button(root, text="Iniciar Captura", command=self.iniciar_captura, style='TButton')
        self.btn_iniciar.pack(pady=10)

        self.btn_parar = ttk.Button(root, text="Parar Captura", command=self.parar_captura, state=tk.DISABLED, style='TButton')
        self.btn_parar.pack()

        self.frame_transcricao = ttk.Frame(root, style='TFrame', relief=tk.GROOVE, padding=(10, 10, 10, 10))
        self.frame_transcricao.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        self.lbl_transcricao = tk.Label(self.frame_transcricao, text="", font=('Helvetica', 14, 'bold'), bg=self.frame_color, fg=self.frame_text_color, wraplength=400)
        self.lbl_transcricao.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        self.lbl_transcricao.config(anchor=tk.CENTER)

        self.gravando = False

    def iniciar_captura(self):
        duracao_captura = int(self.ent_duracao.get()) if self.ent_duracao.get().isdigit() else 5
        arquivo_audio = "captura.wav"

        self.lbl_status.config(text="Capturando áudio... Pressione o botão 'Parar Captura' para parar.")
        self.btn_iniciar.config(state=tk.DISABLED)
        self.btn_parar.config(state=tk.NORMAL)

        self.gravando = True
        self.audio_gravado = []
        self.taxa_amostragem = 0
        self.gravacao_thread = threading.Thread(target=self.capturar_audio, args=(duracao_captura,))
        self.gravacao_thread.start()

    def parar_captura(self):
        self.gravando = False
        self.lbl_status.config(text="Parando a captura de áudio...")

    def capturar_audio(self, duracao, samplerate=44100, channels=2):
        self.audio_gravado = sd.rec(int(duracao * samplerate), samplerate=samplerate, channels=channels, dtype='int16')
        self.taxa_amostragem = samplerate
        sd.wait()

        if self.gravando:
            self.salvar_audio("captura.wav", self.audio_gravado, samplerate)
            self.lbl_status.config(text="Áudio capturado com sucesso. Transcrição:")
            texto_transcrito = self.transcrever_audio("captura.wav")
            self.lbl_transcricao.config(text=texto_transcrito)
            self.btn_iniciar.config(state=tk.NORMAL)
            self.btn_parar.config(state=tk.DISABLED)
        else:
            self.lbl_status.config(text="Captura de áudio interrompida pelo usuário.")
            self.btn_iniciar.config(state=tk.NORMAL)
            self.btn_parar.config(state=tk.DISABLED)

    def salvar_audio(self, arquivo, data, samplerate):
        sf.write(arquivo, data, samplerate)

    def transcrever_audio(self, arquivo_audio):
        recognizer = sr.Recognizer()
        with sr.AudioFile(arquivo_audio) as source:
            audio = recognizer.record(source)

        try:
            texto = recognizer.recognize_google(audio, language='pt-BR')
            return texto
        except sr.UnknownValueError:
            return "Não foi possível entender a fala"
        except sr.RequestError as e:
            return f"Erro ao fazer a requisição ao serviço de reconhecimento de fala; {e}"


if __name__ == "__main__":
    root = tk.Tk()
    app = CapturaAudioApp(root)
    root.mainloop()
