CREATE TABLE IF NOT EXISTS images (
  id SERIAL PRIMARY KEY,
  public_id text NOT NULL,
  url text NOT NULL,
  ts timestamp NOT NULL DEFAULT now()
);
