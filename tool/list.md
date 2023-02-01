## Custom password wordlist generator

https://github.com/sc0tfree/mentalist

## Profilator authentication flow

https://github.com/Mebus/cupp

## Subdomain Search

### AMASS
<code> amass enum -passive -d DOMAIN -src </code>
  
### NMAPPER - SUBDOMAIN FINDER
- https://www.nmmapper.com/sys/tools/subdomainfinder/

## Directory Enumeration with cookie
<code>python3 dirsearch.py -u URL -w db/dicc.txt -x 400,403,404 --cookie='name=value' </code>


## Nikto enumeration

- modify STATIC-COOKIE in */etc/nikto.conf* insert STATIC-COOKIE="name=value";""name:value";

<code> nikto -h URL </code>


## Crawler / Web Spider
<code> curl --silent "URL" | grep -E '<a.*href=.*/a>' | sed -E 's/^.*<a.*href="(.*)">.*/\1/g'</code>

  
 ## SQLMAP
  <code> python sqlmap.py -r request.txt --force-ssl --risk=3 --level=5 --dbs --flush-session --technique=BEUS</code>
  
## Editor Swagger 
  https://editor.swagger.io/

