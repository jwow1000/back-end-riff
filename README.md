
# [RIFF]


[Backend for the RIFF application]



## Table of Contents

- [Project Overview](#project-overview)
- [Tecknology](#technology)
- [Features](#features)
- [Installation](#installation)
- [Contributing](#contributing)
- [Resources](#resources)
- [Contact](#contact)

## Project Overview

Riff serves as a dedicated space for artists to connect, collaborate, and innovate. By harnessing the power of collective creativity, Riff empowers users to explore diverse perspectives and create compelling art together.


Riff is a platform designed to facilitate collaboration among artists and enable crowd-sourced art creation. With Riff, users can engage in a dynamic creative process, contributing to and enhancing each other's work through threaded comments associated with individual posts.

## Technology

- **Python**: Backend development language.
- **Django**: Web framework for building APIs and web applications.
- **Django REST Framework (DRF)**: Toolkit for building Web APIs in Django.
- **PostgreSQL**: Relational database management system for data storage.

## Features
- **User Authentication**: Implement secure user authentication and authorization mechanisms.
- **Artwork Management**: CRUD operations for managing artwork submissions by users.
- **Feed Generation**: Generate personalized feeds for users based on their favorited users.
- **Collaborative Posting**: Users can create posts and others artists can contribute, fostering a collaborative environment for artistic expression.
- **Threaded Comments**: Each post supports threaded comments, allowing users to provide feedback, suggestions, and additions to specific aspects of the artwork.
- **Version Control**: Riff enables users to explore multiple iterations of a piece of art, facilitating iterative refinement and evolution of creative ideas.

## Installation

Provide step-by-step instructions on how to install your Django backend. Include any prerequisites and dependencies that need to be installed beforehand.

`$ pipenv shell`

`$ pipenv install django` 

`$ psycopg2-binary django-mptt Pillow`

`$ psql `

`$ psql -f create-db.sql`

`$ python manage.py makemigrations`

`$ python manage.py migrate`

`$ python manage.py createsuperuser`

`$ python manage.py runserver`

## Contributing

If you want to contribute to this project, please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/banana`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add some bananas'`)
5. Push to the branch (`git push origin feature/banana`)
6. Create a new Pull Request

## Resources

1. https://django-mptt.readthedocs.io/en/latest/models.html


## Contact

 Grace Clower- [Git Hub](https://github.com/geclower) - [LinkedIn](https://www.linkedin.com/in/grace-clower/)

Front-End Project Link: [Riff](https://github.com/jwow1000/front-end-riff)

