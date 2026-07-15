# Sistema de Gestão Hospitalar

Projeto desenvolvido para a disciplina de Banco de Dados da Universidade Federal da Paraíba (UFPB).

O sistema foi desenvolvido em Python utilizando CustomTkinter como interface gráfica e PostgreSQL como banco de dados.

## Funcionalidades

### Pacientes
- Cadastrar paciente
- Listar pacientes
- Editar paciente
- Excluir paciente

### Atendimentos
- Cadastrar atendimento
- Listar atendimentos
- Pesquisar atendimentos por paciente

### Procedimentos
- Listar procedimentos realizados em um atendimento
- Remover procedimento (quando não faturado)

### Consultas Analíticas
- Tempo médio de duração dos atendimentos por residente
- Ranking de residentes por número de atendimentos
- Preceptores com mais de 5 atendimentos em um determinado mês
- Quantidade de plantões por residente no mês corrente
- Pacientes que nunca realizaram procedimento de risco ALTO

---

# Tecnologias utilizadas

- Python 3.11
- PostgreSQL
- psycopg2
- CustomTkinter
- Tkinter

---

# Instalação

## 1. Clonar o repositório

```bash
git clone https://github.com/SEU-USUARIO/PROJETO-BANCO-DE-DADOS.git
```

Entre na pasta do projeto:

```bash
cd PROJETO-BANCO-DE-DADOS
```

---

## 2. Instalar as dependências

Instale as bibliotecas utilizadas:

```bash
pip install customtkinter
pip install psycopg2
```

Ou:

```bash
pip install customtkinter psycopg2
```

---

## 3. Criar o banco de dados

No PostgreSQL:

Crie um banco chamado:

```
hospital
```

Execute o script SQL fornecido no projeto para criar todas as tabelas.

---

## 4. Configurar a conexão

No arquivo

```
frontend/database.py
```

altere as informações de conexão conforme seu PostgreSQL:

```python
host="localhost"
database="hospital"
user="postgres"
password="SUA_SENHA"
```

---

# Execução

Entre na pasta frontend:

```bash
cd frontend
```

Execute:

```bash
python main.py
```

---

# Estrutura do projeto

```
frontend/
│
├── views/
│   ├── atendimento.py
│   ├── consultas.py
│   ├── inicio.py
│   ├── pacientes.py
│   └── procedimentos.py
│
├── database.py
└── main.py
```

---

# Autores

- Gustavo Lacerda
- Isabella Sousa
- Gabriel Simplício
