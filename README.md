<a href="https://github.com/DumbSec/Project-Medusa"><img alt="GitHub love" src="https://img.shields.io/badge/Love-100%25-red?style=social&logo=github&logoColor=red"></a>   <img alt="Scrutinizer code quality (GitHub/Bitbucket)" src="https://scrutinizer-ci.com/g/DumbSec/Project-Medusa/badges/quality-score.png?b=master">   <a href="https://github.com/DumbSec/Project-Medusa/blob/master/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/BatSec/Project-Medusa"></a>
# Project-Medusa <img src="https://github.com/BatSec/Project-Medusa/blob/master/assets/icon.png" width="48">
Medusa is a cross-platform music player based on python3.

# Design

<p align="center">
  <img src="https://github.com/BatSec/Project-Medusa/blob/master/assets/medusa.png">
</p>

## Requirements
Please make sure all the following requirements are satisfied or else the program might crash

      * python3
      * vlc runtime
      * tkinter
      * tinytag
      * PIL
      * config

## Installing Requirements
Run the either of the following commands depending on you system configuration. This will install all the dependencies.

     sudo pip install -r requirements.txt
     
## Configuaration
To change the location of the music directory, edit the 18<sup>th</sup> line in medusa.py

such as <br />
config.path = "/music/directory/"

## Create Executable from source-code
To create an executable from the source-code, type the following command

     sudo pip install pyinstaller
     pyinstaller --add-data 'assets/*:assets' --add-data '/usr/lib/x86_64-linux-gnu/vlc/plugins/*:plugins' --onefile medusa.py --hidden-import='PIL._tkinter_finder'

## Issues
Incase of any issues with the application, feel free to file an issue. I'll look into it ASAP.
