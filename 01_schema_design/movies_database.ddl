CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.person (
  "id" uuid PRIMARY KEY,
  "full_name" TEXT NOT NULL,
  "created" timestamp,
  "modified" timestamp
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
  "id" uuid PRIMARY KEY,
  "person_id" uuid NOT NULL,
  "film_work_id" uuid NOT NULL,
  "role" TEXT NOT NULL,
  "created" timestamp
);

CREATE TABLE IF NOT EXISTS content.film_work (
  "id" uuid PRIMARY KEY,
  "title" TEXT NOT NULL,
  "description" TEXT,
  "creation_date" DATE,
  "rating" FLOAT,
  "type" TEXT NOT NULL,
  "created" timestamp,
  "modified" timestamp
);

CREATE TABLE IF NOT EXISTS content.genre (
  "id" uuid PRIMARY KEY,
  "name" TEXT NOT NULL,
  "description" TEXT,
  "created" timestamp,
  "modified" timestamp
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
  "id" uuid PRIMARY KEY,
  "genre_id" uuid NOT NULL,
  "film_work_id" uuid NOT NULL,
  "created" timestamp
);

ALTER TABLE content.person_film_work ADD FOREIGN KEY (person_id) REFERENCES content.person (id);

ALTER TABLE content.person_film_work ADD FOREIGN KEY (film_work_id) REFERENCES content.film_work (id);

ALTER TABLE content.genre_film_work ADD FOREIGN KEY (film_work_id) REFERENCES content.film_work (id);

ALTER TABLE content.genre_film_work ADD FOREIGN KEY (genre_id) REFERENCES content.genre (id);

CREATE INDEX person_film_work_idx ON content.person_film_work (film_work_id, person_id);

CREATE INDEX genre_film_work_idx ON content.genre_film_work (film_work_id, genre_id);

CREATE INDEX film_work_idx ON content.film_work (id, title, creation_date);

CREATE INDEX person_idx ON content.person (id, full_name);
