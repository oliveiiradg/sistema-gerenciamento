import customtkinter as ctk


def criar_titulo(parent):
    frame_titulo = ctk.CTkFrame(parent, fg_color="transparent")
    frame_titulo.pack(fill="x", pady=(10, 20))

    titulo = ctk.CTkLabel(
        frame_titulo,
        text="Controle GoldStore",
        font=ctk.CTkFont(size=24, weight="bold")
    )
    titulo.pack()

    subtitulo = ctk.CTkLabel(
        frame_titulo,
        text="Sistema de Gerenciamento de Serviços",
        font=ctk.CTkFont(size=14)
    )
    subtitulo.pack()
