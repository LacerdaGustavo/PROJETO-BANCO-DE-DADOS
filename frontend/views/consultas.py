import customtkinter as ctk
from tkinter import ttk

from database import (
    calcular_tempo_medio_residente,
    ranking_residentes,
    preceptores_mes,
    plantoes_residente,
    pacientes_sem_risco_alto
)


def criar_tela(parent):

    
    # Executa a consulta escolhida
   
    def executar():

        consulta = combo_consulta.get()

        # Limpa a tabela
        for item in tabela.get_children():
            tabela.delete(item)

        # Remove colunas antigas
        tabela["columns"] = ()

        
        # Tempo médio

        if consulta == "Tempo médio por residente":

            dados = calcular_tempo_medio_residente()

            tabela["columns"] = ("Residente", "Tempo")

            tabela.heading("Residente", text="Residente")
            tabela.heading("Tempo", text="Tempo Médio (min)")

            tabela.column("Residente", width=350)
            tabela.column("Tempo", width=180, anchor="center")

        # Ranking
        
        elif consulta == "Ranking dos residentes":

            dados = ranking_residentes()

            tabela["columns"] = ("Residente", "Total")

            tabela.heading("Residente", text="Residente")
            tabela.heading("Total", text="Atendimentos")

            tabela.column("Residente", width=350)
            tabela.column("Total", width=180, anchor="center")

        
        # Preceptores
       
        elif consulta == "Preceptores (>5 atendimentos)":

            mes = int(entrada_mes.get())
            ano = int(entrada_ano.get())

            dados = preceptores_mes(mes, ano)

            tabela["columns"] = ("Preceptor", "Total")

            tabela.heading("Preceptor", text="Preceptor")
            tabela.heading("Total", text="Atendimentos")

            tabela.column("Preceptor", width=350)
            tabela.column("Total", width=180, anchor="center")

       
        # Plantões
        
        elif consulta == "Plantões por residente":

            dados = plantoes_residente()

            tabela["columns"] = (
                "Unidade",
                "Residente",
                "Plantões"
            )

            tabela.heading("Unidade", text="Unidade")
            tabela.heading("Residente", text="Residente")
            tabela.heading("Plantões", text="Quantidade")

            tabela.column("Unidade", width=220)
            tabela.column("Residente", width=250)
            tabela.column("Plantões", width=120, anchor="center")

       
        # Pacientes sem risco alto
       
        else:

            dados = pacientes_sem_risco_alto()

            tabela["columns"] = ("Paciente",)

            tabela.heading("Paciente", text="Paciente")

            tabela.column("Paciente", width=450)

        tabela["show"] = "headings"

        for linha in dados:
            tabela.insert("", "end", values=linha)

  
    # Título
   
    titulo = ctk.CTkLabel(
        parent,
        text="Consultas Analíticas",
        font=("Arial", 28, "bold")
    )

    titulo.pack(pady=20)

    
    # Barra superior

    barra = ctk.CTkFrame(parent)

    barra.pack(fill="x", padx=20)

    combo_consulta = ctk.CTkComboBox(

        barra,

        width=300,

        values=[

            "Tempo médio por residente",

            "Ranking dos residentes",

            "Preceptores (>5 atendimentos)",

            "Plantões por residente",

            "Pacientes sem procedimento ALTO"

        ]
    )

    combo_consulta.pack(side="left", padx=10, pady=10)

    combo_consulta.set("Tempo médio por residente")

    entrada_mes = ctk.CTkEntry(
        barra,
        width=60,
        placeholder_text="Mês"
    )

    entrada_mes.pack(side="left", padx=5)

    entrada_ano = ctk.CTkEntry(
        barra,
        width=80,
        placeholder_text="Ano"
    )

    entrada_ano.pack(side="left", padx=5)

    ctk.CTkButton(

        barra,

        text="Executar",

        command=executar

    ).pack(side="left", padx=10)

    
    # Tabela
    
    tabela = ttk.Treeview(parent)

    tabela.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    # Carrega a primeira consulta automaticamente

    executar()