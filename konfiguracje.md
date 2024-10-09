# Moje konfiguracje

## Ollama

## Gmail CTL
Quickstart tutorial:
https://mailtrap.io/blog/send-emails-with-gmail-api/

to add "piotr.adrian.grochowski@gmail.com", you have to add "pagrochowski" first, then edit project and add piotr.adrian, then remove pagrochowski

`go install github.com/mbrt/gmailctl/cmd/gmailctl@latest` command line for gmail accounts
`gmailctl init`
https://github.com/mbrt/gmailctl


## Ollama
1. Download Ollama
https://ollama.com/download

Currently installed on my pc:
https://ollama.com/library/llama2

2. Launch the model locally
CLI
Open the terminal and run ollama run llama2

3. Add API configuration to the Python script
API
Example using curl:

curl -X POST http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt":"Why is the sky blue?"
 }'


## GO.mod installation
`curl -fsSL -o go.tar.gz https://golang.org/dl/go1.19.1.linux-amd64.tar.gz` download the package
`tar -C /usr/local -xzf go.tar.gz` move the go to another folder
`export PATH="/usr/local/go/bin:$PATH"`
`export GOPATH="/go"`
`export GOBIN="/usr/local/go/bin"` set paths to GO
`go version` verify installation

## AWS EC2 instance
https://www.youtube.com/watch?v=PzSUOyshA6k&ab_channel=LegionScript
1. Create new account
2. Launch instance
3. Choose preferred Amazaon Machine Image (AMI): Ubuntu?
4. Instance type: t2.micro or t3.micro (free tier enabled)
5. Create key pair for logging with SSH later on. Place the key pair in a safe place.  
6. Network settings
   Add security group for HTTP, HTTPS, SSH and Django at 8000, source: 0.0.0.0/0 for all
   You can change SSH to My IP for security later on.
7. Launch instance
8. Network & Security -> Elastic IPs
   Allocate Elastic IP to the instance, so the IP does not change if instance is restarted.
9. Associate Elastic IP with your instance (menu under Actions button)/
10. Open PowerShell with Admin rights and cd into the location of PEM key file. 
11. Go to the instance and find "Connect". Connect via "Connect to instance" or SSH using key pair
12. Apply permissions to the key pair file. Run this command
   `icacls "path\to\your\project_portfolio.pem" /inheritance:r /grant:r "%username%:(R)"`
   or more specific example, replace username with actual username SID
   `whoami /user`
    `icacls "project_portfolio.pem" /inheritance:r /grant:r "desktop-tjn4e2m\tragik magik:(R)"`
    ssh -i "project_portfolio.pem" ubuntu@3.10.240.43
    Debug flag command -v
    `ssh -v -i "project_portfolio.pem" ubuntu@3.10.240.43`
    *Even after command was successfull, I had to manually go to file properties and remove all other users (other than pagrochowski) from acces. 
    File properties -> Security -> Advanced. Remove all other users and disable inheritance. Only owner with Read allowed should be there.
    This somehow finally worked, after multiple instance restarts. 
9. Run these commands:
   `sudo ufw app list`, `sudo ufw enable`, `y`, `sudo ufw allow ssh`, `sudo ufw status`, `sudo ufw allow 443`:
   Status: active

    To                         Action      From
    --                         ------      ----
    22/tcp                     ALLOW       Anywhere                  
    22/tcp (v6)                ALLOW       Anywhere (v6)   

   `sudo apt update`, `sudo apt install python3-venv python3-dev libpq-dev postgresql-contrib nginx curl virtualenv`
10. If you need Postgres SQL, run `sudo -u posgres psql`, the commands for:
    CREATE DATABASE djangoblo; CREATE USER admin WITH PASSWORD 'password'; ALTER ROLE admin SET client_encoding TO 'utf8';
11. Clone Github repository
    `git clone https://github.com/pagrochowski/project_portfolio`
    `rm -rf` to delete a folder
12. CD into the project folder and setup virtual environment
    `virtualenv venv`
    activate venv `source venv/bin/activate` or `deactivate`
13. Install dependencies
    `pip install django gunicorn` + `psycopg2` if using postgres
14. Add the public IP address, localhost and domain name in ALLOWED_HOSTS in settings.py. Otherwise gets Host not allowed error.
    `ALLOWED_HOSTS = ['3.10.240.43', 'localhost', '127.0.0.1', 'autogen.uk', 'www.autogen.uk', 'autogen.uk.to', 'www.autogen.uk.to']`
15. Double check static and media roots in settings.py:
    STATIC_URL = "static/"
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'core/static'),
    ]

    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Define the directory where uploaded files will be stored
    MEDIA_URL = '/media/'                     # URL prefix for serving media files
16. Create superuser (if needed)
    `python manage.py createsuperuser`
17. Collect static
    `python manage.py collectstatic`
18. Open up the ports and runserver
    `sudo ufw allow 8000`, `python manage.py runserver 0.0.0.0:8000` and check the ip address in the browser.
19. Register uk.to domain to the website
    https://freedns.afraid.org/
    Add subdomain, wait 24h, done!
    Also names domain registered autogen.uk at https://www.names.co.uk/ on 30 May 2024. AWS deitysix instance started around 24 May 2024.
20. GUNICORN SETUP steps
    1. Stop the running server and deactivate virtual environment
        - right click on powershell window, in properties you can select copy/paste with ctrl shif c+v
    2. Edit socket file with this command `sudo nano /etc/systemd/system/gunicorn.socket`:
        [Unit]
        Description=gunicorn socket
        [Socket]
        ListenStream=/run/gunicorn.sock
        [Install]
        WantedBy=sockets.target

        Ctrl+O, Enter, CTRL+X
        Explanations: Unit is human readable description. Socket is address to communicate with Gunicorn, will be used by Nginx for example. Install is activated early in the boot process.
        `sudo chmod 644 /etc/systemd/system/gunicorn.socket` can be used to grant access permissions.
    3. Edit service file with this command `sudo nano /etc/systemd/system/gunicorn.service`:
        [Unit]
        Description=Gunicorn daemon for 'my_portfolio' application
        Requires=gunicorn.socket
        After=network.target
        [Service]
        User=ubuntu
        Group=www-data
        WorkingDirectory=/home/ubuntu/project_portfolio
        ExecStart=/home/ubuntu/project_portfolio/venv/bin/gunicorn \
            --access-logfile - \
            --error-logfile - \
            --workers 3 \
            --bind unix:/run/gunicorn.sock \
            my_portfolio.wsgi:application
        Restart=on-failure
        [Install]
        WantedBy=multi-user.target
    4. Run these commands to start and enable gunicorn socket
        - Start Gunicorn socket `sudo systemctl start gunicorn.socket`
        - Enable the socket `sudo systemctl enable gunicorn.socket`
        Then checks/tests
        - check status `sudo systemctl status gunicorn.socket`
        - check if file exists `file /run/gunicorn.sock`
        If needed for troubleshooting
        - error logs `sudo journalctl -u gunicorn.sock`
        - reload systemd daemon configuration `sudo systemctl daemon-reload`
        - restart Gunicorn service `sudo systemctl restart gunicorn`
        - test socket `curl --unix-socket /run/gunicorn.sock localhost`
        
