
-- ============================================================
-- PROYECTO: SolarDB Pascual
-- ARCHIVO: sql/02_carga.sql
-- DESCRIPCIÓN: Transformación y carga idempotente (Paso 3)
-- ============================================================

INSERT INTO lectura_demo (
    dispositivo_id,
    timestamps,
    p_ac,
    v_ac,
    irradiancia,
    temp_modulo,
    alarma,
    ingresado_en
)
SELECT
    (payload->>'dispositivo_id')::INT,
    (payload->>'timestamps')::TIMESTAMPTZ,
    (payload->>'p_ac')::NUMERIC,
    (payload->>'v_ac')::NUMERIC,
    (payload->>'irradiancia')::NUMERIC,
    (payload->>'temp_modulo')::NUMERIC,
    payload->>'alarma',
    COALESCE(
        (payload->>'ingresado_en')::TIMESTAMPTZ,
        NOW()
    )
FROM stg_lectura_raw
ON CONFLICT (dispositivo_id, timestamps)
DO NOTHING;

