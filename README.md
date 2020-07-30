## Introduction
The application server has been written in Flask and has 3 endpoints. The server has been fronted with Nginx deployed on another server and is accessible on <http://13.233.172.101>

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
- Run the nginx_playbook.yml with the command `ansible-playbook server_playbook.yml`
- This will setup the reverse proxy with the following rules:
- `/cached` will be cached at location `/var/cache/cached`
- `/internal` will be accessible from the IP assigned to `allow_ip` variable in the playbook
- `/external` will be accessible to the public

## Demo (Hosted on AWS)
- The flask server is deployed on [this url](http://ec2-15-207-85-236.ap-south-1.compute.amazonaws.com:5000) and is accessible only from the Nginx proxy
- The Nginx server is deployed on [this URL](ec2-13-233-172-101.ap-south-1.compute.amazonaws.com) and IP: <http://13.233.172.101> and is publically accessible. 
- The endpoints can be accessed as 
    - [/external](http://13.233.172.101/external)
    - [/internal](http://13.233.172.101/internal)
    - [/cached](http://13.233.172.101/cached)
