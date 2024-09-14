# Insta-Tool
Insta-Tool is a tool written in Python using the instaloader library to get informations about your and others instragram accounts.
In order to access Instagram data it uses Firefox cookies so you just need to login to your account using Firefox and you don't need to provide any information to thirds.

You can run the analysis alone in the terminal by using `py src/InstaTool.py loggedUsername targetedUsername` (be sure to decomment the last rows of the InstaTool.py script in order to let it run)
Otherwise you can use the GUI application by running `py src/InstaToolApp.py` or by running the .exe file in the "dist" folder.
To make your own build of the program run `pyinstaller InstaTool.spec` in the terminal.

The process is simple:
- login to your Instagram account using Firefox
- type your username in the corrisponding app box or as the first argument in the terminal
- type the username of the account you want to analyze in the corrisponding app box or as the second argument in the terminal

I hope you will find this tool useful!

Francesco Bittasi 2024
