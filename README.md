# Backend Assignment

BackendAssignment is a web-based API designed to cater to bloggers and readers. It offers seamless user registration and authentication, ensuring a secure experience. Users can effortlessly pen down their thoughts with the blog post feature and share them with a wider audience. Furthermore, readers have the capability to browse through a collection of posts, diving into content that resonates with them.

## Project Setup

Python Version: 3.10.6

Assumption: Project is cloned, and current working directory in terminal/cmd is `/BackendAssignment`.


### Set Python Virtual Environment (recommended)

Install [Python Virtual Environment](https://www.geeksforgeeks.org/creating-python-virtual-environment-windows-linux/)

To Activate virtual environment

For Linux

    source myenv/bin/activate 

For Windows

    myenv\Scripts\activate


### Install Required Python Packages

    pip install -r requirements.txt

### Create Environment

Create `.env` file

    # For Linux
    cp sample_env.txt .env

    # For Windows
    copy sample_env.txt .env

Change environment variables in `.env` file

#### Variables Description

- `DB_NAME`: `database_name`
- `DB_USER`: `database_user_name`
- `DB_PASS`: `database_user_password`
- `DB_PORT`: `database_port`
- `DB_HOST`: `database_host`


### Database Migrations

Run below commands to create tables in database

    python manage.py makemigrations
    python manage.py migrate


### Run Server

To run Local Development Server, run below cmd

    python manage.py runserver


### Postman Collection

How to import postman collection?

- Open postman & click on the import button.
- Select the json collection file(Which you can find at root level of this project) and click on the import.
- Create an one environment(must needed).
- In that environment create below variables
    1. BASE_URL
    2. ACCESS_TOKEN 
    3. REFRESH_TOKEN 
- So, copy and paste your local url into the environment variable's BASE_URL. Ex: [**http://127.0.0.1:8000/**]
- Now, use the Register API to signup and then call Login API.
- Once you logged in you can call other APIs.
