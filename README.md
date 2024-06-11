# Art & Culture  

### The first social app to showcase African artists and our culture.  
<hr/>  

## Contents:  
  * [Introduction](#Introduction).
  * [Installation](#Installation).
  * [Usage examples](#Usage).
  * [API Documentation](#API-Documentation).
  * [Contributing](#Contributing).
  * [Related Projects](#Related-Projects).
  * [features](#Features).
  * [Authors](#Authors).
  * [License](#License).

## Introduction
Art & Culture is a social app that showcases African artists and our culture. It is a platform where artists can share their work and get feedback from other users. Users can also follow their favorite artists and get updates on their latest work. The app also has a feature that allows users to discover new artists and art forms. The app is built using Flask, a Python web framework, and MySQL, a relational database management system. The frontend is built using HTML, CSS, JavaScript, and jQuery. The deployed website is on [artandculture](https://artandculture.ki2kid.tech/). There is a dedicated Blog for the project at [Art & Culture Blog](https://hackernoon.com/preview/EkaK6YMgA1XSJUW8RqGx).


## Installation
To install the app, you need to have the following installed on your machine:
- Python 3.8.5 or later.
- MySQL 5.7 or later.
- Flask
- Flask-cors
- Flasgger
- sqlalchemy

To install the app, follow these steps:
1. Clone the repository to your local machine.
2. Run `setup_mysql_dev.sql` to create the database and tables.
3. Run the following to command to start the development server:
```bash
python3 -m api.v1.app # start the api server NOTE: This will start the api server on port 5004
```
> In another terminal, run the following command to start the frontend server:
```bash
python3 -m frontend.app # start the frontend server NOTE: This will start the frontend server on port 5006
```

## Usage
To use the app, open your browser and navigate to `http://localhost:5006`. You will be redirected to the landing page where you can sign up or log in if you already have an account. Once you are logged in, you can view the latest posts from artists you follow, discover new artists, view your profile, and create new posts.

## API Documentation
The API documentation is available at `http://localhost:5004/apidocs`. You can use the API documentation to learn how to interact with the API and make requests to the server.

## Contributing
To contribute to the project, follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them to your branch.
4. Push your changes to your fork.
5. Create a pull request to the main repository.

## Related Projects
- [Google Arts & Culture](https://artsandculture.google.com/)
- [Art & Culture](https://www.artandculture.com/)

## Features
The app has the following features:
- User authentication: Users can sign up and log in to the app.
- Follow artists: Users can follow their favorite artists and get updates on their latest work.
- Discover new artists: Users can discover new artists and art forms.
- Create posts: Users can create new posts and share their work with other users.
- View profile: Users can view their profile and update their information.

## Authors
Mohammed Mubarak / [Github](https://github.com/mmubarak0) / [Twitter](https://twitter.com/ki2kid)

Mbali Ramakgasha / [Github]() / [Twitter]()
