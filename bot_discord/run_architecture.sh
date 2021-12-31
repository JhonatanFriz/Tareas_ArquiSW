docker-compose -f docker-compose.yml up -d --build rabbitmq

docker-compose -f docker-compose.yml up -d --build birthday_database

docker-compose -f docker-compose.yml up -d --build moneda_database

DATABASE_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' birthday_database) 

DATABASE_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' moneda_database) 

echo $DATABASE_IP

DATABASE_IP=$DATABASE_IP docker-compose -f docker-compose.yml up -d --build birthday_manager

DATABASE_IP=$DATABASE_IP docker-compose -f docker-compose.yml up -d --build lanza_moneda

docker-compose -f docker-compose.yml up -d --build discord_listener