#!/bin/bash
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/owasp-amass/amass/v3/...@master
go install -v github.com/tomnomnom/assetfinder@latest
go install -v github.com/tomnomnom/waybackurls@latest
pip3 install dirsearch
go install -v github.com/ffuf/ffuf/v2@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
