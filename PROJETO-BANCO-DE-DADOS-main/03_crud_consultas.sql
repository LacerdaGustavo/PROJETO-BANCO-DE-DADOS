-- ------------------------------------------------------------
-- 1) Inserir um novo atendimento
-- (verificando se paciente, residente e preceptor existem)
-- ------------------------------------------------------------
-- Insert condicional em SQL puro: o INSERT só ocorre se as três
-- condições de existência (paciente, residente, preceptor) forem
-- verdadeiras ao mesmo tempo. Se qualquer uma delas não existir,
-- nenhuma linha é inserida (0 rows affected).
-- ------------------------------------------------------------

INSERT INTO ATENDIMENTO (data_hora, duracao_minutos, id_paciente, id_residente, id_preceptor)
SELECT '2026-07-14 08:00:00', 30, 1, 6, 11
WHERE EXISTS (SELECT 1 FROM PACIENTE WHERE id_pessoa = 1)
  AND EXISTS (SELECT 1 FROM RESIDENTE WHERE id_profissional = 6)
  AND EXISTS (SELECT 1 FROM PRECEPTOR WHERE id_profissional = 11);

-- Exemplo de uso inválido: paciente 999 não existe, deve inserir 0 linhas
-- INSERT INTO ATENDIMENTO (data_hora, duracao_minutos, id_paciente, id_residente, id_preceptor)
-- SELECT '2026-07-14 09:00:00', 30, 999, 6, 11
-- WHERE EXISTS (SELECT 1 FROM PACIENTE WHERE id_pessoa = 999)
--   AND EXISTS (SELECT 1 FROM RESIDENTE WHERE id_profissional = 6)
--   AND EXISTS (SELECT 1 FROM PRECEPTOR WHERE id_profissional = 11);


-- ------------------------------------------------------------
-- 2) Listar todos os atendimentos de um paciente específico
-- (ordenados por data)
-- ------------------------------------------------------------
-- SELECT puro que retorna todos os atendimentos do paciente
-- informado (troque o valor 1 pelo id_paciente desejado),
-- ordenados da data mais antiga para a mais recente.

SELECT id_atendimento, data_hora, duracao_minutos, id_residente, id_preceptor
FROM ATENDIMENTO
WHERE id_paciente = 1
ORDER BY data_hora ASC;

-- ------------------------------------------------------------
-- 3) Listar os procedimentos realizados em um atendimento
-- (com nome do procedimento, quantidade e tempo real)
-- ------------------------------------------------------------
-- SELECT puro com JOIN entre PROCEDIMENTO_REALIZADO e PROCEDIMENTO
-- para trazer o nome do procedimento (troque o valor 1 pelo
-- id_atendimento desejado).

SELECT p.nome, pr.quantidade, pr.tempo_real_minutos
FROM PROCEDIMENTO_REALIZADO pr
JOIN PROCEDIMENTO p ON p.id_procedimento = pr.id_procedimento
WHERE pr.id_atendimento = 1;

-- ------------------------------------------------------------
-- 4) Atualizar os dados de um paciente
-- (endereço ou convênio)
-- ------------------------------------------------------------
-- UPDATE puro. COALESCE não é exclusivo de PL/pgSQL, funciona
-- normalmente em SQL puro: se um valor não for informado (NULL),
-- mantém o valor atual da coluna. Troque os valores conforme o
-- paciente e o dado que quiser atualizar.

UPDATE PACIENTE
SET endereco     = COALESCE('Rua das Flores, 123 - Campina Grande/PB', endereco),
    num_convenio = COALESCE(num_convenio, num_convenio)
WHERE id_pessoa = 1;

-- ------------------------------------------------------------
-- 5) Remover um procedimento realizado
-- (apenas se ainda não houver faturamento associado)
-- ------------------------------------------------------------
-- DELETE puro com a condição faturado = FALSE direto no WHERE.
-- Se o procedimento já estiver faturado, a condição não bate e
-- 0 linhas são removidas (sem erro, mas também sem apagar dado
-- que não deveria ser apagado).

DELETE FROM PROCEDIMENTO_REALIZADO
WHERE id_atendimento = 6
  AND id_procedimento = 10
  AND faturado = FALSE;

-- ------------------------------------------------------------
-- 6) Calcular o tempo médio de duração dos atendimentos
-- por residente
-- ------------------------------------------------------------
-- SELECT puro com JOIN + GROUP BY, usando a coluna duracao_minutos
-- já existente em ATENDIMENTO. Resultado ordenado do maior para
-- o menor tempo médio.

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
ORDER BY AVG(a.duracao_minutos) DESC;

