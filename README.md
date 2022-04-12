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

This functionality is confirmed by Bcrypt. The inputted passwords are hashed and salted, then saved in the db. Upon login, the newly inputted password is hashed and salted the same way, then compare to the stored password if the email exists.   
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
Create new user               | POST   | /users/*\<id\>*
Retrieve user                 | GET    | /users/*\<id\>*
Login to account              | POST   | /sessions/*\<id\>*