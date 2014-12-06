#!/bin/bash
sudo yum install -y python-devel
sudo yum install -y python-pip
sudo pip install mrjob numpy nltk
sudo python -m nltk.downloader -d /usr/share/nltk_data all
yes | sudo yum install perl-CPAN
yes | sed 's/y//' | sudo cpan install HTML::Parser
sudo cpan install HTML::Parser
sudo easy_install pysentiment

