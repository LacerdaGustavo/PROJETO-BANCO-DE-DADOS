DROP VIEW IF EXISTS vw_pacientes_internados;
DROP VIEW IF EXISTS vw_residentes_sem_supervisor;
DROP VIEW IF EXISTS vw_estatisticas_atendimentos_mensal;


CREATE OR REPLACE VIEW vw_residentes_sem_supervisor AS

SELECT
    r.id_profissional,
    pr.nome AS residente,
    pp.nome AS preceptor,
    p.titulacao,
    e.id_unidade,
    e.dia_semana,
    e.turno

FROM escala e

JOIN residente r
ON e.id_residente = r.id_profissional

JOIN pessoa pr
ON r.id_profissional = pr.id_pessoa

JOIN preceptor p
ON e.id_preceptor = p.id_profissional

JOIN profissional prof
ON p.id_profissional = prof.id_pessoa

JOIN pessoa pp
ON prof.id_pessoa = pp.id_pessoa

WHERE p.titulacao <> 'Doutor';






CREATE OR REPLACE VIEW vw_estatisticas_atendimentos_mensal AS
SELECT
    DATE_TRUNC('month', a.data_hora)::DATE AS mes,
    u.id_unidade,
    u.nome AS unidade,

    COUNT(DISTINCT a.id_atendimento) AS total_atendimentos,

    ROUND(AVG(a.duracao_minutos), 2) AS media_duracao_minutos,

    STRING_AGG(
        DISTINCT p.nome,
        ', '
        ORDER BY p.nome
    ) AS procedimentos_mais_comuns

FROM ATENDIMENTO a

JOIN UNIDADE u
    ON a.id_unidade = u.id_unidade

LEFT JOIN PROCEDIMENTO_REALIZADO pr
    ON a.id_atendimento = pr.id_atendimento

LEFT JOIN PROCEDIMENTO p
    ON pr.id_procedimento = p.id_procedimento

GROUP BY
    DATE_TRUNC('month', a.data_hora),
    u.id_unidade,
    u.nome

ORDER BY
    mes,
    unidade;