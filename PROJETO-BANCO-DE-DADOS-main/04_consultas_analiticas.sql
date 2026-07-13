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
