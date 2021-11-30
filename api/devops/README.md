# Housing-Units DevOps
##DevOps related files for the Housing-Units REST API

###Prerequisites:
- You must have installed Docker and Docker-compose in your OS.

###Steps to run the Dockerfiles:

1. cd to the housing-units directory.
2. docker build -f api/devops/migrations/Dockerfile -t housing-units-api-migrations .
3. docker tag housing-units-api-migrations housing-units-api-migrations:0.1
4. docker build -f api/devops/worker/Dockerfile -t housing-units-api-worker .
5. docker tag housing-units-api-worker housing-units-api-worker:0.1
6. docker build -f api/devops/api/Dockerfile -t housing-units-api .
7. docker tag housing-units-api housing-units-api:0.1
8. docker-compose -f api/devops/docker-compose.yml up -d