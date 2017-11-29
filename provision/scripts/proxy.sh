#! /bin/bash
#
# proxy.sh
# Copyright (C) 2017 Ryan Mackenzie White <ryan.white4@canada.ca>
#
#
sudo touch /etc/environment
echo -e "http_proxy=\"http://user:passwd@stcweb.statcan.ca:80/\"" | sudo tee -a "/etc/environment"
echo -e "https_proxy=\"http://user:passwd@stcweb.statcan.ca:80/\"" | sudo tee -a "/etc/environment"
echo -e "ftp_proxy=\"http://user:passwd@stcweb.statcan.ca:80/\"" | sudo tee -a "/etc/environment"
echo -e "no_proxy=\"localhost,127.0.0.1,localaddress.,.localdomain.com,statcan.ca\"" | sudo tee -a "/etc/environment"
echo -e "HTTP_PROXY=\"http://user:passwd@stcweb.statcan.ca:80/\"" | sudo tee -a "/etc/environment"
echo -e "HTTPS_PROXY=\"http://user:passwd@stcweb.statcan.ca:80/\"" | sudo tee -a "/etc/environment"
echo -e "FTP_PROXY=\"http://user:passwd@stcweb.statcan.ca:80/\"" | sudo tee -a "/etc/environment"
echo -e "NO_PROXY=\"localhost,127.0.0.1,localaddress.,.localdomain.com,statcan.ca\"" | sudo tee -a "/etc/environment"

