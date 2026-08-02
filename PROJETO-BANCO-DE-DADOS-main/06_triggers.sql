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

-- Exemplo de uso inválido: residente 6 já está em Sábado/Noite na
-- unidade 1 (dado de teste original). Tentar escalar ele no mesmo
-- Sábado/Noite em OUTRA unidade (ex: 2) deve disparar o erro.
-- INSERT INTO ESCALA (id_unidade, dia_semana, turno, id_residente, id_preceptor, data_plantao)
-- VALUES (2, 'Sábado', 'Noite', 6, 12, '2026-07-18');
