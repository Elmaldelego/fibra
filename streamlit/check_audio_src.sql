-- Verificar si hay desafíos con audio_src
SELECT 
    id,
    lesson_id,
    type,
    question,
    audio_src
FROM challenges
WHERE audio_src IS NOT NULL AND audio_src != ''
ORDER BY id;

-- Contar cuántos desafíos tienen audio
SELECT COUNT(*) as total_with_audio
FROM challenges
WHERE audio_src IS NOT NULL AND audio_src != '';

-- Ver todos los desafíos de la lección 13 (primera lección)
SELECT 
    id,
    lesson_id,
    type,
    question,
    audio_src
FROM challenges
WHERE lesson_id = 13
ORDER BY "order";
