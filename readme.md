## Project setup
```
To run locally:

pip install telethon
pip install peewee
pip install PyJWT
pip install flask
pip install psycopg2
pip install -U flask-cors

To deploy:
install docker, docker-compose
create a directory
git clone https://github.com/gerladeno/telega.git
add config.ini to ./config/
run "python config.py" to estabilish connection (you'll have to enter your phone and code, and config.ini should include your password if you have 2-step verification)
run "docker-compose up -d --build"
check, that all 3 containers run "docker ps"
```