22. Setup NGINX
    1. Edit the file with command `sudo nano /etc/nginx/sites-available/project_portfolio`
    ### HTTP version:
    server {
        listen 80;
        server_name 3.10.240.43 autogen.uk www.autogen.uk autogen.uk.to www.autogen.uk.to;
        location = /favicon.ico { access_log off; log_not_found off; }
        location /static/ {
            alias /home/ubuntu/project_portfolio/static/; 
        }

        location / { 
            include proxy_params;
            proxy_pass http://unix:/run/gunicorn.sock;
        }
    }

    ### HTTPS version:
    server {
        listen 80;
        server_name autogen.uk www.autogen.uk autogen.uk.to www.autogen.uk.to;

        # Optional: Additional configuration for handling HTTP traffic (e.g., error pages)
        # If you don't need any specific HTTP handling, you can remove this entire block.
    }

    server {
        listen 443 ssl;
        server_name autogen.uk www.autogen.uk; # Combined server_name for both domains

        # SSL Configuration (Adjust paths if needed)
        ssl_certificate /etc/letsencrypt/live/autogen.uk/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/autogen.uk/privkey.pem;
        include /etc/letsencrypt/options-ssl-nginx.conf;
        ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

        location /static/ {
            alias /home/ubuntu/project_portfolio/static/;
        }

        location /media/ { 
            alias /home/ubuntu/project_portfolio/media/; 
        }

        location / {
            include proxy_params;
            proxy_pass http://unix:/run/gunicorn.sock;
        }
    }

    ### Explanation 
    HTTP version: location Alias, should be better if we run collectstatic for deployment. With the alias directive, when a request comes in for /static/somefile.css, Nginx will look for the file at /home/ubuntu/project_portfolio/static/somefile.css
    HTTPS version: 
    Two server Blocks: There are now two distinct blocks, one for HTTP (port 80) and one for HTTPS (port 443).
    HTTP Redirect: The first server block (port 80) simply redirects all traffic to the HTTPS version of the site using return 301.
    SSL Configuration: The second server block (port 443) includes the ssl directive to enable SSL/TLS encryption. You'll need to replace placeholders with the actual paths to your SSL certificate and private key files.
    Proxy Pass (Optional): If you're using Gunicorn as your application server (as suggested by your previous configurations), the location / block proxies requests to your Gunicorn socket.
    Additional Considerations:

    SSL Certificates: You'll need to obtain an SSL certificate (and the corresponding private key) for your domain or IP address. You can get free certificates from providers like Let's Encrypt or purchase one from a commercial CA.
    Nginx Configuration: Make sure Nginx is configured to load SSL modules and has access to your certificate and key files.
    Firewall: Ensure your firewall (both on the EC2 instance and any external firewalls) allows incoming traffic on port 443 for HTTPS.
    Additional SSL Settings: You can customize the ssl_protocols and ssl_ciphers directives to control the allowed SSL/TLS versions and cipher suites.
    Important:

    Make sure to replace /path/to/your/certificate.crt and /path/to/your/privatekey.key with the actual paths to your SSL certificate and private key files.
    After making changes to the Nginx configuration, test it with sudo nginx -t and reload Nginx with sudo systemctl reload nginx to apply the changes.
    
23. Create SimLink from sites-available to sites-enabled
    `sudo ln -s /etc/nginx/sites-available/project_portfolio /etc/nginx/sites-enabled`
24. Test nginx configuration file `sudo nginx -t`
25. Restart Nginx `sudo systemctl restart nginx`
26. Remove port 8000 listening `sudo ufw delete allow 8000`
27. Allow Nginx through firewall `sudo ufw allow 'Nginx Full'`, check the website
28. Edit Nginx config file to potentiall enable stylesheets
    `sudo nano /etc/nginx/nginx.conf`
    Change `user data-www;` to `user ubuntu;`
    restart nginx `sudo systemctl restart nginx`
        
29. Add proper domain to DNS via Cloudflare
    Once you're logged in, click "Add a site" and enter your domain name (autogen.uk). Click "Add Site."
    Cloudflare will scan for existing DNS records for your domain. This might take a few minutes.
    https://dash.cloudflare.com/52008f119392e27fc8d1d99b94733cc6/add-site

