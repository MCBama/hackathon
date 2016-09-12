
#REQUIREMENTS

- Python 3.5.2+
- Django 1.10+

#Setup Instructions

##Windows

1. Install Python 3.5.2+
  1. Ensure the correct version of Python was added to your path by running `python --version` in a command prompt
2. Install virtualenv from https://pypi.python.org/pypi/virtualenv
  1. cd into your project directory (where you downloaded the files from github)
  1. Create a virtual environment for the app by calling `mkvirtualenv <app_name>`
3. Ensure you're now working within the virtual environment by checking the command line for something like `(<app_name>)C:\code\project`
  1. Install Django within the virtual environment by calling `pip install django`
  2. Create database for project by calling `python manage.py migrate`
  3. Create superuser for control of the project by typing `python manage.py createsuperuser` and filling in the prompted information
  4. Start project by calling the 'start_app.bat' script in the repository