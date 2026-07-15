-- novo atendimento e verificar se paciente, residente e preceptor existem

INSERT INTO ATENDIMENTO (data_hora, duracao_minutos, id_paciente, id_residente, id_preceptor)
SELECT '2026-07-14 08:00:00', 30, 1, 6, 11
WHERE EXISTS (SELECT 1 FROM PACIENTE WHERE id_pessoa = 1)
  AND EXISTS (SELECT 1 FROM RESIDENTE WHERE id_profissional = 6)
  AND EXISTS (SELECT 1 FROM PRECEPTOR WHERE id_profissional = 11);


-- lista todos os atendimentos de um paciente específico (por data)

SELECT id_atendimento, data_hora, duracao_minutos, id_residente, id_preceptor
FROM ATENDIMENTO
WHERE id_paciente = 1
ORDER BY data_hora ASC;


-- lista os procedimentos realizados em um atendimento (nome do procedimento, quantidade e tempo real)

SELECT p.nome, pr.quantidade, pr.tempo_real_minutos
FROM PROCEDIMENTO_REALIZADO pr
JOIN PROCEDIMENTO p ON p.id_procedimento = pr.id_procedimento
WHERE pr.id_atendimento = 1;


-- atualiza os dados de um paciente

UPDATE PACIENTE
SET endereco     = 'Rua das Flores, 123 - Campina Grande/PB',
    num_convenio = 'HAPVIDA-777'
WHERE id_pessoa = 1;


-- remover um procedimento realizado

DELETE FROM PROCEDIMENTO_REALIZADO
WHERE id_atendimento = 6
  AND id_procedimento = 10
  AND faturado = FALSE;

-- tempo médio de duração dos atendimentos

SELECT
    r.id_profissional AS id_residente,
    pe.nome AS nome_residente,
    COUNT(a.id_atendimento) AS qtd_atendimentos,
    ROUND(AVG(a.duracao_minutos), 2) AS tempo_medio_minutos
FROM RESIDENTE r
JOIN PROFISSIONAL pr ON pr.id_pessoa = r.id_profissional
JOIN PESSOA pe ON pe.id_pessoa = pr.id_pessoa
JOIN ATENDIMENTO a ON a.id_residente = r.id_profissional
GROUP BY r.id_profissional, pe.nome
ORDER BY tempo_medio_minutos DESC;