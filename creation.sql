CREATE SCHEMA IF NOT EXISTS initial;
CREATE SCHEMA IF NOT EXISTS result;

CREATE TABLE IF NOT EXISTS initial.Location (
    id SERIAL PRIMARY KEY,
    location_id VARCHAR(50) UNIQUE NOT NULL,
    location_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE  IF NOT EXISTS initial.Customer (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(50) UNIQUE NOT NULL,
    gender VARCHAR(10) NULL
);

CREATE TABLE  IF NOT EXISTS initial.Facts (
  id SERIAL PRIMARY KEY,
  customer_id VARCHAR(50) NOT NULL,
  location_id VARCHAR(50) NOT NULL,
  date TIMESTAMP NOT NULL,
  quantity FLOAT NOT NULL,
  total_price FLOAT NOT NULL,
  gender VARCHAR(10) NULL,
  unit_price FLOAT NOT NULL AS (total_price / quantity)
);

ALTER TABLE initial.Facts ADD CONSTRAINT FK_Location_id FOREIGN KEY (location_id) REFERENCES initial.Location (location_id);
ALTER TABLE initial.Facts ADD CONSTRAINT FK_Customer_id FOREIGN KEY (customer_id) REFERENCES initial.Customer (customer_id);


SELECT *
    FROM initial.Customer
