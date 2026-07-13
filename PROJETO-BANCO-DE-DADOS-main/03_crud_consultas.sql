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
-- Function que recebe o id do atendimento e retorna os
-- procedimentos realizados nele, já com o nome do procedimento
-- (via JOIN com PROCEDIMENTO), a quantidade e o tempo real gasto.

CREATE OR REPLACE FUNCTION listar_procedimentos_atendimento(p_id_atendimento INT)
RETURNS TABLE (
    nome_procedimento    VARCHAR(150),
    quantidade           INT,
    tempo_real_minutos   INT
) AS $$
BEGIN
    -- verifica se o atendimento existe antes de listar
    IF NOT EXISTS (SELECT 1 FROM ATENDIMENTO WHERE id_atendimento = p_id_atendimento) THEN
        RAISE EXCEPTION 'Atendimento com id % não existe', p_id_atendimento;
    END IF;

    RETURN QUERY
    SELECT p.nome, pr.quantidade, pr.tempo_real_minutos
    FROM PROCEDIMENTO_REALIZADO pr
    JOIN PROCEDIMENTO p ON p.id_procedimento = pr.id_procedimento
    WHERE pr.id_atendimento = p_id_atendimento;
END;
$$ LANGUAGE plpgsql;

-- Exemplo de uso: listar procedimentos realizados no atendimento 1
SELECT * FROM listar_procedimentos_atendimento(1);

-- ------------------------------------------------------------
-- 4) Atualizar os dados de um paciente
-- (endereço ou convênio)
-- ------------------------------------------------------------
-- Function que recebe o id do paciente e, opcionalmente, o novo
-- endereço e/ou novo número de convênio. Os parâmetros usam
-- DEFAULT NULL, e o COALESCE garante que, se um parâmetro não
-- for informado, o valor atual no banco é mantido (não é
-- sobrescrito com NULL). Verifica se o paciente existe antes
-- de tentar atualizar.

CREATE OR REPLACE FUNCTION atualizar_dados_paciente(
    p_id_paciente     INT,
    p_endereco        VARCHAR(255) DEFAULT NULL,
    p_num_convenio    VARCHAR(50)  DEFAULT NULL
) RETURNS VOID AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM PACIENTE WHERE id_pessoa = p_id_paciente) THEN
        RAISE EXCEPTION 'Paciente com id % não existe', p_id_paciente;
    END IF;

    UPDATE PACIENTE
    SET endereco     = COALESCE(p_endereco, endereco),
        num_convenio = COALESCE(p_num_convenio, num_convenio)
    WHERE id_pessoa = p_id_paciente;
END;
$$ LANGUAGE plpgsql;

-- Exemplo de uso: atualiza só o endereço do paciente 1
SELECT atualizar_dados_paciente(1, 'Rua das Flores, 123 - Campina Grande/PB');

-- Exemplo de uso: atualiza só o convênio do paciente 3
SELECT atualizar_dados_paciente(3, NULL, 'HAPVIDA-777');

-- ------------------------------------------------------------
-- 5) Remover um procedimento realizado
-- (apenas se ainda não houver faturamento associado)
-- ------------------------------------------------------------
-- Function que recebe o id do atendimento e o id do procedimento
-- (chave composta de PROCEDIMENTO_REALIZADO). Verifica se o
-- registro existe e, em seguida, verifica a flag "faturado".
-- Caso já esteja estiver faturado, a remoção é bloqueada com RAISE
-- EXCEPTION; caso contrário, o registro é removido.

CREATE OR REPLACE FUNCTION remover_procedimento_realizado(
    p_id_atendimento   INT,
    p_id_procedimento  INT
) RETURNS VOID AS $$
DECLARE
    v_faturado BOOLEAN;
BEGIN
    SELECT faturado INTO v_faturado
    FROM PROCEDIMENTO_REALIZADO
    WHERE id_atendimento = p_id_atendimento
      AND id_procedimento = p_id_procedimento;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Procedimento realizado (atendimento %, procedimento %) não existe',
            p_id_atendimento, p_id_procedimento;
    END IF;

    IF v_faturado THEN
        RAISE EXCEPTION 'Não é possível remover: procedimento já faturado';
    END IF;

    DELETE FROM PROCEDIMENTO_REALIZADO
    WHERE id_atendimento = p_id_atendimento
      AND id_procedimento = p_id_procedimento;
END;
$$ LANGUAGE plpgsql;

-- Exemplo de uso válido: remove o procedimento 2 do atendimento 8 (não faturado)
SELECT remover_procedimento_realizado(8, 2);

-- Exemplo de uso inválido: marcar como faturado antes e tentar remover
-- UPDATE PROCEDIMENTO_REALIZADO SET faturado = TRUE WHERE id_atendimento = 1 AND id_procedimento = 1;
-- SELECT remover_procedimento_realizado(1, 1);

-- ------------------------------------------------------------
-- 6) Calcular o tempo médio de duração dos atendimentos
-- por residente
-- ------------------------------------------------------------
-- Function que retorna, para cada residente, o nome, a
-- quantidade de atendimentos realizados e o tempo médio de
-- duração (em minutos), usando a coluna duracao_minutos já
-- existente em ATENDIMENTO. o resultado está ordenado do maior 
-- para o menor tempo médio.
-- Observação: o ORDER BY usa a expressão AVG(a.duracao_minutos)
-- diretamente, e não o nome da coluna de saída
-- (tempo_medio_minutos), pois em funções com RETURNS TABLE o
-- Postgres cria uma variável interna com o mesmo nome da coluna,
-- o que torna a ordenação por nome ambígua e faz o ORDER BY
-- não funcionar como esperado.

CREATE OR REPLACE FUNCTION tempo_medio_atendimento_por_residente()
RETURNS TABLE (
    id_residente        INT,
    nome_residente       VARCHAR(150),
    qtd_atendimentos     BIGINT,
    tempo_medio_minutos  NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        r.id_profissional,
        pe.nome,
        COUNT(a.id_atendimento),
        ROUND(AVG(a.duracao_minutos), 2)
    FROM RESIDENTE r
    JOIN PROFISSIONAL pr ON pr.id_pessoa = r.id_profissional
    JOIN PESSOA pe ON pe.id_pessoa = pr.id_pessoa
    JOIN ATENDIMENTO a ON a.id_residente = r.id_profissional
    GROUP BY r.id_profissional, pe.nome
    ORDER BY AVG(a.duracao_minutos) DESC;
END;
$$ LANGUAGE plpgsql;

-- Exemplo de uso: tempo médio de duração por residente
SELECT * FROM tempo_medio_atendimento_por_residente();
