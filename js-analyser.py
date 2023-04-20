import pyfiglet
import os
import re
from termcolor import *

word = "JS-Analyse"
banner = pyfiglet.figlet_format(word)
print("\n")
print(banner)
print("\n")
lolz1 = lambda x: colored(x, 'yellow', 'on_magenta',  attrs=['bold', 'reverse', 'blink', 'underline'])
print((lolz1('Searching for js files...')))
print("\n")

with open('results.txt', 'r') as f:
    
    for endpoint in f:
        
        endpoint = endpoint.strip()

        
        curl_command = f"curl -i -k -L -s {endpoint}"
        response = os.popen(curl_command).read()

        
        if "HTTP/1.1 200" in response or "HTTP/1.1 301" in response or "HTTP/1.1 302" in response:
            
            try:
                headers, body = response.split('\r\n\r\n', 1)
            except ValueError:
                error_message = f"Error: Could not parse response for endpoint {endpoint}\n"
                with open('output.txt', 'a') as output_file:
                    output_file.write(error_message)
                    output_file.write(f"Response:\n{response}\n")
                continue

            
            with open('output.txt', 'a') as output_file:
                output_file.write(f"\n\nResponse for endpoint: {endpoint}\n\n")
                output_file.write(body)
        else:
            error_message = f"Error: Failed to retrieve a valid response for endpoint {endpoint}\n"
            with open('output.txt', 'a') as output_file:
                output_file.write(error_message)

print("\n")
print("\n")

lolz2 = lambda x: colored(x, 'yellow', 'on_magenta',  attrs=['bold', 'reverse', 'blink', 'underline'])
print((lolz2('Searching for secret info...')))

print("\n")

regex_dict = {
    'google_api': (r'AIza[0-9A-Za-z-_]{35}', 'output.txt'),
    'firebase': (r'AAAA[A-Za-z0-9_-]{7}:[A-Za-z0-9_-]{140}', 'output.txt'),
    'google_captcha': (r'6L[0-9A-Za-z-_]{38}|^6[0-9a-zA-Z_-]{39}$', 'output.txt'),
    'google_oauth': (r'ya29\.[0-9A-Za-z\-_]+', 'output.txt'),
    'amazon_aws_access_key_id': (r'A[SK]IA[0-9A-Z]{16}', 'output.txt'),
    'amazon_mws_auth_toke': (r'amzn\\.mws\\.[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', 'output.txt'),
    'amazon_aws_url': (r's3\.amazonaws.com[/]+|[a-zA-Z0-9_-]*\.s3\.amazonaws.com', 'output.txt'),
    'amazon_aws_url2': (r"(" \
        r"[a-zA-Z0-9-\.\_]+\.s3\.amazonaws\.com" \
        r"|s3://[a-zA-Z0-9-\.\_]+" \
        r"|s3-[a-zA-Z0-9-\.\_\/]+" \
        r"|s3.amazonaws.com/[a-zA-Z0-9-\.\_]+" \
        r"|s3.console.aws.amazon.com/s3/buckets/[a-zA-Z0-9-\.\_]+)", 'output.txt'),
    'facebook_access_token': (r'EAACEdEose0cBA[0-9A-Za-z]+', 'output.txt'),
    'authorization_basic': (r'basic [a-zA-Z0-9=:_\+\/-]{5,100}', 'output.txt'),
    'authorization_bearer': (r'bearer [a-zA-Z0-9_\-\.=:_\+\/]{5,100}', 'output.txt'),
    'authorization_api': (r'api[key|_key|\s+]+[a-zA-Z0-9_\-]{5,100}', 'output.txt'),
    'mailgun_api_key': (r'key-[0-9a-zA-Z]{32}', 'output.txt'),
    'twilio_api_key': (r'SK[0-9a-fA-F]{32}', 'output.txt'),
    'twilio_account_sid': (r'AC[a-zA-Z0-9_\-]{32}', 'output.txt'),
    'twilio_app_sid': (r'AP[a-zA-Z0-9_\-]{32}', 'output.txt'),
    'paypal_braintree_access_token': (r'access_token\$production\$[0-9a-z]{16}\$[0-9a-f]{32}', 'output.txt'),
    'square_oauth_secret': (r'sq0csp-[ 0-9A-Za-z\-_]{43}|sq0[a-z]{3}-[0-9A-Za-z\-_]{22,43}', 'output.txt'),
    'square_access_token': (r'sqOatp-[0-9A-Za-z\-_]{22}|EAAA[a-zA-Z0-9]{60}', 'output.txt'),
    'stripe_standard_api': (r'sk_live_[0-9a-zA-Z]{24}', 'output.txt'),
    'stripe_restricted_api': (r'rk_live_[0-9a-zA-Z]{24}', 'output.txt'),
    'github_access_token': (r'[a-zA-Z0-9_-]*:[a-zA-Z0-9_\-]+@github\.com*', 'output.txt')
}

for key, (regex, file_name) in regex_dict.items():
    matches = []
    with open(file_name, 'r') as f:
        for line_num, line in enumerate(f, start=1):
            for match in re.finditer(regex, line):
                matches.append((match.group(), file_name, line_num))
    if matches:
        print(f"Matches for {key}:")
        for match, file, line in matches:
            print(f"\t- {match} found in {file}, line {line}")
    else:
        print(f"No matches found for {key}")
