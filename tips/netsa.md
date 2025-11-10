Scan all host: `sudo nmap -n -sn -PS22,80,443,8000,8080,445,88 <subnet> -o <subnet>_host_up.txt -v`

Create file only host up:`cat <subnet>_host_up.txt | grep "Nmap scan report for" | grep -v "host down" | cut -d " " -f 5 > <subnet>_host_up_cleaned.txt`

Format nmap: `while read p; do echo -n "$p "; done < <SUBNET>_host_up_cleaned.txt`
