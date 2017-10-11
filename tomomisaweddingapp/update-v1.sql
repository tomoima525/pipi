-- add timestamp
ALTER TABLE images ADD COLUMN ts timestamp NOT NULL DEFAULT now();
