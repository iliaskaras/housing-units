help:
	@echo " "
	@echo "Targets:"
	@echo " "
	@echo "- make deploy-local"
	@echo " "

deploy-local:
		@echo "=============================== Start Local Deployment ==============================="
		@echo "=================================== Requirements ====================================="
		@echo "1. Ensure you have Docker installed and service up and running in your system."
		@echo "2. Ensure you have Docker Compose installed and with permissions to execute it."
		sudo docker build -f api/devops/migrations/Dockerfile -t housing-units-api-migrations .
		sudo docker tag housing-units-api-migrations housing-units-api-migrations:0.1
		sudo docker build -f api/devops/worker/Dockerfile -t housing-units-api-worker .
		sudo docker tag housing-units-api-worker housing-units-api-worker:0.1
		sudo docker build -f api/devops/api/Dockerfile -t housing-units-api .
		sudo docker tag housing-units-api housing-units-api:0.1
		sudo docker-compose -f api/devops/docker-compose.yml up -d

down-services:
		@echo "======================= Stopping Local Deployment Running Services==============================="
		sudo docker-compose -f api/devops/docker-compose.yml down