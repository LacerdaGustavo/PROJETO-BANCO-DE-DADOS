-- ranking dos residentes por número de atendimentos realizados

SELECT
    pe.nome AS nome_residente,
    COUNT(a.id_atendimento) AS total_atendimentos
FROM RESIDENTE r
JOIN PROFISSIONAL pr ON pr.id_pessoa = r.id_profissional
JOIN PESSOA pe ON pe.id_pessoa = pr.id_pessoa
JOIN ATENDIMENTO a ON a.id_residente = r.id_profissional
GROUP BY pe.nome
ORDER BY total_atendimentos DESC;

-- lista os preceptores que supervisionaram mais de 5 atendimentos em um determinado mês

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

-- mostrar a quantidade de plantões escalados por residente no mês corrente (em cada unidade)

SELECT
    u.nome AS unidade,
    pe.nome AS nome_residente,
    COUNT(e.id_escala) AS qtd_plantoes
FROM ESCALA e
JOIN UNIDADE u ON u.id_unidade = e.id_unidade
JOIN RESIDENTE r ON r.id_profissional = e.id_residente
JOIN PROFISSIONAL pr ON pr.id_pessoa = r.id_profissional
JOIN PESSOA pe ON pe.id_pessoa = pr.id_pessoa
GROUP BY u.nome, pe.nome
ORDER BY u.nome, qtd_plantoes DESC;


-- a consulta abaixo lista os pacientes que não tiveram atendimentos com procedimentos de alto risco, usando JOINs e subquery para filtrar os pacientes que tiveram atendimentos com procedimentos de alto risco!!!! se atentem a essa add

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