30. Review and Update DNS Records:
    After the scan, Cloudflare will present you with a list of detected DNS records.
    You'll need to add or modify two essential records:
    A Record: Points the domain's root (autogen.uk) to your EC2 instance's public IP address.
    CNAME Record (Optional): If you want to use www.autogen.uk, create a CNAME record pointing it to your root domain (autogen.uk).

31. Change Nameservers:
    Cloudflare will provide you with two nameservers (e.g., ella.ns.cloudflare.com and logan.ns.cloudflare.com).
    Go to your domain registrar (where you purchased the domain) and change the nameservers for your domain to these Cloudflare nameservers. This step is crucial to make Cloudflare the authoritative DNS provider for your domain.
    Change nameservers here:
    https://admin.names.co.uk/controlpanel/nameservers/?domain=autogen.uk

32. Enable Cloudflare Features (Optional):
    Once your nameservers have been updated, you can explore Cloudflare's dashboard to enable various features like:
    SSL/TLS: Get a free SSL certificate for HTTPS.
    Caching: Improve website performance with caching.
    Firewall: Add security with Cloudflare's Web Application Firewall (WAF).
    DNSSEC: Enhance DNS security.
    Example DNS Records:

    Type     Name         Value                           TTL    
    A        autogen.uk   <your_EC2_public_IP_address>    Auto 
    CNAME     www          autogen.uk                      Auto

    Important Considerations:
    DNS Propagation Time: After changing nameservers, it can take up to 48 hours for the changes to propagate globally.
    Orange Cloud: Make sure the cloud icon next to your A and CNAME records in Cloudflare is orange (or proxied). This means Cloudflare will be handling the traffic and providing features like SSL/TLS and caching.
    Flexible vs. Full SSL: If you have an existing SSL certificate on your server, choose the "Full (strict)" SSL mode in Cloudflare to ensure end-to-end encryption. Otherwise, use "Flexible."
    Troubleshooting:

    DNS Issues: If you have trouble accessing your website after switching to Cloudflare, double-check that the DNS records are correct and give it some time for the changes to propagate.
    Nginx Configuration: Make sure your Nginx server configuration is also updated to recognize the new domain names. You can follow the example configuration I provided earlier in our conversation.

33. Get SSL certificate for HTTPS protocol outside CloudFlare:
    https://letsencrypt.org/

    For Ubuntu 22, no snapd installation is required.
    run this command just to make sure we don't have any residue: `sudo apt-get remove certbot`
    the install certbot: `sudo snap install --classic certbot`
    get and install certificate: `sudo certbot --nginx`
    or you can install two certificates at once: `sudo certbot --nginx -d autogen.uk -d www.autogen.uk`
    reload nginx `sudo systemctl reload nginx`
    restart nginx `sudo systemctl restart nginx`

34. DEBUGGING
    Once inevitable debugging starts, remember to always restart Nginx as well as Gunicorn and collect static files for Django. You know why ;)


















## PythonAnywhere
Free service offers server hosting for small Django and Flask projects. 

### Hosting Django app on PythonAnywhere
https://www.youtube.com/watch?v=xtnUwvjOThg&ab_channel=CloudWithDjango

1. Create account, log into Dashboard, go into Bash console
2. Clone repository from Github
    `pwd` to check your current directory
    removing files works through Files panel in dashboard
    `git clone {github-repo-link}` to create project folder, for example `git clone https://github.com/pagrochowski/project_portfolio`
3. Set up virtual environment
    check which python version is utilised with `python --version` and use the version in below command
    setup venv with command `mkvirtualenv venv --python=/usr/bin/python3.10`
4. Install Django and/or other dependencies
    `pip install Django` or cd into project directory and `pip install requirements.txt`
5. Activate virtual environment with `workon venv`
6. Open Web App in dashboard -> Add new Web App -> Manual configuration -> Python 3.10
7. Go to Web App settings and set Virtualenv path to "venv"
8. Navigate to Code: -> WSGI configuration file and open the file
9. Change path to where the app sits and os.environ to where the app is

# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
import os
import sys
#
## assuming your django settings file is at '/home/TragicMagic/mysite/mysite/settings.py'
## and your manage.py is is at '/home/TragicMagic/mysite/manage.py'
path = '/home/TragicMagic/project_portfolio'
if path not in sys.path:
    sys.path.append(path)
#
os.environ['DJANGO_SETTINGS_MODULE'] = 'my_portfolio.settings'
#
## then:
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

10. in settings.py file, set this
`ALLOWED_HOSTS = ['TragicMagic.pythonanywhere.com']`
11. Change to DEBUG = False

## Terraform
Used to automate cloud instance creation and streamline configuration process.

### Docker on EC2 in AWS server
1. Install terraform

https://developer.hashicorp.com/terraform/install?product_intent=terraform

Place the exe file in a folder and add path to that folder to environmental variables in the system (remember about "/" at the path end to access the file)

2. Install AWS CLI 

https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

3. Create Access Key and store the credentials

https://us-east-1.console.aws.amazon.com/iam/home#/security_credentials

Access keys section

3. Configure Terraform file structure inside project folder

project_portfolio/
├── main.tf          (Core infrastructure: EC2, security groups)
├── variables.tf     (Define variables for reusability)
├── outputs.tf       (Expose useful info like the instance's IP)
├── terraform.tfvars (Defining ECR variables)
├── docker-compose.yaml  (Your existing file for local development)
├── Dockerfile        (Your existing file for building the image)

-----------

4. Define IAM role for EC2 to store access credentials safely. 

IAM Roles (Best Practice):

Create an IAM role with permissions to access ECR (e.g., AmazonEC2ContainerRegistryFullAccess).

Access IAM to add new role:
https://us-east-1.console.aws.amazon.com/iam/home?region=us-east-1#/roles

Steps to Create the IAM Role:

Create a New Role: In the IAM console, go to "Roles" and click "Create role."
Select "AWS service" as the trusted entity and choose "EC2" as the use case.
Attach Policy: Search for and attach the AmazonEC2ContainerRegistryReadOnly policy (or a more specific policy if you only need certain permissions). This gives your EC2 instance read-only access to your ECR repositories.
Review and Create: Give your role a descriptive name (e.g., "EC2_ECR_ReadOnly") and create it.

Attaching the Role to Your EC2 Instance: 
This part is done in the main.tf file

#### This step can be automated using GtiHub actions and Github secrets
Add docker image to the ECR repository:

https://eu-north-1.console.aws.amazon.com/ecr/home?region=eu-north-1


5. Create an Amazon ECR Repository:

Free tier: private 500 MB, public 50 GB (cannot be changed after creation)

If you haven't already, create a repository in ECR to store your Docker image. You can do this in the AWS console or using the AWS CLI.
Take note of your ECR repository URI (e.g., 123456789012.dkr.ecr.us-east-1.amazonaws.com/project_portfolio).

Actual:
public.ecr.aws/f9a2r4a5/project_portfolio

6. Build Your Docker Image:

Build your Django project's Docker image if you haven't already:
Bash (-t for tag)
docker build -t project_portfolio:latest .

6. Tag Your Image:

Tag the image with your ECR repository URI and the desired tag (e.g., latest):
Bash
docker tag project_portfolio:latest YOUR_ECR_REPOSITORY_URI/project_portfolio:latest

Actual ECR URI:
docker tag project_portfolio:latest public.ecr.aws/f9a2r4a5/project_portfolio:latest

(You can remove the previously created image)

7. Authenticate with ECR:

Go to Amazon ECR > Public Registry > Repositories

Select repository and click "View push commands" button for set of instructions.

8. Push the Image:

Push the tagged image to your ECR repository:
Bash
docker push YOUR_ECR_REPOSITORY_URI/project_portfolio:latest

4. Deployment (Terraform):

Same steps as before: terraform init, terraform plan, terraform apply.
