-- ============================================================
-- ETAPA 2 - ITEM 2: TRIGGERS
-- ============================================================

-- ------------------------------------------------------------
-- trg_check_sobreposicao_escala
-- ------------------------------------------------------------
CREATE OR REPLACE FUNCTION fn_check_sobreposicao_escala()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM ESCALA
        WHERE id_residente = NEW.id_residente
          AND dia_semana = NEW.dia_semana
          AND turno = NEW.turno
          AND id_unidade <> NEW.id_unidade
          AND id_escala <> COALESCE(NEW.id_escala, -1)
    ) THEN
        RAISE EXCEPTION 'Residente % já está escalado em outra unidade no dia % turno % (sobreposição de escala)',
            NEW.id_residente, NEW.dia_semana, NEW.turno;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_sobreposicao_escala
BEFORE INSERT OR UPDATE ON ESCALA
FOR EACH ROW
EXECUTE FUNCTION fn_check_sobreposicao_escala();

-- Exemplo de uso válido: nova escala pro residente 9, dia/turno livres
INSERT INTO ESCALA (id_unidade, dia_semana, turno, id_residente, id_preceptor, data_plantao)
VALUES (2, 'Sexta', 'Manhã', 9, 14, '2026-07-17');

-- ------------------------------------------------------------
-- trg_audita_atendimento
-- ------------------------------------------------------------
-- Tabela de auditoria: registra toda inserção, atualização ou
-- remoção feita em ATENDIMENTO, guardando o estado antes/depois
-- em JSON e quem fez a operação.
--
-- Sobre a coluna "usuario": o valor é capturado a partir de uma
-- variável de sessão do PostgreSQL (app.usuario_atual), definida
-- via SET antes de cada operação, simulando "quem" está agindo.
-- Se essa variável não for definida, o valor cai para 'sistema'
-- por padrão, usando COALESCE + current_setting(..., true).

CREATE TABLE IF NOT EXISTS AUDITORIA_ATENDIMENTO (
    id_auditoria    SERIAL PRIMARY KEY,
    id_atendimento  INT NOT NULL,
    operacao        VARCHAR(10) NOT NULL CHECK (operacao IN ('INSERT', 'UPDATE', 'DELETE')),
    usuario         VARCHAR(100) NOT NULL,
    data_hora       TIMESTAMP NOT NULL DEFAULT NOW(),
    dados_antigos   JSONB,
    dados_novos     JSONB
);

CREATE OR REPLACE FUNCTION fn_audita_atendimento()
RETURNS TRIGGER AS $$
DECLARE
    v_usuario VARCHAR(100);
BEGIN
    v_usuario := COALESCE(current_setting('app.usuario_atual', true), 'sistema');

    IF TG_OP = 'INSERT' THEN
        INSERT INTO AUDITORIA_ATENDIMENTO (id_atendimento, operacao, usuario, dados_antigos, dados_novos)
        VALUES (NEW.id_atendimento, 'INSERT', v_usuario, NULL, to_jsonb(NEW));
        RETURN NEW;

    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO AUDITORIA_ATENDIMENTO (id_atendimento, operacao, usuario, dados_antigos, dados_novos)
        VALUES (NEW.id_atendimento, 'UPDATE', v_usuario, to_jsonb(OLD), to_jsonb(NEW));
        RETURN NEW;

    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO AUDITORIA_ATENDIMENTO (id_atendimento, operacao, usuario, dados_antigos, dados_novos)
        VALUES (OLD.id_atendimento, 'DELETE', v_usuario, to_jsonb(OLD), NULL);
        RETURN OLD;
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_audita_atendimento
AFTER INSERT OR UPDATE OR DELETE ON ATENDIMENTO
FOR EACH ROW
EXECUTE FUNCTION fn_audita_atendimento();

-- ------------------------------------------------------------
-- trg_atualiza_media_procedimentos
-- ------------------------------------------------------------
-- AFTER INSERT em PROCEDIMENTO_REALIZADO. Toda vez que um novo
-- procedimento realizado é registrado, recalcula a média de
-- tempo_real_minutos daquele procedimento (considerando todas
-- as vezes que ele já foi realizado) e atualiza a coluna
-- media_tempo_procedimento em PROCEDIMENTO.

CREATE OR REPLACE FUNCTION fn_atualiza_media_procedimentos()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE PROCEDIMENTO
    SET media_tempo_procedimento = (
        SELECT ROUND(AVG(tempo_real_minutos), 2)
        FROM PROCEDIMENTO_REALIZADO
        WHERE id_procedimento = NEW.id_procedimento
    )
    WHERE id_procedimento = NEW.id_procedimento;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_atualiza_media_procedimentos
AFTER INSERT ON PROCEDIMENTO_REALIZADO
FOR EACH ROW
EXECUTE FUNCTION fn_atualiza_media_procedimentos();
