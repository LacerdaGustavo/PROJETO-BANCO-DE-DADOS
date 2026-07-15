import customtkinter as ctk

def criar_tela(parent):

    titulo = ctk.CTkLabel(
        parent,
        text="Sistema de Gestão Hospitalar",
        font=("Arial", 28, "bold")
    )

    titulo.pack(pady=(50,20))

    texto = ctk.CTkLabel(
        parent,
        text="Projeto da disciplina Banco de Dados I\n\nEscolha uma opção no menu lateral.",
        font=("Arial",18)
    )

    texto.pack()