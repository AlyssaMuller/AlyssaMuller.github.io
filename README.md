# Le Cacao

## Resource

**Chocolates**

Attributes:
* Name (string)
* Size (string)
* Flavor (string)
* Price (string)
* Description (string)
* Rating (string)

## Schema

```sql
CREATE TABLE CHOCOLATES(
id INTEGER PRIMARY KEY,
name text,
size text,
flavor text,
price text,
description text,
rating text);
```

## REST Endpoints

Name                          | Method | Path
----------------------------- | ------ | --------------------
Retrieve chocolate collection | GET    | /chocolates
Retrieve chocolate member     | GET    | /chocolates/*\<id\>*
Create chocolate member       | POST   | /chocolates
Update chocolate member       | PUT    | /chocolates/*\<id\>*
Delete chocolate member       | DELETE | /chocolates/*\<id\>*