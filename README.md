# Coffee Shop Full Stack

## Full Stack Nanodegree

### Auth0 account

```
AUTH0_DOMAIN = 'coffeshopapp.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'drinks'
```

> :warning: I DID updated the POSTman collection with both `barista` and `manager` accounts, the thing is that the token does expire, so I've created two dummy accounts on my Auth0 profile, both of them are verified and functional.

#### Manager account
```
User: manager@coffe.com
password: manager123!
```
#### Barista account
```
User: barista@coffe.com
password: barista123!
```

### POSTman
* Exported collection with configured tokens can be found at: `/backend/Coffe Shop Full Stack.postman_collection.json`



1. [`./backend/`](./backend/README.md)
2. [`./frontend/`](./frontend/README.md)

## About the Stack

We started the full stack application for you. It is desiged with some key functional areas:

### Backend

* Added Auth0 functionalities
* Implemented RESTful endpoints
* Implemented error handlers
* I've used [Pycodestyle](https://github.com/PyCQA/pycodestyle) to enforce python code style
 ```pycodestyle is a tool to check your Python code against some of the style conventions in PEP 8.```

The `./backend` directory contains a partially completed Flask server with a pre-written SQLAlchemy module to simplify your data needs. You will need to complete the required endpoints, configure, and integrate Auth0 for authentication.

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

* Added the Auth0 variables on `environment.ts` file
* Guarantee that the frontend can be launched upon an `ionic serve` command and the login/token retrieval are functional

The `./frontend` directory contains a complete Ionic frontend to consume the data from the Flask server. You will only need to update the environment variables found within (./frontend/src/environment/environment.ts) to reflect the Auth0 configuration details set up for the backend app. 

[View the README.md within ./frontend for more details.](./frontend/README.md)
