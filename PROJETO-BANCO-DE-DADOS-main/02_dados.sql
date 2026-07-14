-- 5 pacientes
INSERT INTO PESSOA (nome, cpf, data_nascimento, is_flamengo, telefone) VALUES
('Ana Silva', '111.111.111-11', '1990-05-15', TRUE, '83999991111'),
('Gustavo Santos', '222.222.222-22', '1985-10-20', FALSE, '83999992222'),
('Carlos Lima', '333.333.333-33', '2000-01-10', TRUE, '83999993333'),
('Daniela Costa', '444.444.444-44', '1975-08-05', FALSE, '83999994444'),
('Eduardo Melo', '555.555.555-55', '1995-12-30', TRUE, '83999995555');

INSERT INTO PACIENTE (id_pessoa, num_convenio, alergias, grupo_sanguineo, endereco) VALUES
(1, 'UNIMED-001', 'Nenhuma', 'O+', 'Rua A, 100 - Centro'),
(2, 'SULAMERICA-002', 'Dipirona', 'A-', 'Rua B, 200 - Prata'),
(3, NULL, 'Amendoim', 'AB+', 'Rua C, 300 - Malvinas'),
(4, 'BRADESCO-004', 'Nenhuma', 'B+', 'Rua D, 400 - Catolé'),
(5, 'UNIMED-005', 'Iodo', 'O-', 'Rua E, 500 - Bodocongó');

-- 5 residentes
INSERT INTO PESSOA (nome, cpf, data_nascimento, is_flamengo, telefone) VALUES
('Dr. Felipe (R)', '666.666.666-66', '1996-03-12', FALSE, '83999996666'),
('Dra. Gabriela (R)', '777.777.777-77', '1997-07-25', TRUE, '83999997777'),
('Dr. Gabriel (R)', '888.888.888-88', '1995-11-18', FALSE, '83999998888'),
('Dra. Isabella (R)', '999.999.999-99', '1998-02-28', TRUE, '83999999999'),
('Dr. João (R)', '000.000.000-00', '1996-09-09', FALSE, '83999990000');

INSERT INTO PROFISSIONAL (id_pessoa, crm, data_admissao, especialidade) VALUES
(6, 'CRM-PB-1001', '2025-01-10', 'Clínica Médica'),
(7, 'CRM-PB-1002', '2025-01-10', 'Cirurgia Geral'),
(8, 'CRM-PB-1003', '2024-01-10', 'Pediatria'),
(9, 'CRM-PB-1004', '2026-01-10', 'Ortopedia'),
(10, 'CRM-PB-1005', '2025-01-10', 'Clínica Médica');

INSERT INTO RESIDENTE (id_profissional, ano_residencia) VALUES
(6, 'R2'), (7, 'R2'), (8, 'R3'), (9, 'R1'), (10, 'R2');

-- 5 preceptores
INSERT INTO PESSOA (nome, cpf, data_nascimento, is_flamengo, telefone) VALUES
('Dr. Marcos (P)', '121.121.121-12', '1980-04-10', TRUE, '83988881111'),
('Dra. Natalia (P)', '232.232.232-23', '1975-06-22', FALSE, '83988882222'),
('Dr. Otavio (P)', '343.343.343-34', '1982-12-05', TRUE, '83988883333'),
('Dra. Paula (P)', '454.454.454-45', '1978-01-30', FALSE, '83988884444'),
('Dr. Roberto (P)', '565.565.565-56', '1970-08-15', TRUE, '83988885555');

INSERT INTO PROFISSIONAL (id_pessoa, crm, data_admissao, especialidade) VALUES
(11, 'CRM-PB-5001', '2015-03-01', 'Clínica Médica'),
(12, 'CRM-PB-5002', '2010-05-15', 'Cirurgia Geral'),
(13, 'CRM-PB-5003', '2018-07-20', 'Pediatria'),
(14, 'CRM-PB-5004', '2012-02-10', 'Ortopedia'),
(15, 'CRM-PB-5005', '2005-11-01', 'Cardiologia');

INSERT INTO PRECEPTOR (id_profissional, titulacao) VALUES
(11, 'Doutor'), (12, 'Mestre'), (13, 'Especialista'), (14, 'Doutor'), (15, 'Mestre');

