CREATE TABLE data (
  id SERIAL PRIMARY KEY,
  location TEXT NOT NULL,
  latitude REAL NOT NULL,
  longitude REAL NOT NULL,
  created TIMESTAMP NOT NULL,
  nickname TEXT
);