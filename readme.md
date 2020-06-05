## Project setup
```
To run locally:
pip install -r requirements.txt

or

pip install telethon
pip install peewee
pip install PyJWT
pip install flask
pip install psycopg2
pip install -U flask-cors
add config.ini to ./config/ (check config.py to see it's structure, ALL FIELDS ARE MANDATORY)
config.ini must contain
[DB]
host = localhost

To deploy:
install docker, docker-compose
create a directory
git clone https://github.com/gerladeno/telega.git
add config.ini to ./config/ (check config.py to see it's structure, ALL FIELDS ARE MANDATORY)
for docker-compose to work make sure you have
[DB]
host = db
in your config.ini
run "python config.py" to estabilish connection (you'll have to enter your phone and code, and config.ini should include your password if you have 2-step verification)
run "docker-compose up -d --build"
check, that all 3 containers are up: run "docker ps"
```