-- 3 unidades
INSERT INTO UNIDADE (nome, tipo, capacidade_leitos) VALUES
('Pronto-Socorro Adulto', 'Pronto-Socorro', 20),
('UTI Geral', 'UTI', 15),
('Enfermaria Pediátrica', 'Enfermaria', 30);

-- 10 procedimentos (catalogo do hospital)
INSERT INTO PROCEDIMENTO (codigo, nome, tempo_medio_minutos, nivel_risco) VALUES
('PR-001', 'Sutura Simples', 20, 'BAIXO'),
('PR-002', 'Coleta de Sangue', 10, 'BAIXO'),
('PR-003', 'Aplicação de Medicação IV', 15, 'BAIXO'),
('PR-004', 'Eletrocardiograma', 15, 'BAIXO'),
('PR-005', 'Raio-X de Tórax', 20, 'BAIXO'),
('PR-006', 'Intubação Orotraqueal', 30, 'ALTO'),
('PR-007', 'Curativo Complexo', 45, 'MEDIO'),
('PR-008', 'Acesso Venoso Central', 40, 'ALTO'),
('PR-009', 'Lavagem Gástrica', 25, 'ALTO'),
('PR-010', 'Nebulização', 15, 'BAIXO');

-- 10 atendimentos (as consultas com datas e médicos responsáveis)
INSERT INTO ATENDIMENTO (data_hora, duracao_minutos, id_paciente, id_residente, id_preceptor) VALUES
('2026-07-10 08:30:00', 45, 1, 6, 11),
('2026-07-10 09:15:00', 30, 2, 7, 12),
('2026-07-11 10:00:00', 60, 3, 8, 13),
('2026-07-11 11:30:00', 20, 4, 9, 14),
('2026-07-12 14:00:00', 90, 5, 10, 11),
('2026-07-12 15:45:00', 15, 1, 6, 15),
('2026-07-13 07:00:00', 120, 2, 7, 12),
('2026-07-13 09:30:00', 25, 3, 8, 13),
('2026-07-13 10:15:00', 35, 4, 9, 14),
('2026-07-13 11:00:00', 40, 5, 10, 11);

-- 10 procedimentos realizados (ligando o que foi feito em qual consulta)
INSERT INTO PROCEDIMENTO_REALIZADO (id_atendimento, id_procedimento, quantidade, tempo_real_minutos, observacao) VALUES
(1, 1, 1, 25, 'Paciente agitado'),
(2, 2, 2, 15, 'Veia de difícil acesso'),
(3, 3, 1, 10, 'Sem intercorrências'),
(4, 4, 1, 20, 'Ritmo sinusal regular'),
(5, 6, 1, 35, 'Via aérea difícil'),
(6, 10, 1, 15, 'Boa resposta clínica'),
(7, 8, 1, 45, 'Sucesso na primeira tentativa'),
(8, 2, 1, 5, 'Rápido e eficiente'),
(9, 5, 1, 20, 'Imagem de boa qualidade'),
(10, 7, 1, 50, 'Lesão extensa');

-- Dados de teste para ESCALA (plantões escalados)
-- Usando as 3 unidades, os 5 residentes e os 5 preceptores já
-- cadastrados em 02_dados.sql. Datas dentro de julho/2026 para
-- representar o "mês corrente" da consulta analítica.

INSERT INTO ESCALA (id_unidade, dia_semana, turno, id_residente, id_preceptor, data_plantao) VALUES
(1, 'Segunda', 'Manhã', 6, 11, '2026-07-06'),
(1, 'Terça',   'Tarde', 7, 12, '2026-07-07'),
(2, 'Quarta',  'Noite', 8, 13, '2026-07-08'),
(2, 'Quinta',  'Manhã', 9, 14, '2026-07-09'),
(3, 'Sexta',   'Tarde', 10, 11, '2026-07-10'),
(1, 'Sábado',  'Noite', 6, 15, '2026-07-11'),
(2, 'Domingo', 'Manhã', 7, 12, '2026-07-12'),
(3, 'Segunda', 'Tarde', 8, 13, '2026-07-13'),
(1, 'Terça',   'Noite', 9, 14, '2026-07-14'),
(2, 'Quarta',  'Manhã', 10, 11, '2026-07-15');
