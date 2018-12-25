# Saúde em Jogo

### Setting up on Arch:

```
sudo pacman -S python-pip
```

Check pip version:
```
pip -V
```
Should be on python3.*

Install virtualenv as user (non-root)
```
pip3 install virtualenv --user
```
 Check if virtualenv is working
 ```
virtualenv --version
 ```
 If you have any troubles here, add to $PATH `~/.local/bin/` or install virtualenv as `root` (works but it is not recommended)
 
 Create a virtualenv wherever you want, this __`DOES NOT GO TO GIT`__
 ```
virtualenv env
 ```
 Now you can activate your env with
 ```
source env/bin/activate
 ```
 Let's install everything in our venv
 ```
pip install -r requirements.txt
 ```
 Just run!
 ```
python3 manage.py runserver
 ```
 
 ### Setting up PostgreSQL
 
 You can use whatever database you want, really. I'll explain how to use PostgreSQL, since i'm using it right now.
 ```
 sudo pacman -S postgresql
 ```
  ```
 sudo su postgres -l
 ```
  ```
 initdb --locale $LANG -E UTF8 -D '/var/lib/postgres/data/'
 ```
  ```
 exit or ctrl+d
 ```
  ```
 sudo systemctl enable --now postgresql.service
 ```
 ```
 sudo -i -u postgres psql
 ```
 ```
 create database saude_em_jogo;
 ```
 ```
 create user myuser with encrypted password 'mypass';
 ```
 ```
 grant all privileges on database saude_em_jogo to myuser;
 ```
 ```
 ctrl+d until exit all
 ```
 P.S: These are my configs, feel free to do yours