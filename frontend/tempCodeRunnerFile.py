import customtkinter as ctk

# Importando as telas
from views.inicio import criar_tela as tela_inicio
from views.pacientes import criar_tela as tela_pacientes
from views.atendimento import criar_tela as tela_atendimento
from views.procedimentos import criar_tela as tela_procedimentos
from views.consultas import criar_tela as tela_consultas

# Configuração
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Janela principal
app = ctk.CTk()
app.title("Sistema de Gestão Hospitalar")
app.geometry("1200x700")

# ---------------- MENU ----------------

menu = ctk.CTkFrame(app, width=220)
menu.pack(side="left", fill="y")

titulo = ctk.CTkLabel(
    menu,
    text="🏥 Hospital",
    font=("Arial", 24, "bold")
)
titulo.pack(pady=30)

# ---------------- ÁREA PRINCIPAL ----------------

conteudo = ctk.CTkFrame(app)
conteudo.pack(side="right", fill="both", expand=True)


# Função que limpa a tela
def limpar_tela():
    for widget in conteudo.winfo_children():
        widget.destroy()


# Função que troca de tela
def mostrar_tela(tela):
    limpar_tela()
    tela(conteudo)


# ---------------- BOTÕES ----------------

btn_inicio = ctk.CTkButton(
    menu,
    text="Início",
    command=lambda: mostrar_tela(tela_inicio)
)
btn_inicio.pack(pady=10, padx=20)

btn_atendimento = ctk.CTkButton(
    menu,
    text="Atendimento",
    command=lambda: mostrar_tela(tela_atendimento)
)
btn_atendimento.pack(pady=10, padx=20)

btn_pacientes = ctk.CTkButton(
    menu,
    text="Pacientes",
    command=lambda: mostrar_tela(tela_pacientes)
)
btn_pacientes.pack(pady=10, padx=20)

btn_procedimentos = ctk.CTkButton(
    menu,
    text="Procedimentos",
    command=lambda: mostrar_tela(tela_procedimentos)
)
btn_procedimentos.pack(pady=10, padx=20)

btn_consultas = ctk.CTkButton(
    menu,
    text="Consultas",
    command=lambda: mostrar_tela(tela_consultas)
)
btn_consultas.pack(pady=10, padx=20)

# Tela inicial
mostrar_tela(tela_inicio)

app.mainloop()