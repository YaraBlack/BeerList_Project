# BeerList
GUI program that shows a list of beers with columns: name, ingridients, % of alchohol, user's derscription and points.

## For this program to work properly you have to have follow next steps:
1. Create a file `config.json` with "BD_USER" and "BD_PASSWORD" name-value pairs. Example:
```config.json
{
  "BD_USER": "postgres"
  "BD_PASSWORD": "postgres"
}
```
2. Also, you have to create in your DBMS (I used PostgreSQL) new DB called 'users_db'.
3. Inside 'users_db' create a table with the following columns:
  - id - integer PRIMARY KEY NOT NULL
  - username - VARCHAR(20) NOT NULL
  - password_hash - VARCHAR(20) NOT NULL
4. Create a venv using `py venv venv` and activate it.
5. Open a terminal in the project directory and run `pip install -r requirements.txt`
6. Run a backend using `py backend.py`
7. Open a new terminal and enter `py beerGUI.pyw`
8. Create a user

If you wish to use another DBMS - change the URL in row 10 in the `backend.py`.

# This program isn't finished yet.
The program is currently under development.

TBD:
- add bcrypt library to hash passwords;
- add JWT for the authorization process;
- add logging;
- update search algorithm;
- add detailed README.


