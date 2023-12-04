# How to use
1) First create virtual environemt for the api using this command: `"python3 -m venv .venv"` (can change **.venv** to any other preferd name for the virtual environment, but don't forget to change .gitignore to ignore the virtual environment)
2) Using bash, activate virtual environment for the api using this command: `". .<nameOfTheEnvironment>/bin/activate"` or if you are using python version 3.11 activation script has been moved to _.nameOfTheEnvironment/Scrpits_ so use this command: \n`". <nameOfTheEnvironment>/Scripts/activate"`. Now everything you do is in virtual environment and no extra libraries are downloaded to your global python libraries.
3) Using the **requirements.txt** (list of all dependencies used for the project) install them in the virtual environment with this command: `"python -m pip install -r requirements.txt"`
4) Create a superuser by running `./createUser.sh`. This creates a superuser with **username: admin** and **password: admin123** for loging into the _/admin_ page. (If you are on linux give execution premission to the script with `chmod +x ./createUser.sh`)
5) To run the api for testing run this command: `"python manage.py runserver"`
6)  If there are problems with migrations run `"python manage.py migrate"` this should fix problems related to realocaing code or running it on another machine, if there are any
7) To visit the admin page for more visual representation of data in general and stored data in sqlite go to _/admin_, and login with **username: admin**, **password: admin123**

# TODO
For now we only have an API. Need to implement back-end for notifying user about water level reaching defined treshold.
