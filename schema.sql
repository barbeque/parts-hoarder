drop table if exists users;
create table users (
  username text primary key not null,
  password text not null
);
drop table if exists parts;
create table parts (
  id      int primary key,
  name    text not null
);
