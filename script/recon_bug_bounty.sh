#!/bin/bash

# Set the target URL
url="https://example.com"

# Set the output file
output_file="recon_results.txt"

# Perform subdomain enumeration
echo "Performing subdomain enumeration..."
subdomains=$(subfinder -d $url)
echo $subdomains >> $output_file

# Perform directory and file discovery
echo "Performing directory and file discovery..."
dirsearch -u $url -e * >> $output_file

# Check for open ports and running services
echo "Performing port scan..."
nmap -sC -sV $url >> $output_file

# Check for known vulnerabilities
echo "Checking for known vulnerabilities..."
vulners -s $url >> $output_file

# Check getallurls
echo "Check getallurls"
gau -s $url

echo "Recon complete!"
