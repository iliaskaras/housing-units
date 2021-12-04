# Housing-Units API
### A REST API written with the FastAPI Web Framework

A containerized FastAPI Rest API that provides CRUD and data ingestion endpoints for importing and managing the 
Housing New York Units by Building dataset.

## Description

##### Showcasing:
1. Authentication via JWT
2. Authorization via user groups (Data ingestion can only performed by admins) - Simple implementation.
3. Error handling
4. CRUD endpoints
5. Unit, Integration and Functional tests
6. SQLAlchemy Async and Sync integration
7. Celery for async tasks with Redis as broker.
8. Dependency-Injection python package implementation.

### POSTMAN:
You can import the Housing Units.postman_collection.json file into your Postman and try out all the available endpoints.

### Prerequisites

* Have Docker and docker-compose installed in your OS.
* Linux.
* Have the ports used in the docker-compose free.

### Deploying the REST API

* Download the repository.
* Change directory to **housing-units** where the Makefile is located.
* Run the docker-compose with the Makefile command (warning: you might be required to type your sudo code):
```
make deploy-local
```
* This will run the following:
    * ****PostgreSQL container****
    * ****Database migrations**** where 2 users will be created:
        * email: customer_user@customer.com | password: 123456
        * email: ****admin_user@admin.com**** | password: 123456
    * The ****Redis****
    * The ****The Worker****
    * The ****The REST API****
    * The ****Flower****
    * The ****Nginx****

### Testing the REST API

* A collection of Postman ****Housing Units.postman_collection.json**** requests is provided under the **housing-units** directory, import and:
    * Authenticate via the **login** endpoint using the ****admin_user@admin.com****.
    * Add the returned ****'access_token'**** to the rest of the endpoints inside the bearer token.

* Run unit, integration and functional tests at once with the Makefile command: 
```
make run-tests
```

## Version History

* 0.1
    * Initial Release
