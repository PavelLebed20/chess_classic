# Chess Classic 
# Project description
Chess classic is open source online chess supports possibility of
offline game against AI with chess board and figures skinning. 
### Our features are
* Modern game visualization and animation
* Changing figures render models
* Showing your game skin to online opponent
* Project is open source
## Analogue 1
* https://steamcommunity.com/sharedfiles/filedetails?id=1613886175 - dota auto chess
 is a game that emphasises fast and fluid gameplay that simultaneously avoids the emphasis on APM and twitch-like
 reflexes. How you play your pieces matters far more than how fast you can click! 
 As a custom mode, it's available for free from the Steam Workshop.
### Our advantage are
* Classic chess game rules 
* Free skin change
* Project is open source
* Choosing own gamestate sound
## Analogue 2
* https://www.dreamchess.org/ - DreamChess is an open source chess game. 
 Our primary target platforms are Windows, Mac OS X and Linux. 
 DreamChess features 3D OpenGL graphics and provides various chess board sets, 
 ranging from classic wooden to flat figurines.
### Our advantage are
* Multilayer 
* Free skin change
* Choose own gamestate sound
# Installation quid
## Install python
* https://www.python.org/downloads/release/python-372/ - download python 3.7
### run commands:
* pip install --upgrade pip
* pip install altgraph==0.16.1
cffi==1.12.2
cycler==0.10.0
future==0.17.1
kiwisolver==1.0.1
macholib==1.11
matplotlib==3.0.3
numpy==1.16.2
panda3d==1.10.1
pandas==0.24.1
pefile==2018.8.8
pycparser==2.19
PyInstaller==3.4
pyparsing==2.3.1
python-chess==0.26.0
python-dateutil==2.8.0
pytz==2018.9
pywin32-ctypes==0.2.0
scipy==1.2.1
seaborn==0.9.0
six==1.12.0
vectormath==0.2.1
## Install sql server
* https://www.microsoft.com/en-US/download/details.aspx?id=42299 - install Express 
and Tools version
* set mixed authorization mode
# Git workflow
* Main demonstration branch - *master*
* Main coding branch - *develop*
* For feature development branch from *develop*, use the template: #<issue_number>_<brief_description>
* Feature branch merges only with *develop* branch
* *develop* merges with *master* at the end of each sprint
* Create new commit for each branch
* Do not delete branches after each merge

### Example of branches
```
#228_add_user_registration
#1488_add_random_ai
```
## Commit
* Subject line is **short** complete summary, starting with #<issue_number>
* Do not end the subject line with a period
* Capitalize the subject line and each paragraph
* Use the imperative mood in the subject line
* Do not explain how you have done something
* Use the body to explain what and why you have done something
  * List with bullet points
  * Use imperative mood

### Example
Subject line:
```
#322 Add Encryption
```
Body:
```
- Add start key creation.
```
# Code style
## Python
* Each file start with header taht contains module purpose, author, last update date
* Each function starts with """ header, contains function arguments, returns type, and function purpose
* Other style definitions are described in https://pythonworld.ru/osnovy/pep-8-rukovodstvo-po-napisaniyu-koda-na-python.html

# Development team
1) [Lebed Pavel](https://github.com/PavelLebed20) - **teamlead**
2) [Federov Dmitry](https://github.com/dimaaa1fed)
3) [Tunikov Dmitry](https://github.com/DmitriiTunikov) - **techlead**
4) [Nazarov Nikita](https://github.com/nekit-000000)
5) [Yangildin Ivan](https://github.com/IvanYangildin)
