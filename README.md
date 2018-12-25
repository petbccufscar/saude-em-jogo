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