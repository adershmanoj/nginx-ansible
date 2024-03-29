## Introduction
The application server has been written in Flask and has 3 endpoints. The server has been fronted with Nginx deployed on another server and is accessible on <https://13.232.157.91>

## Installation
Steps to get up and running

### Prerequisites
- Ubuntu (16+)
- Ansible 

### Provisioning the flask server
- Run the server_playbook.yml with the command: `ansible-playbook server_playbook.yml `
- This will download the api.py file and setup a flask server at port 5000(default) with the 3 endpoints.
- Internal at endpoint `/internal`
- External at endpoint `/external`
- Cached at endpoint `/cached` 

### Provisioning the Nginx proxy
- Set the hostname of the flask server to the variable `hostname` in the playbook.
- Run the nginx_playbook.yml with the command `ansible-playbook nginx_playbook.yml`
- This will setup the reverse proxy with the following rules:
- `/cached` will be cached at location `/var/cache/cached`
- `/internal` will be accessible from the IP assigned to `allow_ip` variable in the playbook
- `/external` will be accessible to the public

## Demo (Hosted on AWS)
- The flask server is deployed on [this url](http://ip-172-31-12-97.ap-south-1.compute.internal:5000) and is accessible only from the Nginx proxy
- The Nginx server is deployed on [this URL](https://ec2-13-232-157-91.ap-south-1.compute.amazonaws.com) and IP: <https://13.232.157.91/> and is publically accessible. 
- The endpoints can be accessed as 
    - [/external](https://13.232.157.91/external)
    - [/internal](https://13.232.157.91/internal)
    - [/cached](https://13.232.157.91/cached)
