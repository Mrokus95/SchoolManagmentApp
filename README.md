# SchoolManagmentApp

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

### AWS RDS (Amazon Relational Database Service) ![aws rds](https://github.com/Mrokus95/SchoolManagmentApp/assets/59625513/93a6776b-0dfb-4d21-8cb7-15af08644212)



We integrated AWS RDS to host our database in the Amazon cloud. This allowed us to work collaboratively on the same dataset while gaining experience in cloud-based services integration. The use of Amazon RDS enables efficient and reliable data storage.

### PostgreSQL Database ![postgreSQL](https://github.com/Mrokus95/SchoolManagmentApp/assets/59625513/017d3d41-b9bd-4c05-b5c7-8cd1e32e5efc)

To surpass the limitations of SQLite and enhance our relational database capabilities, we migrated to PostgreSQL. This allowed us to work with larger datasets and practice handling more complex database interactions. 

### HTML5, CSS, JS, and Bootstrap ![html5-logo png](https://github.com/Mrokus95/SchoolManagmentApp/assets/59625513/78447f01-ef70-44ce-b7d7-e10729e3c4a0) ![js](https://github.com/Mrokus95/SchoolManagmentApp/assets/59625513/0c875413-b287-4950-8d9f-d4daeb87346f) ![css3](https://github.com/Mrokus95/SchoolManagmentApp/assets/59625513/be020416-3f50-4d2b-a3e0-85847c5e3312) ![bootstrap](https://github.com/Mrokus95/SchoolManagmentApp/assets/59625513/16bd8ee7-c4b9-4125-a6c1-34aeeb83c5d0)

For the frontend, we leveraged HTML5, CSS3, JavaScript, and Bootstrap5. These technologies collectively allowed us to design and develop a responsive, user-friendly, and visually appealing user interface.

### Python and Django ![python](https://github.com/Mrokus95/SchoolManagmentApp/assets/59625513/b82413c4-2b4c-4c82-a06d-b0ba5cdeebfe) ![django](https://github.com/Mrokus95/SchoolManagmentApp/assets/59625513/6cb9996c-5ab0-4797-a422-1c8894d2b7de)


The backend of the project was developed using Python 3.12 and Django 4.2. Python's versatility and readability empowered us to create robust backend logic. Django's high-level framework facilitated rapid development, efficient database management, and seamless integration of various components.

Through the harmonious collaboration of these technologies, we've crafted a comprehensive School Management App that embodies modern best practices and offers a rich user experience.

## Features

The project was developed with the purpose of refining skills in the Django framework. Its goals included encompassing a diverse array of functionalities while staying closely aligned with market demands and venturing beyond the conventional scope of such projects. Recognizing a potential need, we identified an opportunity for a school platform that facilitates information dissemination and communication among all entities within the school community. The result of our endeavor is precisely this project.

Functions and permissions vary depending on the account type. The website offers slightly different capabilities for teachers, students, and parents.

### UserApp:

After logging in as an admin, we have the capability to create new user accounts by assigning them various pertinent attributes. For instance, while setting up a student account, in addition to the usual particulars, we are required to choose a class and designate a parent. Conversely, for a teacher account, it is imperative to specify a subject. Furthermore, each profile is afforded the option to upload a photograph. This is also the section responsible for user authentication. Each user has the authority to edit crucial information such as email address or password.
####Adding student by adminn:
![Adding_Student_By_Admin](https://github.com/Mrokus95/SchoolManagmentApp/assets/123180025/8a601a25-d4ff-4d0a-a51b-9184028b2f2b)

### TeacherApp:

After login as admin , we can add new users by assigning them all the relevant attributes. For instance, when creating a student account, aside from standard details, we need to select a class and a parent. Conversely, for a teacher, specifying a subject is essential. Each profile also has the option to add a photo.To również miejsce, kóre odpowiada za logowanie użytkowników. Każdy z nich może edytować kluczowe dane, jak adres email czy hasło.
####Adding grades:
![Adding_Grades](https://github.com/Mrokus95/SchoolManagmentApp/assets/123180025/e382df2d-7ce8-4b25-86c8-f2decc24f967)
####Adding lesson report:
![Lesson_Conducting](https://github.com/Mrokus95/SchoolManagmentApp/assets/123180025/c147d16b-4cb4-483d-906d-b2f16257c93e)
Filtering reports:
![Lesson_Report_Filter](https://github.com/Mrokus95/SchoolManagmentApp/assets/123180025/defc983f-4c6f-42c0-ac89-330ff9a37f08)

### MessagesApp:

Through the messaging panel, we facilitate communication among distinct entities. Within this panel, messages are categorized into three sections: Inbox, Sent, and Important. We can reply to messages, mark them as important, or delete them. When a user receives a new message, they will see a special notification icon until the message is read.
####Create new message:
![New_Message](https://github.com/Mrokus95/SchoolManagmentApp/assets/123180025/10f2ce30-ca29-4249-931f-ca060775ffd9)
####Inbox:
![Messages_Inbox](https://github.com/Mrokus95/SchoolManagmentApp/assets/123180025/d37fcfe1-1198-466e-83ee-c7066ffde6be)

### GradesApp:

The application allows for navigation through grades. When a student is logged in, they select a semester and view their grades categorized by subjects. Similarly, a parent, if associated with more than one student, will see a separate table for each of them. On the other hand, a teacher must choose not only the semester but also the subject and class. As a result, they will see a list of students with grades for that specific subject. Each user type can click on a grade to reveal a tooltip with details about the author, date, and a brief description
####Viewing grades:
![Grades_By_Teacher_With_Details](https://github.com/Mrokus95/SchoolManagmentApp/assets/123180025/09b72b14-cdbe-4cf6-88d4-3478141ac465)

### EventsApp:

Each student and parent can browse through events associated with their class or their child's class, which are additionally marked with a red exclamation mark if they haven't been viewed yet. They have the ability to filter these events based on subjects, lessons, date ranges, or view all at once. By clicking on an event, they can read its details and navigate to the corresponding report.
####Viewing events for student:
![Events_Student](https://github.com/Mrokus95/SchoolManagmentApp/assets/123180025/58bb1c31-dbf1-432f-866e-ab23989d4f2a)

###  CalendarApp:

This section is responsible for displaying the schedule. We select a class, and then we can iterate through upcoming weeks. Additionally, the admin panel enables adding lessons from this view. The schedule itself verifies the availability of a specific teacher and classroom on a given day and time. The real-time form adjusts the options available in subsequent fields based on prior selections. It prevents creating conflicting lessons by considering the availability of subject-specific teachers, other students' lessons, and the availability of classrooms. Lessons can be added in two ways—by making permanent schedule changes or by introducing updates for specific weeks. Furthermore, a mechanism sends a message about introduced changes to each individual affected by a given lesson.
####Auto message after changed lesson:
![Changed_Auto_Message](https://github.com/Mrokus95/SchoolManagmentApp/assets/123180025/90ddf414-6f4b-49cc-a349-9b532024e065)
####Shedule:
![Sheludes_Student](https://github.com/Mrokus95/SchoolManagmentApp/assets/123180025/13740fa7-c73d-40a5-9a2f-3d95829c7946)
####Adding lesson:
![Shelude_Updating_By_Admin](https://github.com/Mrokus95/SchoolManagmentApp/assets/123180025/bad9ab16-ca8f-444a-b026-0fb1c782d47d)

## Authors:


