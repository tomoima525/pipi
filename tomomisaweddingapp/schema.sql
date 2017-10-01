CREATE TABLE IF NOT EXISTS images (
  id SERIAL PRIMARY KEY,
  public_id text not null,
  url text not null
);
