![aws-rds-logo svg](https://github.com/Mrokus95/SchoolManagmentApp/assets/59625513/7e14dca4-f706-4d44-acbb-921b404f7b51)![aws-rds-logo svg](https://github.com/Mrokus95/SchoolManagmentApp/assets/59625513/5ff4243d-d7f3-45fe-93ea-372af36d6ec8)![aws-rds-logo svg](https://github.com/Mrokus95/SchoolManagmentApp/assets/59625513/d1bd6f6a-128d-4d12-ae87-56e52cad0d3c)![postgresql-logo svg](https://github.com/Mrokus95/SchoolManagmentApp/assets/59625513/c6518a0a-0d32-4959-9b7e-41b6262a1d91)# SchoolManagmentApp

Welcome to the School Management App, a web application designed to streamline and manage various aspects of educational institutions. This project is built using a powerful stack of technologies, ensuring a robust and efficient solution.

[![AWS RDS](https://img.shields.io/badge/AWS%20RDS-Cloud-orange)](https://aws.amazon.com/rds/) [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-orange)](https://www.postgresql.org/) [![Django](https://img.shields.io/badge/Django-Backend-blue)](https://www.djangoproject.com/) [![Python](https://img.shields.io/badge/Python-Backend-blue)](https://www.python.org/) [![HTML5](https://img.shields.io/badge/HTML5-Frontend-yellow)](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5) [![CSS](https://img.shields.io/badge/CSS3-Frontend-yellow)](https://developer.mozilla.org/en-US/docs/Web/CSS) [![JavaScript](https://img.shields.io/badge/JavaScript-Frontend-yellow)](https://developer.mozilla.org/en-US/docs/Web/JavaScript) [![Bootstrap](https://img.shields.io/badge/Bootstrap-Frontend-yellow)](https://getbootstrap.com/) 

![Home page](https://github.com/Mrokus95/SchoolManagmentApp/assets/59625513/d3abdfbe-1bf6-4752-bf9a-1a2e36fb742b)

## Table of contents
* [Installation process](#installation-process)
* [Technologies](#technologies)
* [Features](#features)


## Installation process:

1. Clone the repository to your local computer:

    ```
    $ git clone 'https://github.com/Mrokus95/SchoolManagmentApp.git'
    ```

2. Navigate to the project directory:

    ```
    $ cd SchoolManagmentApp
    ```

3. (Optional) It is recommended to create and activate a Python virtual environment:

    ```
    $ python -m venv venv
    $ python venv/bin/activate
    ```

4. Install the required dependencies:

    ```
    $ pip install -r requirements.txt
    ```

5. Set the environment variables:

    **General Django settings:**
    - `SECRET_KEY`: Django secret key (automatically generated when creating a Django project)
    - `DEBUG`: True

    **AWS RDS settings:**
    - `NAME`: The database name.
    - `USER`: The username that you configured for your database.
    - `PASSWORD`: The password that you configured for your database.
    - `HOST`: The hostname of the DB instance.
    - `PORT`: The port where the DB instance accepts connections. The default value varies among DB engines.

    **Gmail account credentials:**
    - `EMAIL_HOST_USER`: The email address
    - `EMAIL_HOST_PASSWORD`: The key or password app

    **Gmail SMTP settings:**
    - `EMAIL_HOST`: 'smtp.gmail.com'
    - `EMAIL_USE_TLS`: True
    - `EMAIL_PORT`: 587

    You can set the environment variables on your operating system or place them in a .env file in the project's root directory.

6. Run the Django development server:

    ```
    $ python manage.py runserver
    ```

    The application will be available at http://localhost:8000/.

## Technologies

We have utilized a diverse range of technologies to develop the School Management App, ensuring its functionality, scalability, and efficiency.

### AWS RDS (Amazon Relational Database Service)

![aws rds](https://github.com/Mrokus95/SchoolManagmentApp/assets/59625513/93a6776b-0dfb-4d21-8cb7-15af08644212)

We integrated AWS RDS to host our database in the Amazon cloud. This allowed us to work collaboratively on the same dataset while gaining experience in cloud-based services integration. The use of Amazon RDS enables efficient and reliable data storage.

### PostgreSQL Database
![postgreSQL](https://github.com/Mrokus95/SchoolManagmentApp/assets/59625513/017d3d41-b9bd-4c05-b5c7-8cd1e32e5efc)

To surpass the limitations of SQLite and enhance our relational database capabilities, we migrated to PostgreSQL. This allowed us to work with larger datasets and practice handling more complex database interactions. 

### HTML5, CSS, JS, and Bootstrap

![html5-logo png](https://github.com/Mrokus95/SchoolManagmentApp/assets/59625513/78447f01-ef70-44ce-b7d7-e10729e3c4a0) 

![js](https://github.com/Mrokus95/SchoolManagmentApp/assets/59625513/0c875413-b287-4950-8d9f-d4daeb87346f)
![css3](https://github.com/Mrokus95/SchoolManagmentApp/assets/59625513/be020416-3f50-4d2b-a3e0-85847c5e3312)
![bootstrap](https://github.com/Mrokus95/SchoolManagmentApp/assets/59625513/16bd8ee7-c4b9-4125-a6c1-34aeeb83c5d0)

For the frontend, we leveraged HTML5, CSS3, JavaScript, and Bootstrap5. These technologies collectively allowed us to design and develop a responsive, user-friendly, and visually appealing user interface.

### Python and Django

![python](https://github.com/Mrokus95/SchoolManagmentApp/assets/59625513/b82413c4-2b4c-4c82-a06d-b0ba5cdeebfe)
![django](https://github.com/Mrokus95/SchoolManagmentApp/assets/59625513/6cb9996c-5ab0-4797-a422-1c8894d2b7de)


The backend of the project was developed using Python 3.12 and Django 4.2. Python's versatility and readability empowered us to create robust backend logic. Django's high-level framework facilitated rapid development, efficient database management, and seamless integration of various components.

Through the harmonious collaboration of these technologies, we've crafted a comprehensive School Management App that embodies modern best practices and offers a rich user experience.

## Features

images:
![Adding_Grades](https://github.com/Mrokus95/SchoolManagmentApp/assets/123180025/e382df2d-7ce8-4b25-86c8-f2decc24f967)
![Adding_Student_By_Admin](https://github.com/Mrokus95/SchoolManagmentApp/assets/123180025/8a601a25-d4ff-4d0a-a51b-9184028b2f2b)
![Events_Student](https://github.com/Mrokus95/SchoolManagmentApp/assets/123180025/58bb1c31-dbf1-432f-866e-ab23989d4f2a)
![Grades_By_Teacher_With_Details](https://github.com/Mrokus95/SchoolManagmentApp/assets/123180025/09b72b14-cdbe-4cf6-88d4-3478141ac465)
![Lesson_Conducting](https://github.com/Mrokus95/SchoolManagmentApp/assets/123180025/c147d16b-4cb4-483d-906d-b2f16257c93e)
![Lesson_Report_Filter](https://github.com/Mrokus95/SchoolManagmentApp/assets/123180025/defc983f-4c6f-42c0-ac89-330ff9a37f08)
![New_Message](https://github.com/Mrokus95/SchoolManagmentApp/assets/123180025/852d5f92-612b-4d21-af8b-33207b2921e6)
![Shelude_Updating_By_Admin](https://github.com/Mrokus95/SchoolManagmentApp/assets/123180025/bad9ab16-ca8f-444a-b026-0fb1c782d47d)
![Sheludes_Student](https://github.com/Mrokus95/SchoolManagmentApp/assets/123180025/13740fa7-c73d-40a5-9a2f-3d95829c7946)
