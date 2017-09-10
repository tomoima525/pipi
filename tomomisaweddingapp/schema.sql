drop table if exists images;
create table images (
  id integer primary key autoincrement,
  public_id text not null,
  url text not null
);
