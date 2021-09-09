#Initialization of the development environment 

##Requirements
- Python 3.8
- pip 3.8
- PostgreSQl >=9.6
- git

##Database setup
1. Switch user to postgres<br/>
    _sudo su – postgres_<br/><br/>
2. Log into a Postgres session<br/>
    _psql_<br/><br/>
3. Create a database<br/>
    _CREATE DATABASE finlive_db;_<br/><br/>
4. Create a user named finlive<br/>
   _CREATE USER finlive WITH PASSWORD 'password';_<br/><br/>
5. Modify connection parameters for the new database user<br/>
   _ALTER ROLE finlive SET client_encoding TO 'utf8';_<br/>
   _ALTER ROLE finlive SET default_transaction_isolation TO 'read committed';_<br/>
   _ALTER ROLE finlive SET timezone TO 'UTC';_<br/><br/><br/>
6. Grant permissions to the user<br/>
    _GRANT ALL PRIVILEGES ON DATABASE finlive_db TO finlive;_<br/><br/>
7. Exit to your normal user's session<br/>
   _\q_<br/>
   _exit_<br/>

##Django project setup
1. Navigate to the directory where you want the project codes<br/>
    e.g. _cd /home/user/work_<br/><br/>
2. Copy project from the repository<br/>
    git clone https://github.com/FinLiveRI/FinLiveApp.git finlive<br/><br/>
3. Navigate to the project folder<br/>
   _cd finlive_<br/><br/>
4. Optional. Activate the virtual environment if you are using the isolated Python environment<br/>
    e.g. _source /home/user/work/venv/bin/activate_<br/><br/>
5. Install the project dependencies<br/>
   _pip install -r requirements.txt_<br/><br/>
6. Create a new .env file for the non-public settings. The SECRET_KEY is for development purposes only. You can also create a new key with get_random_secret_key() function. <br/>
   _nano finliveapp/settings/.env<br/><br/>_
   Add follow content to the file:<br/>
   SECRET_KEY=f_2+o&tsxefa9i7))%*f&yc$gr-cs0j*15)u89vnavrsrni2!y<br/>
   DEBUG=True<br/>
   DB_NAME=’finlive_db’<br/>
   DB_USER=’finlive’<br/>
   DB_PASS=’previously created db user password here’<br/>
   DB_HOST=’localhost’<br/>
   DB_PORT=’’<br/><br/>
7. Initialize the database<br/>
   python manage.py migrate<br/><br/>
8. Create an administrative account<br/>
   python manage.py createsuperuser<br/><br/>
9. Start up the development server<br/>
   python manage.py runserver<br/><br/>
10. In your web browser, open admin login screen and login with the superuser username and password<br/>
   http://127.0.0.1:8000/admin <br/><br/>
11. With the admin interface you can create new user accounts used in development
    
    