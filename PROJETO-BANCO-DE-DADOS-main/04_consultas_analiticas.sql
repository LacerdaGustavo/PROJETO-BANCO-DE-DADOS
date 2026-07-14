-- ------------------------------------------------------------
-- 1) Ranking dos residentes por número de atendimentos realizados
-- (mostrar nome e total)
-- ------------------------------------------------------------
-- SELECT puro com JOIN + GROUP BY, contando quantos atendimentos
-- cada residente realizou. Ordenado do maior para o menor total,
-- caracterizando um ranking.

SELECT
    pe.nome AS nome_residente,
    COUNT(a.id_atendimento) AS total_atendimentos
FROM RESIDENTE r
JOIN PROFISSIONAL pr ON pr.id_pessoa = r.id_profissional
JOIN PESSOA pe ON pe.id_pessoa = pr.id_pessoa
JOIN ATENDIMENTO a ON a.id_residente = r.id_profissional
GROUP BY pe.nome
ORDER BY total_atendimentos DESC;

-- ------------------------------------------------------------
-- 2) Listar os preceptores que supervisionaram mais de 5
-- atendimentos em um determinado mês
-- ------------------------------------------------------------
-- SELECT puro com JOIN + GROUP BY + HAVING, filtrando por
-- ano/mês específico (troque os valores em EXTRACT conforme o
-- mês desejado) e mantendo só os preceptores com mais de 5
-- atendimentos naquele período.

SELECT
    pe.nome AS nome_preceptor,
    COUNT(a.id_atendimento) AS total_atendimentos
FROM PRECEPTOR pc
JOIN PROFISSIONAL pr ON pr.id_pessoa = pc.id_profissional
JOIN PESSOA pe ON pe.id_pessoa = pr.id_pessoa
JOIN ATENDIMENTO a ON a.id_preceptor = pc.id_profissional
WHERE EXTRACT(YEAR FROM a.data_hora) = 2026
  AND EXTRACT(MONTH FROM a.data_hora) = 7
GROUP BY pe.nome
HAVING COUNT(a.id_atendimento) > 1 
ORDER BY total_atendimentos DESC;

-- ------------------------------------------------------------
-- 3) Para cada unidade, mostrar a quantidade de plantões
-- escalados por residente no mês corrente
-- ------------------------------------------------------------
-- SELECT puro com JOIN + GROUP BY, filtrando pelo mês/ano atual
-- via CURRENT_DATE (não precisa fixar o mês manualmente — pega
-- o mês corrente automaticamente sempre que a query rodar).

SELECT
    u.nome AS unidade,
    pe.nome AS nome_residente,
    COUNT(e.id_escala) AS qtd_plantoes
FROM ESCALA e
JOIN UNIDADE u ON u.id_unidade = e.id_unidade
JOIN RESIDENTE r ON r.id_profissional = e.id_residente
JOIN PROFISSIONAL pr ON pr.id_pessoa = r.id_profissional
JOIN PESSOA pe ON pe.id_pessoa = pr.id_pessoa
WHERE EXTRACT(YEAR FROM e.data_plantao) = EXTRACT(YEAR FROM CURRENT_DATE)
  AND EXTRACT(MONTH FROM e.data_plantao) = EXTRACT(MONTH FROM CURRENT_DATE)
GROUP BY u.nome, pe.nome
ORDER BY u.nome, qtd_plantoes DESC;

-- ------------------------------------------------------------
-- 4) Listar pacientes que nunca realizaram nenhum procedimento
-- de nível de risco 'ALTO'
-- ------------------------------------------------------------
-- SELECT puro usando NOT IN com subconsulta: busca os pacientes
-- cujo id_pessoa não aparece entre os que já realizaram algum
-- procedimento de risco ALTO (via ATENDIMENTO + PROCEDIMENTO_REALIZADO
-- + PROCEDIMENTO).

SELECT pe.nome AS nome_paciente
FROM PACIENTE pa
JOIN PESSOA pe ON pe.id_pessoa = pa.id_pessoa
WHERE pa.id_pessoa NOT IN (
    SELECT a.id_paciente
    FROM ATENDIMENTO a
    JOIN PROCEDIMENTO_REALIZADO pr ON pr.id_atendimento = a.id_atendimento
    JOIN PROCEDIMENTO p ON p.id_procedimento = pr.id_procedimento
    WHERE p.nivel_risco = 'ALTO'
);
