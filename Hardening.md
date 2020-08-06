# Hardening steps
Hardening steps to secure the proxy and application server. The hardening on Nginx proxy has been implemented in Ansible using the nginx role.
A self signed certificate has been used to implement HTTPS communication. A role for Letsencrypt based SSL has been written but not implemented as Letsencrypt does not allow for registration of AWS Hostname. 
For the application server, Gunicorn has been used to serve requests and communication is only permitted to the Nginx server using AWS rules. 

## Proxy Server Hardening (Nginx)

### Set properly values of the X-Forwarded-For header
X-Forwarded-For (XFF) is the custom HTTP header that carries along the original IP address of a client.
```
proxy_set_header HOST $host;
proxy_set_header X-Forwarded-Proto $scheme;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Original-URL "";
proxy_set_header X-Rewrite-URL "";
proxy_set_header X-Forwarded-Server "";
proxy_set_header X-Forwarded-Host "";
proxy_set_header X-Host "";
```

### Hide upstream proxy headers and Remove support for legacy and risky HTTP request headers
Hide some standard response headers:
```
proxy_hide_header X-Powered-By;
proxy_hide_header X-AspNetMvc-Version;
proxy_hide_header X-AspNet-Version;
proxy_hide_header X-Drupal-Cache;
```
Hide other risky response headers:
` proxy_hide_header X-Runtime `;

### Run as an unprivileged user
Minimize priledge escalation risk and follow the principle of least privilege.

### Disable unnecessary modules
Compiling from source and using the configure option 
`./configure --without-http_geo_module`

### Disable nginx server_tokens and hide server signature
This information can be used as a starting point for attackers who know of specific vulnerabilities associated with specific versions and might help gain a greater understanding of the systems in use.
`server_tokens off;`

### Disable Any Unwanted HTTP methods
```
location /external {
	limit_except GET { deny all; }
}
```

### Configure Nginx to Include Security Headers
Helps to protect your visitors against clickjacking attacks by declaring a policy whether your application may be embedded on other (external) pages using frames.
`add_header X-Frame-Options "SAMEORIGIN";`
Strict-Transport-Security (HSTS)
`add_header Strict-Transport-Security "max-age=31536000; includeSubdomains; preload";`
CSP and X-XSS-Protection
```
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
add_header X-XSS-Protection "1; mode=block";
```

### Configure SSL and Cipher Suites
It is recommended to enable TLS 1.2/1.3 as older versions have protocol weaknesses and uses older cipher suites
`ssl_protocols TLSv1.2 TLSv1.3;`
When ssl_prefer_server_ciphers is set to on, the web server owner can control which ciphers are available.
`ssl_prefer_server_ciphers on;`
`ssl_ciphers "EECDH+ECDSA+AESGCM EECDH+aRSA+AESGCM EECDH+ECDSA+SHA384 EECDH+ECDSA+SHA256 EECDH+aRSA+SHA384 EECDH+aRSA+SHA256 EECDH+aRSA+RC4 EECDH EDH+aRSA HIGH !RC4 !aNULL !eNULL !LOW !3DES !MD5 !EXP !PSK !SRP !DSS";`

### Use strong Key Exchange with Perfect Forward Secrecy
Parameters from ssl_dhparam define how OpenSSL performs the Diffie-Hellman (DH) key-exchange.
`ssl_dhparam	/etc/nginx/dh{{ nginx_dh_size }}.pem;`
### Restrict access to unused urls
```
location / {
    deny all;
    return 403;
}
```

### Configure logs to monitor malicious activities
```
http {
	access_log  logs/access.log   combined;
	error_log   logs/warn.log     warn;
}
```

### Limiting users requests (DDOS prevention) (http block)
`limit_req_zone $binary_remote_addr zone=one:10m rate=30r/m;`

### Limit the number of connections  (http block)
```
limit_conn_zone $binary_remote_addr zone=addr:10m;
limit_conn addr 10;
```

### Disable directory listing
Prevents directory traversal attacks
```
location / {
	autoindex off;
}
```
### Constant updates
Keep track of security vulnerabilities and apply patches to keep server updated

## Application Server Hardening (Flask)

### Running in python virtual environment
Virtual environment keeps dependencies isolated.

###  Using production-grade gunicorn server
Gunicorn is a WSGI application server suitable for production environment. 

### Limit inbound connections
Use a firewall to expose only the required port.
AWS rules are used to make only the exposed port open on the server. Inbound connection to the server is only allowed on the private IP of the proxy server. 