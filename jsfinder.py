import os
import subprocess
import requests
from bs4 import BeautifulSoup
from termcolor import colored
import time

target_domain = input("Enter target domain: ")
time.sleep(2)
print("\n")
lolz1 = lambda x: colored(x, 'yellow', 'on_magenta',  attrs=['bold', 'reverse', 'blink', 'underline'])
print((lolz1('Searching for js files on target domain...')))


js_files = []
response = requests.get(f"https://{target_domain}")
soup = BeautifulSoup(response.content, 'html.parser')
for script in soup.find_all('script'):
    if script.get('src'):
        if ".js" in script['src']:
            js_files.append(script['src'])


with open('results.txt', 'w') as f:
    for js_file in js_files:
        f.write(f"{js_file}\n")
print("\n")
lolz10 = lambda x: colored(x, 'yellow', 'on_magenta',  attrs=['bold', 'reverse', 'blink', 'underline'])
print((lolz10('Finished searching for js files on target domain...')))
time.sleep(2)
print("\n")

lolz2 = lambda x: colored(x, 'yellow', 'on_magenta',  attrs=['bold', 'reverse', 'blink', 'underline'])
print((lolz2('Running some deep scans...')))

subdomains_file = 'subdomains.txt'
subfinder_output = subprocess.check_output(f"subfinder -d {target_domain} -silent", shell=True)
with open(subdomains_file, 'wb') as f:
    f.write(subfinder_output)
assetfinder_output = subprocess.check_output(f"assetfinder --subs-only {target_domain}", shell=True)
with open(subdomains_file, 'ab') as f:
    f.write(assetfinder_output)
amass_output = subprocess.check_output(f"amass enum -d {target_domain} -silent", shell=True)
with open(subdomains_file, 'ab') as f:
    f.write(amass_output)
print("\n")
lolz11 = lambda x: colored(x, 'yellow', 'on_magenta',  attrs=['bold', 'reverse', 'blink', 'underline'])
print((lolz11('Finished with some deep scans...')))
time.sleep(2)
print("\n")


lolz3 = lambda x: colored(x, 'yellow', 'on_magenta',  attrs=['bold', 'reverse', 'blink', 'underline'])
print((lolz3('Filtering invalid results...')))

valid_subdomains = []
with open(subdomains_file, 'r') as f:
    total_valid_subdomains = len(f.readlines())
    f.seek(0)
    processed_subdomains = 0
    for subdomain in f:
        subdomain = subdomain.strip()
        command = f"httpx -silent -mc 200,301,302,403 https://{subdomain}"
        response = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
        if response.stdout:
            valid_subdomains.append(subdomain)

        # Calculate and print progress
        processed_subdomains += 1
        progress = int(processed_subdomains / total_valid_subdomains * 100)
        print("\n")
        print(f"Filtering subdomains: {progress}% complete", end='\r')
print("\n")
lolz12 = lambda x: colored(x, 'yellow', 'on_magenta',  attrs=['bold', 'reverse', 'blink', 'underline'])
print((lolz12('Finished filtering...')))
time.sleep(2)
print("\n")



dirsearch_path = "/home/kali/Desktop/github/dirsearch/dirsearch.py"
ffuf_path = "ffuf"
wordlist_path = "/usr/share/seclists/Discovery/Web-Content/common.txt"
with open('results.txt', 'a') as f:
    total_valid_subdomains = len(valid_subdomains)
    processed_subdomains = 0
    for subdomain in valid_subdomains:
        dirsearch_command = f"python3 {dirsearch_path} -u https://{subdomain} -w {wordlist_path}"
        dirsearch_output = subprocess.check_output(dirsearch_command, shell=True)
        f.write(dirsearch_output.decode('utf-8'))

        ffuf_command = f"{ffuf_path} -u https://{subdomain}/FUZZ -w {wordlist_path} -mc 200"
        ffuf_output = subprocess.check_output(ffuf_command, shell=True)
        f.write(ffuf_output.decode('utf-8'))

        
        processed_subdomains += 1
        progress = int(processed_subdomains / total_valid_subdomains * 100)
        print(f"Running Dirsearch and FFUF: {progress}% complete", end='\r')

lolz4 = lambda x: colored(x, 'yellow', 'on_magenta',  attrs=['bold', 'reverse', 'blink', 'underline'])
print((lolz4('Preparing Results...')))

total_valid_subdomains = len(valid_subdomains)
processed_subdomains = 0
for subdomain in valid_subdomains:
    response = requests.get(f"https://{subdomain}")
    soup = BeautifulSoup(response.content, 'html.parser')
    for script in soup.find_all('script'):
        if script.get('src'):
            if ".js" in script['src']:
                with open('results.txt', 'a') as f:
                    f.write(f"{script['src']}\n")

    processed_subdomains += 1
    progress = int(processed_subdomains / total_valid_subdomains * 100)
    print(f"Finding JS files on valid subdomains: {progress}% complete", end='\r')
print("\n")
lolz14 = lambda x: colored(x, 'yellow', 'on_magenta',  attrs=['bold', 'reverse', 'blink', 'underline'])
print((lolz14('Finished results...')))
time.sleep(2)
print("\n")



waybackurls_output = subprocess.check_output(f"waybackurls https://{target_domain} | grep -i '\.js$'", shell=True)
with open('results.txt', 'ab') as f:
    f.write(waybackurls_output)

lolz5 = lambda x: colored(x, 'yellow', 'on_magenta',  attrs=['bold', 'reverse', 'blink', 'underline'])
print((lolz5('Printing results...')))
print("\n")
time.sleep(2)

with open('results.txt', 'r') as f:
    for line in f:
        if ".js" in line:
            print(colored(line.strip(), 'green'))
