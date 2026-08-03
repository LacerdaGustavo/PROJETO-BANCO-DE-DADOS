import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox  # Importado para mostrar o aviso da simulação

# Importações originais do seu projeto
from database import (
    calcular_tempo_medio_residente,
    ranking_residentes,
    preceptores_mes,
    plantoes_residente,
    pacientes_sem_risco_alto
)

# Novas importações das Consultas Avançadas e Concorrência (ORM)
from backend.database import SessionLocal
from backend.consultas_avancadas import (
    preceptores_pacientes_flamenguistas,
    ultimo_atendimento_pacientes,
    percentual_risco_alto_residentes
)
from backend.concorrencia import simular_concorrencia


def criar_tela(parent):

    # Executa a consulta escolhida
    def executar():

        consulta = combo_consulta.get()

        # Limpa a tabela
        for item in tabela.get_children():
            tabela.delete(item)

        # Remove colunas antigas
        tabela["columns"] = ()

        # --- CONSULTAS ORIGINAIS DO GRUPO ---
        
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
        elif consulta == "Pacientes sem procedimento ALTO":
            dados = pacientes_sem_risco_alto()
            tabela["columns"] = ("Paciente",)
            tabela.heading("Paciente", text="Paciente")
            tabela.column("Paciente", width=450)

        # --- NOVAS CONSULTAS (ORM / PONTO 6.1) ---
        
        elif consulta == "Preceptores (Pacientes Flamenguistas)":
            session = SessionLocal()
            try:
                dados_orm = preceptores_pacientes_flamenguistas(session)
                tabela["columns"] = ("Preceptor",)
                tabela.heading("Preceptor", text="Nome do Preceptor")
                tabela.column("Preceptor", width=450)
                # Converte o objeto do SQLAlchemy para o formato que a tabela entende
                dados = [(row.nome_preceptor,) for row in dados_orm]
            finally:
                session.close()

        elif consulta == "Último Atendimento por Paciente":
            session = SessionLocal()
            try:
                dados_orm = ultimo_atendimento_pacientes(session)
                tabela["columns"] = ("Paciente", "Data/Hora", "Residente", "Preceptor", "Procedimentos")
                tabela.heading("Paciente", text="Paciente")
                tabela.heading("Data/Hora", text="Data/Hora")
                tabela.heading("Residente", text="Residente")
                tabela.heading("Preceptor", text="Preceptor")
                tabela.heading("Procedimentos", text="Procedimentos")
                
                tabela.column("Paciente", width=150)
                tabela.column("Data/Hora", width=120, anchor="center")
                tabela.column("Residente", width=120)
                tabela.column("Preceptor", width=120)
                tabela.column("Procedimentos", width=200)
                
                dados = [(row.nome_paciente, row.data_hora, row.nome_residente, row.nome_preceptor, row.procedimentos) for row in dados_orm]
            finally:
                session.close()

        elif consulta == "Risco Alto por Residente":
            session = SessionLocal()
            try:
                dados_orm = percentual_risco_alto_residentes(session)
                tabela["columns"] = ("Residente", "Total", "Alto Risco", "Percentual")
                tabela.heading("Residente", text="Residente")
                tabela.heading("Total", text="Total Proc.")
                tabela.heading("Alto Risco", text="Qtd Alto Risco")
                tabela.heading("Percentual", text="Percentual (%)")
                
                tabela.column("Residente", width=250)
                tabela.column("Total", width=100, anchor="center")
                tabela.column("Alto Risco", width=100, anchor="center")
                tabela.column("Percentual", width=100, anchor="center")
                
                dados = [(row['residente'], row['total_procedimentos'], row['total_alto_risco'], row['percentual']) for row in dados_orm]
            finally:
                session.close()

        # --- SIMULAÇÃO DE CONCORRÊNCIA (PONTO 6) ---
        
        elif consulta == "Simular Concorrência (Ver Terminal)":
            simular_concorrencia()
            messagebox.showinfo("Simulação Concluída", "A simulação de concorrência disparou!\n\nProfessor, verifique o terminal do VS Code para ver os logs do Lock Pessimista funcionando em tempo real.")
            
            tabela["columns"] = ("Status",)
            tabela.heading("Status", text="Status da Execução")
            tabela.column("Status", width=450)
            dados = [("Simulação executada com sucesso. Logs registrados no terminal.",)]

        tabela["show"] = "headings"

        # Insere os dados processados na tabela visual
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
        width=350, # Aumentado levemente para caber as opções novas
        values=[
            "Tempo médio por residente",
            "Ranking dos residentes",
            "Preceptores (>5 atendimentos)",
            "Plantões por residente",
            "Pacientes sem procedimento ALTO",
            # Novas opções inseridas abaixo:
            "Preceptores (Pacientes Flamenguistas)",
            "Último Atendimento por Paciente",
            "Risco Alto por Residente",
            "Simular Concorrência (Ver Terminal)"
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