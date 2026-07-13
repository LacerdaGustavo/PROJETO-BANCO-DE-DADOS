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
HAVING COUNT(a.id_atendimento) > 5
ORDER BY total_atendimentos DESC;
