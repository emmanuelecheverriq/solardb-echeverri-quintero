SolarDB Pascual - Pipeline de Ingesta ETL y Gobernanza de Datos

An idempotent ETL pipeline that loads simulated IoT telemetry into a governed PostgreSQL repository, versioned on GitHub.

📌 Información General
Curso: Bases de Datos I (SD1006)
Grupo: 811
Semestre: 2026-II
Institución: Institución Universitaria Pascual Bravo
Integrantes:
Integrante 1: Emmanuel Echeverri Quintero

🛠️ Descripción del Trabajo

Este proyecto implementa la ingesta de telemetría simulada IoT para la planta solar SolarDB Pascual.

El desarrollo abarca un flujo ETL idempotente en PostgreSQL, la definición de reglas de gobernanza y control de accesos por roles, y la gestión del código mediante versionado en GitHub.

📁 Estructura del Repositorio

solardb-echeverri-quintero/
├── README.md
├── .gitignore
├── docs/                   # Informe PDF central
├── data/                   # Muestra de datos: lecturas.jsonl
├── etl/                    # Scripts Python: simulador.py y run_etl.py
└── sql/                    # Scripts SQL: 01_tablas.sql, 02_carga.sql y 03_roles.sql