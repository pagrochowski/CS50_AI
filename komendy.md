# My Useful Commands

## Docker Commands

### Single service container
- `docker build -t kontener .` Build docker container image
- `docker run -v ${pwd}:/usr/src/app -p 8000:8000 kontener` Execute container with directory mounted as in docker-compose

### Multi service container
- `docker-compose build web` Create compose image
- `docker-compose up` Start services

- `docker exec -it CONTAINER_ID bash -l` Enter CLI of the CONTAINER_ID container
- `docker build -t my_image .` (Build a Docker image)
- `docker run -p 8000:8000 my_image` (Run the image and expose port 8000)
- `docker ps` (List running containers)

## Git Commands
- `apt-get install git` install git
- `git init` Initialise .git folder
- `git remote add origin https://github.com/pagrochowski/CS50_SQL.git` Connect to GitHub repository
- `git remote -v` check your current remote repository
- `git pull -u origin master` Pull code files from origin repository, branch "master"
- `git fetch --all && git reset --hard origin/main` Hard pull and reset to current "main" branch

- .gitignore
    `git add .gitignore`
    `git commit -m "Add .gitignore file"`
    `git push`

- initialise new repository with SSH access after fresh installation
    `mkdir ~/.ssh` create ssh folder
    `chmod 700 ~/.ssh` grant access to the ssh folder
    `ssh-keygen -t rsa -b 4096 -C "pagrochowski@gmail.com"` create ssh key
    `eval "$(ssh-agent -s)"` check the ssh agent is online and working
    `ssh-add ~/.ssh/id_rsa` add identity to the ssh file
    `cat ~/.ssh/id_rsa.pub` read the ssh public key, add it to github account -> settings -> ssh
    `ssh -T git@github.com` verify connection
    `git config --global user.email "pagrochowski@gmail.com"`
    `git config --global user.name "pagrochowski"`

- manually push the files to repository
    - `git add .` (Stage all changes)
    - `git commit -m "Your commit message"` (Commit changes)
    - `git push origin master` (Push to the 'master' branch on the 'origin' remote)

## Python Commands
- `pip freeze > requirements.txt` (Save dependencies to a file)
- `python -m venv myenv` (Create a virtual environment)
- `source venv/bin/activate` or `deactivate` Virtual Environment

## Django Commands
- `python manage.py runserver` Starts Django server
- `python manage.py makemigrations` prepares database migration from models
- `python manage.py migrate` migrates models changes
- `python manage.py collectstatic` collects static files
- `python manage.py test` to run the Django tests

## Nginx Commands
- `sudo systemctl reload nginx` reload nginx 
- `sudo systemctl restart nginx` restart nginx 
- `sudo nano /etc/nginx/sites-available/project_portfolio` edit config file
- `sudo nginx -t` test syntax

## Gunicorn Commands
- `sudo systemctl restart gunicorn` Restart Gunicorn to reload server files
- check status `sudo systemctl status gunicorn.socket`
- `sudo systemctl reset-failed gunicorn.socket` reset failed restart

## SSH console editor
- `CTRL+O` save file, `ENTER` to confirm changes
- `CTRL+X` exit file
- `CTRL+K` delete row in editor
- `ALT+M` for mouse support
- `sudo su -` gain access as root user

## Ollama
`ollama serve` is starting the service on Linux
`ollama run ...` and choose a model to run/download

## SQLITE3
`.headers on` display headers in SQLITE3
`.timer on` display timer details for each query
`.read schema.sql` to import table creation from the schema file or commands from other sql file
`cat file.sql | sqlite3 database.db` execute file.sql commands into database.db
`.schema` check t he current schema for the tables

## MySQL (CS50_SQL dependant)
In the folder with docker-compose.yml:
`docker-compose up` starts mysql server
`docker-compose run --service-ports python-app bash` starts python bash command line
`mariadb -h mysql -u root -p` opens connection to mysql database
password: crimson
