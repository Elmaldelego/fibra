-- Migration: Add audio_src column to challenges table
-- This fixes the error: column units_lessons_challenges.audio_src does not exist

-- Add audio_src column to challenges table if it doesn't exist
ALTER TABLE challenges 
ADD COLUMN IF NOT EXISTS audio_src TEXT;

-- Verify the column was added
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'challenges' 
AND column_name = 'audio_src';
