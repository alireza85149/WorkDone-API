# WorkDone API

WorkDone API is a production-inspired freelancing platform backend built with Django and Django REST Framework.
It connects employers with freelancers through a complete project lifecycle, from project creation and proposal submission to contract management, work delivery, and reviews.
The project is designed to demonstrate modern backend development practices, including RESTful API design, authentication, authorization, relational database modeling, and scalable application architecture.


## Features:

* JWT Authentication (Register, Login, Refresh Tokens)
* Role-based Authorization (Employer, Freelancer, Admin)
* Freelancer & Employer Profiles
* Project Posting and Management
* Proposal/Bidding System
* Contract Management
* Work Submission & Delivery
* Review & Rating System
* Search, Filtering & Pagination
* File Upload Support
* Notification System
* Interactive API Documentation (Swagger/OpenAPI)
* Dockerized Development Environment


## Tech Stack

* Python
* Django
* Django REST Framework
* PostgreSQL
* Redis
* Celery
* Docker
* Git & GitHub
* JWT Authentication
* Swagger / drf-spectacular


## Project Goals

* Build a production-style REST API.
* Follow clean and maintainable architecture.
* Apply real-world backend design patterns.
* Demonstrate secure authentication and authorization.
* Practice scalable database design using PostgreSQL.
* Showcase professional development workflows with Git and Docker.


## Planned Architecture

Client (React / Flutter / Mobile)

            │

        REST API

            │

 Django REST Framework

            │

 PostgreSQL   Redis

            │        │

         Celery Workers
```


## Learning Objectives

This project focuses on gaining practical experience with:

* Backend API development
* Database design and optimization
* Authentication & permissions
* Docker containerization
* Asynchronous background tasks
* API documentation
* Professional Git workflows
* Production-ready backend architecture

> **Note:** This project is being developed as a portfolio project to simulate the architecture and workflow of a real-world freelancing platform while following industry best practices.
