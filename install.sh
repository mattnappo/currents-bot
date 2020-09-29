#!/bin/bash

# maybe you already have it installed, i didn't

mkdir -p bin/

wget "https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz" -P bin/

cd bin/
tar -xvzf geckodriver*

chmod +x geckodriver

sudo cp geckodriver /usr/bin/

# then export PATH=$PATH:/bin/
