
CREATE TABLE CHOCOLATES(
id INTEGER PRIMARY KEY,
name text,
size text,
flavor text,
price text,
description text,
rating INTEGER);

CREATE TABLE USERS(
id INTEGER PRIMARY KEY,
first_name text,
last_name text,
email text,
encrypted_password text
);
