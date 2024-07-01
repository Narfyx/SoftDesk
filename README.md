![alt text](https://user.oc-static.com/upload/2023/06/28/16879473703315_P10-02.png)

# SoftDesk

SoftDesk, a collaboration software publishing company, decided to publish an application allowing you to report and track technical problems. This solution, SoftDesk Support, is aimed at B2B (Business to Business) companies.
## Objective

In this project, you will improve your skills to create a high-performance **RESTful API** with **Django REST**.

This project is an opportunity to implement and secure an API while respecting modern security and data protection standards, such as **OWASP and GDPR** standards as well as **Green Code* best practices. *.

## install requirements
```python
pipenv install
pipenv shell
```

## Start Django server:

Linux/Mac:
```bash
python src/manage.py runserver
```

Windows:
```powershell
python src\manage.py runserver
```

You will see this message in your terminal:
```bash
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
June 30, 2024 - 09:24:22
Django version 5.0.6, using settings 'softdesk.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

## Generate migrations

To create new migrations based on the changes made to the models, run:
```bash
python manage.py makemigrations
```

## Apply migrations

To apply the migrations and synchronize the database schema with the defined models, run:
```bash
python manage.py migrate
```


By combining these sections, you will have a clear and concise explanation of how to use `makemigrations` and `migrate` to manage migrations in Django.

## Features

- User registration and authentication
- Creation and management of projects
- Adding contributors to projects
- Creation and management of issues
- Creation and management of comments

## API Endpoints

### Users

- `GET /user/all/?page={page_number}`: Show all users
- `POST /user/register/`: Registration of a new user
- `POST /user/token/`: Authentication and obtaining a JWT token
- `POST /user/token-refresh/`: Refreshing the JWT token
- `GET /user/`: Retrieve authenticated user details
- `PUT /user/`: Update authenticated user details
- `DELETE /user/`: Delete the authenticated user's account

### Projects

- `POST /project/create/`: Create a new project
- `GET /project/all/?page={page_number}`: Retrieve the list of projects
- `GET /project/{project_id}/`: Retrieve project details
- `PUT /project/{project_id}/`: Update a project
- `PATCH /project/{project_id}/`: Partially update a project
- `DELETE /project/{project_id}/`: Delete a project
- `PUT /project/contributors/`: Add a contributor to a project
- `DELETE /project/contributors/`: Delete a contributor from a project

### Issues

- `POST /project/issue/create/`: Create a new issue
- `GET /project/issue/all/?page={page_number}`: Retrieve the list of issues
- `GET /project/issue/{issue_id}/`: Retrieve the details of an issue
- `PUT /project/issue/{issue_id}/`: Update an issue
- `PATCH /project/issue/{issue_id}/`: Partially update an issue
- `DELETE /project/issue/{issue_id}/`: Delete an issue

### Comments

- `POST /project/comment/create/`: Create a new comment
- `GET /project/comment/all/?page={page_number}`: Retrieve the list of comments
- `GET /project/comment/{comment_id}/`: Retrieve comment details
- `PATCH /project/comment/{comment_id}/`: Update a comment
- `DELETE /project/comment/{comment_id}/`: Delete a comment
