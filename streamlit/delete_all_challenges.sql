-- Script para eliminar todos los desafíos y opciones de respuesta
-- ADVERTENCIA: Esta operación es irreversible. Asegúrate de tener un respaldo.

-- Primero eliminamos las opciones de respuesta (por la relación de clave foránea)
DELETE FROM challenge_options;

-- Luego eliminamos los desafíos
DELETE FROM challenges;

-- Reiniciar las secuencias de IDs para que empiecen desde 1
ALTER SEQUENCE challenge_options_id_seq RESTART WITH 1;
ALTER SEQUENCE challenges_id_seq RESTART WITH 1;

-- Verificar que se eliminaron correctamente
SELECT COUNT(*) as total_challenges FROM challenges;
SELECT COUNT(*) as total_options FROM challenge_options;
