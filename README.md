# Le Cacao
Inspired by the lack of LoveCrunch granola, Le Caco provides an easy way to find your favorite chocolate foods. 
## Resources
All attributes are strings unless otherwise noted

**Chocolates:**
* Chocolate ID(integer)
* Name 
* Size 
* Flavor 
* Price 
* Description 
* Rating (integer)

**Users:**
* User ID (integer)
* First Name 
* Last Name 
* Email 
* Encrypted Password 

This functionality is confirmed by Bcrypt. Upon registration of a new email address, inputted passwords are hashed and salted, then saved in the db alongside the other collected information. When logging in using a known email, the newly inputted password is verified with bcrypt, which encrypts & compares the password to the stored password. Login is required to access the main chocolates page.
## SQL Schema

```sql
CREATE TABLE CHOCOLATES(
id INTEGER PRIMARY KEY,
name text,
size text,
flavor text,
price text,
description text,
rating text);

CREATE TABLE USERS(
id INTEGER PRIMARY KEY,
first_name text,
last_name text,
email text,
encrypted_password text
);
```


## REST Endpoints

Name                          | Method | Path
----------------------------- | ------ | --------------------
Retrieve chocolate collection | GET    | /chocolates
Retrieve chocolate member     | GET    | /chocolates/*\<id\>*
Create chocolate member       | POST   | /chocolates
Update chocolate member       | PUT    | /chocolates/*\<id\>*
Delete chocolate member       | DELETE | /chocolates/*\<id\>*
Create new user               | POST   | /users
Login to account              | POST   | /sessions