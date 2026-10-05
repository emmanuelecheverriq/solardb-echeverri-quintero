
-- ============================================================
-- PROYECTO: SolarDB Pascual
-- ARCHIVO: sql/01_tablas.sql
-- DESCRIPCIÓN: Definición DDL de Staging, Modelo y Bitácora
-- ============================================================

-- 1. Capa de Staging (Almacenamiento crudo JSONB)
CREATE TABLE IF NOT EXISTS stg_lectura_raw (
    id BIGSERIAL PRIMARY KEY,
    payload JSONB NOT NULL,
    cargado_en TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Tabla Relacional Destino (Lecturas procesadas)
CREATE TABLE IF NOT EXISTS lectura_demo (
    dispositivo_id INT NOT NULL,
    timestamps TIMESTAMPTZ NOT NULL,
    p_ac NUMERIC(10,3) CHECK (p_ac >= 0),
    v_ac NUMERIC(5,1),
    irradiancia NUMERIC(8,1) CHECK (irradiancia BETWEEN 0 AND 1500),
    temp_modulo NUMERIC(5,1),
    alarma VARCHAR(50),
    ingresado_en TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (dispositivo_id, ts)
);

-- 3. Tabla de Bitácora de Auditoría
CREATE TABLE IF NOT EXISTS etl_log (
    id SERIAL PRIMARY KEY,
    proceso VARCHAR(100) NOT NULL,
    inicio TIMESTAMPTZ NOT NULL,
    fin TIMESTAMPTZ,
    filas_leidas INT DEFAULT 0,
    filas_cargadas INT DEFAULT 0,
    estado VARCHAR(20) DEFAULT 'EN_PROCESO'
);

