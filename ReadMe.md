
#REQUIREMENTS

- [Python 3.5.2+](https://www.python.org/downloads/)
- Django 1.10+

#Setup Instructions

##Windows

1. Install [Python 3.5.2+](https://www.python.org/downloads/)
  1. Ensure the correct version of Python was added to your path by running `python --version` in a command prompt and ensuring the version number matches the requirements
2. Install virtualenv from https://pypi.python.org/pypi/virtualenv
  1. cd into your project directory (where you downloaded the files from github)
  2. Create a virtual environment for the app by calling `mkvirtualenv <app_name>`
3. Ensure you're now working within the virtual environment by checking the command line for something like `(<app_name>)C:\code\project`
  1. Install Django within the virtual environment by calling `pip install django`
  2. Create database for project by calling `python manage.py migrate`
  3. Create superuser for control of the project by typing `python manage.py createsuperuser` and filling in the prompted information
  4. Start project by calling the `start_app.bat` script in the repository
4. Visit the admin page at `localhost:8000/admin` and login using the created superuser
  1. Within the Django admin view create a new `Reporter` referencing the admin account allowing you to use the admin account to create reports
    * Note: Without this step you will be unable to create new reports as you will not have a "validated" account.