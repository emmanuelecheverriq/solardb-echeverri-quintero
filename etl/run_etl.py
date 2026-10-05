import json
from datetime import datetime

import psycopg2


# 1. Configuración de conexión DB
DB_CONFIG = {
    "dbname": "solardb",
    "user": "postgres",
    "password": "3138", 
    "host": "localhost",
    "port": "5432",
}


def ejecutar_etl():
    inicio = datetime.now()

    print("🚀 [1/4] Iniciando Pipeline ETL en SolarDB...")

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # --- PASO A: REGISTRAR INICIO EN BITÁCORA ---
        cur.execute(
            "INSERT INTO etl_log (proceso, inicio, estado) "
            "VALUES (%s, %s, %s) "
            "RETURNING id;",
            ("Ingesta_JSONL_Solar", inicio, "EN_PROCESO"),
        )

        log_id = cur.fetchone()[0]
        conn.commit()

        # --- PASO B: CARGAR JSONL A STAGING (stg_lectura_raw) ---
        ruta_jsonl = "data/lecturas.jsonl"
        filas_leidas = 0

        print(
            "📄 [2/4] Leyendo 'data/lecturas.jsonl' "
            "e insertando en staging..."
        )

        with open(ruta_jsonl, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    payload = json.loads(line)

                    cur.execute(
                        "INSERT INTO stg_lectura_raw (payload) "
                        "VALUES (%s);",
                        (json.dumps(payload),),
                    )

                    filas_leidas += 1

        conn.commit()

        print(
            f" ↳ Se insertaron {filas_leidas} objetos JSON "
            "en 'stg_lectura_raw'."
        )

        # --- PASO C: TRANSFORMACIÓN Y CARGA IDEMPOTENTE (lectura_demo) ---
        print(
            "🔄 [3/4] Transformando datos JSONB e insertando "
            "en 'lectura_demo'..."
        )

        sql_transformacion = """
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
                COALESCE((payload->>'ingresado_en')::TIMESTAMPTZ, NOW())
            FROM stg_lectura_raw
            ON CONFLICT (dispositivo_id, timestamps)
            DO NOTHING;
        """

        cur.execute(sql_transformacion)

        filas_cargadas = cur.rowcount  # Conteo de filas realmente insertadas

        conn.commit()

        print(
            f" ↳ Se cargaron {filas_cargadas} filas transformadas "
            "en 'lectura_demo'."
        )

        # --- PASO D: REGISTRAR FIN EXITOSO EN BITÁCORA ---
        fin = datetime.now()

        cur.execute(
            """
            UPDATE etl_log
            SET
                fin = %s,
                filas_leidas = %s,
                filas_cargadas = %s,
                estado = 'EXITOSO'
            WHERE id = %s;
            """,
            (fin, filas_leidas, filas_cargadas, log_id),
        )

        conn.commit()

        print(
            "✅ [4/4] ¡ETL finalizado con éxito y bitácora "
            "'etl_log' actualizada!"
        )

        cur.close()
        conn.close()

    except Exception as e:
        print(f"❌ ERROR durante la ejecución del ETL: {e}")


if __name__ == "__main__":
    ejecutar_etl()
