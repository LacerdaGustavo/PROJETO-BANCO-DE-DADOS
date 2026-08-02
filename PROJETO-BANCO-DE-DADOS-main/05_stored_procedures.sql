CREATE OR REPLACE PROCEDURE sp_registrar_atendimento_completo(
    p_id_paciente     INT,
    p_id_residente    INT,
    p_id_preceptor    INT,
    p_data_hora       TIMESTAMP,
    p_duracao_minutos INT,
    p_procedimentos   JSONB
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id_atendimento  INT;
    v_item            JSONB;
    v_id_procedimento INT;
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
    VALUES (p_data_hora, p_duracao_minutos, p_id_paciente, p_id_residente, p_id_preceptor)
    RETURNING id_atendimento INTO v_id_atendimento;

    FOR v_item IN SELECT * FROM jsonb_array_elements(p_procedimentos)
    LOOP
        v_id_procedimento := (v_item ->> 'id_procedimento')::INT;

        IF NOT EXISTS (SELECT 1 FROM PROCEDIMENTO WHERE id_procedimento = v_id_procedimento) THEN
            RAISE EXCEPTION 'Procedimento com id % não existe (atendimento revertido)', v_id_procedimento;
        END IF;

        INSERT INTO PROCEDIMENTO_REALIZADO (id_atendimento, id_procedimento, quantidade, tempo_real_minutos, observacao)
        VALUES (
            v_id_atendimento,
            v_id_procedimento,
            COALESCE((v_item ->> 'quantidade')::INT, 1),
            (v_item ->> 'tempo_real_minutos')::INT,
            v_item ->> 'observacao'
        );
    END LOOP;

    RAISE NOTICE 'Atendimento % registrado com sucesso, com % procedimento(s)', v_id_atendimento, jsonb_array_length(p_procedimentos);
END;
$$;
