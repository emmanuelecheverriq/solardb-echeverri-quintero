```sql
-- 1. Crear el rol de solo lectura con contraseña
CREATE ROLE solar_lector
WITH LOGIN PASSWORD 'lector123';

-- 2. Otorgar permiso de conexión a la base de datos
GRANT CONNECT ON DATABASE solardb
TO solar_lector;

-- 3. Otorgar permiso de uso del esquema público
GRANT USAGE ON SCHEMA public
TO solar_lector;

-- 4. Otorgar únicamente permiso SELECT sobre la tabla lectura_demo
GRANT SELECT ON TABLE lectura_demo
TO solar_lector;

-- 5. Revocar permisos de modificación explícitamente
-- Principio de Mínimo Privilegio
REVOKE INSERT, UPDATE, DELETE
ON TABLE lectura_demo
FROM solar_lector;
```
