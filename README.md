# Auctionable Change API [![Build Status](https://travis-ci.com/Auctionable-Change/auctionable_change_api.svg?branch=master)](https://travis-ci.com/Auctionable-Change/auctionable_change_api)

## Description

**Auctionable Change API** is the backend API for our [Turing School of Software and Design](https://turing.io/) capstone project, **Auctionable Change**.

The idea behind **A.change** is creating a platform in which an individual can post an item for sale/auction, set a minimum asking price and then select a charity to which the funds from that item's sale would be donated.

This **API** functions to consume a charity listing/ranking API and return that information to the front end, as well as provide full endpoints for creating, maintaining and accessing information within the database.

## Endpoints

https://auctionable-change-api.herokuapp.com/swagger


## Application Links

BE Production: https://auctionable-change-api.herokuapp.com/


FE Repo: https://github.com/Auctionable-Change/auctionable_change  

## Local Setup Instructions
#### Python and Flask Setup

- Clone this repo to your local machine using SSH:
  ```
  git clone git@github.com:Auctionable-Change/auctionable_change_api.git
  ```
- Navigate to the new directory:
  ```
  cd auctionable_change_api
  ```
- Set up virtual environment
  ```
  python3 -m venv venv
  . venv/bin/activate
  ```
- Install Flask (if necessary)
  ```
  pip install Flask
  ```
- Install packages in requirements.txt:
  ```
  pip install -r requirements.txt
  ```
- Set environment variables (place in an `.env` file at the root level)
  ```APP_SETTINGS="development"
  DATABASE_URL="postgresql://localhost/auctionable_change_api"
  FLASK_APP=app
  CHARITY_APP_ID=<register for your own>
  CHARITY_APP_KEY=<register for your own>
  ```

#### Database Setup

![Screenshot](public/AC_tables_7-26-20.png)
- Run the Alembic migrations to add tables to database:
  ```
  python manage.py db migrate
  python manage.py db upgrade
  ```

#### Starting Flask Server

- To run server on `localhost:5000/`:
  ```
  python run.py
  ```

## Testing and Coverage
- To run a testing and coverage report utilizing the included `coverage` module:
  ```
  nosetests --cover-package=application --with-coverage
  ```

## Dev Team BE

 - Stephanie Friend ([GitHub](https://github.com/StephanieFriend), [LinkedIn](https://www.linkedin.com/in/s-friend/))
 - Kevin McGrevey ([GitHub](https://github.com/kmcgrevey), [LinkedIn](www.linkedin.com/in/‎kevin-mcgrevey‎-8660958/))
 - Andrew Reid ([GitHub](https://github.com/reid-andrew), [LinkedIn](https://www.linkedin.com/in/reida/))

 ## Technologies and Frameworks

- Back-End
  - Language: Python 3.8.4
  - Framework: Flask 1.1.2
  - Testing: Nose
  - Database: PostgreSQL
  - Database Interaction & ORM: SQLAlchemy
  - Database Migrations: Alembic (via Flask-Migration wrapper)
  - API management: Flask-RESTful, Requests
- CI/CD
  - Continuous Integration: TravisCI
  - Deployment: Heroku
- Project Management
  - Kanban & Sprint Planning: Github Project Boards
  - Agile Planning & Retros: Miro
  - Communication: Zoom, Slack, Tuple