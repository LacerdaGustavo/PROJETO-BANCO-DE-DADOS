-- tabela base para pacientes e médicos
CREATE TABLE PESSOA (
    id_pessoa SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    data_nascimento DATE NOT NULL,
    is_flamengo BOOLEAN NOT NULL,
    telefone VARCHAR(20)
);

-- do paciente
CREATE TABLE PACIENTE (
    id_pessoa INT PRIMARY KEY,
    num_convenio VARCHAR(50),
    alergias TEXT,
    grupo_sanguineo VARCHAR(3),
    endereco VARCHAR(255),
    FOREIGN KEY (id_pessoa) REFERENCES PESSOA(id_pessoa) ON DELETE CASCADE
);

-- profissional de saude
CREATE TABLE PROFISSIONAL (
    id_pessoa INT PRIMARY KEY,
    crm VARCHAR(20) UNIQUE NOT NULL,
    data_admissao DATE NOT NULL,
    especialidade VARCHAR(100) NOT NULL,
    FOREIGN KEY (id_pessoa) REFERENCES PESSOA(id_pessoa) ON DELETE CASCADE
);

-- preceptor (supervisor)
CREATE TABLE PRECEPTOR (
    id_profissional INT PRIMARY KEY,
    titulacao VARCHAR(50) NOT NULL,
    FOREIGN KEY (id_profissional) REFERENCES PROFISSIONAL(id_pessoa) ON DELETE CASCADE
);

-- residente (aluno)
CREATE TABLE RESIDENTE (
    id_profissional INT PRIMARY KEY,
    ano_residencia VARCHAR(2) NOT NULL,
    FOREIGN KEY (id_profissional) REFERENCES PROFISSIONAL(id_pessoa) ON DELETE CASCADE,
    CHECK (ano_residencia IN ('R1', 'R2', 'R3')) 
);

-- unidade (local do atendimento)
CREATE TABLE UNIDADE (
    id_unidade SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    capacidade_leitos INT NOT NULL
);

-- escala (coloquei UNIQUE composto)
CREATE TABLE ESCALA (
    id_escala SERIAL PRIMARY KEY,
    id_unidade INT NOT NULL,
    dia_semana VARCHAR(20) NOT NULL,
    turno VARCHAR(10) NOT NULL,
    id_residente INT NOT NULL,
    id_preceptor INT NOT NULL,
    data_plantao DATE NOT NULL DEFAULT CURRENT_DATE,
    FOREIGN KEY (id_unidade) REFERENCES UNIDADE(id_unidade),
    FOREIGN KEY (id_residente) REFERENCES RESIDENTE(id_profissional),
    FOREIGN KEY (id_preceptor) REFERENCES PRECEPTOR(id_profissional),
    UNIQUE (id_unidade, dia_semana, turno, id_residente),
    CHECK (turno IN ('Manhã', 'Tarde', 'Noite'))
);

-- atendimento/a consulta em si
CREATE TABLE ATENDIMENTO (
    id_atendimento SERIAL PRIMARY KEY,
    data_hora TIMESTAMP NOT NULL,
    duracao_minutos INT NOT NULL,
    id_paciente INT NOT NULL,
    id_residente INT NOT NULL,
    id_preceptor INT NOT NULL,
    FOREIGN KEY (id_paciente) REFERENCES PACIENTE(id_pessoa),
    FOREIGN KEY (id_residente) REFERENCES RESIDENTE(id_profissional),
    FOREIGN KEY (id_preceptor) REFERENCES PRECEPTOR(id_profissional)
);

-- procedimento (catálogo do hospital)
CREATE TABLE PROCEDIMENTO (
    id_procedimento SERIAL PRIMARY KEY,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    nome VARCHAR(150) NOT NULL,
    tempo_medio_minutos INT NOT NULL
    nivel_risco VARCHAR(10) NOT NULL DEFAULT 'BAIXO',
    CHECK (nivel_risco IN ('BAIXO', 'MEDIO', 'ALTO'))
);

-- procedimento realizado (o que foi feito na consulta)
CREATE TABLE PROCEDIMENTO_REALIZADO (
    id_atendimento INT NOT NULL,
    id_procedimento INT NOT NULL,
    quantidade INT NOT NULL DEFAULT 1,
    tempo_real_minutos INT NOT NULL,
    observacao TEXT,
    faturado BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (id_atendimento, id_procedimento),
    FOREIGN KEY (id_atendimento) REFERENCES ATENDIMENTO(id_atendimento) ON DELETE CASCADE,
    FOREIGN KEY (id_procedimento) REFERENCES PROCEDIMENTO(id_procedimento)
);

