# Housing-Units DevOps
##DevOps related files for the Housing-Units REST API

###Prerequisites:
- You must have installed Docker and Docker-compose in your OS.

###Steps to run the Dockerfiles:

    cd housing-units
    sudo docker build -f api/devops/migrations/Dockerfile -t housing-units-api-migrations .
    sudo docker tag housing-units-api-migrations housing-units-api-migrations:0.1
    sudo docker build -f api/devops/worker/Dockerfile -t housing-units-api-worker .
    sudo docker tag housing-units-api-worker housing-units-api-worker:0.1
    sudo docker build -f api/devops/api/Dockerfile -t housing-units-api .
    sudo docker tag housing-units-api housing-units-api:0.1
    sudo docker build -f api/devops/nginx/Dockerfile -t housing-units-api-nginx api/devops/nginx/
    sudo docker tag housing-units-api-nginx housing-units-api-nginx:0.1
    sudo docker-compose -f api/devops/docker-compose.yml up -d