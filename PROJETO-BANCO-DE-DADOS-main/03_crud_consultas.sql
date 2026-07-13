-- ------------------------------------------------------------
-- 1) Inserir um novo atendimento
-- (verificando se paciente, residente e preceptor existem)
-- ------------------------------------------------------------
-- Stored Procedure/Function que recebe os dados do atendimento 
-- como parâmetros, verifica se paciente, residente e preceptor 
-- existem e, e caso existam, insere o atendimento e retorna 
-- o id gerado. Caso algum não exista, a função interrompe a 
-- execução com RAISE EXCEPTION e nada é inserido.
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION inserir_atendimento(
    p_id_paciente   INT,
    p_id_residente  INT,
    p_id_preceptor  INT,
    p_data_hora     TIMESTAMP,
    p_duracao       INT
) RETURNS INT AS $$
DECLARE
    v_id_atendimento INT;
BEGIN
    IF NOT EXISTS (SELECT 1 FROM PACIENTE WHERE id_pessoa = p_id_paciente) THEN
        RAISE EXCEPTION 'Paciente com id % não existe', p_id_paciente;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM RESIDENTE WHERE id_profissional = p_id_residente) THEN
        RAISE EXCEPTION 'Residente com id % não existe', p_id_residente;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM PRECEPTOR WHERE id_profissional = p_id_preceptor) THEN
        RAISE EXCEPTION 'Preceptor com id % não existe', p_id_preceptor;
    END IF;

    INSERT INTO ATENDIMENTO (data_hora, duracao_minutos, id_paciente, id_residente, id_preceptor)
    VALUES (p_data_hora, p_duracao, p_id_paciente, p_id_residente, p_id_preceptor)
    RETURNING id_atendimento INTO v_id_atendimento;

    RETURN v_id_atendimento;
END;
$$ LANGUAGE plpgsql;

-- Exemplo de uso válido: insere atendimento e mostra o id gerado
SELECT inserir_atendimento(1, 6, 11, '2026-07-14 08:00:00', 30);

-- Exemplo de uso inválido: paciente 999 não existe, deve gerar erro
-- SELECT inserir_atendimento(999, 6, 11, '2026-07-14 08:00:00', 30);


-- ------------------------------------------------------------
-- 2) Listar todos os atendimentos de um paciente específico
-- (ordenados por data)
-- ------------------------------------------------------------
-- Function que recebe o id do paciente e retorna todos os
-- atendimentos dele, do mais antigo para o mais recente de
-- forma ordenada (data_hora ASC).

CREATE OR REPLACE FUNCTION listar_atendimentos_paciente(p_id_paciente INT)
RETURNS TABLE (
    id_atendimento   INT,
    data_hora        TIMESTAMP,
    duracao_minutos  INT,
    id_residente     INT,
    id_preceptor     INT
) AS $$
BEGIN
    -- verifica se o paciente existe antes de listar
    IF NOT EXISTS (SELECT 1 FROM PACIENTE WHERE id_pessoa = p_id_paciente) THEN
        RAISE EXCEPTION 'Paciente com id % não existe', p_id_paciente;
    END IF;

    RETURN QUERY
    SELECT a.id_atendimento, a.data_hora, a.duracao_minutos, a.id_residente, a.id_preceptor
    FROM ATENDIMENTO a
    WHERE a.id_paciente = p_id_paciente
    ORDER BY a.data_hora ASC;
END;
$$ LANGUAGE plpgsql;

-- Exemplo de uso: listar atendimentos do paciente 1
SELECT * FROM listar_atendimentos_paciente(1);


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
