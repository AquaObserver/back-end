# How to use
1) First create virtual environemt for the api using this command: `"python -m venv .venv"` (can change .venv to any other preferd name for the virtual environment, but don't forget to change .gitignore to ignore the virtual environment)
2) Using bash, activate virtual environment for the api using this command: `". <nameOfTheEnvironment>/bin/activate"`. Now everything you do is in virtual environment and no extra libraries are downloaded to your global python libraries.
3) Using the **requirements.txt** (list of all dependencies used for the project) install them in the virtual environment with this command: `"python -m pip install -r requirements.txt"`
4) If there are problems run "python manage.py migrate" this should fix problems with realocaing code or running it on a nother machine if there are any
5) To run the api for testing run this command: `"python manage.py runserver"`
6) To visit the admin page for more visual representation of data in general and stored data in sqlite go to _/admin_, and login with **username: admin**, **password: admin123**

# TODO
For now we only have an API. Need to implement back-end for notifying user about water level reaching defined treshold.
