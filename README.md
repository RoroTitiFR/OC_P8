# Pur Beurre by @RoroTiti

![Screenshot](https://i.imgur.com/8aca2df.jpg)

## User manual

### Getting started

To run the application, it's recommended to set up a virtual environment. We will use virtualenv.

- Move to the source root directory
```
cd "/the/app/directory"
```

- Initialize a virtualenv
```
pip install virtualenv # install virtualenv if not already installed
virtualenv venv
```

- Enable the virtual environment 

  - macOS/Linux
    ```
    source venv/bin/
    ```
    
  - Windows
    ```
    .\venv\Scripts\activate
    ```

- Install Pur Beurre dependencies (if you use macOS, install Postgres on your computer first : [Postgres.app](https://postgresapp.com/))
```
pip install -r requirements.txt
```

- Connect to the database by changing the settings at ``pur_beurre/settings.py``, in DATABASES settings

- Populate the database by running :
````
python manage.py off_download
````

- Compile frontend assets (make sure you have [NodeJS](https://nodejs.org/en/) and [Yarn](https://yarnpkg.com/) installed)
````
yarn build
````

### Run Pur Beurre

- You can now start Pur Beurre with the following commands. Run them from the root of the source code directory.

  - macOS/Linux/Windows
    ```
    python manage.py runserver
    ```
    
- Once the Django server is running, you can now browse the URL given in the terminal to start exploring Pur Beurre.

## Working environment
- Windows 10 or macOS Mojave and upper
- Python 3.8.1
- Postgres 12