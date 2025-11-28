# Orders Microservice (Django + AWS + Docker)

Microservicio de órdenes para Provesi.  
Corre en **Django + DRF**, desplegado en **Docker** dentro de una **EC2**, usando **PostgreSQL en AWS RDS** como base de datos.

---

## 1. Requisitos

### Infraestructura
- 1 instancia **EC2 Ubuntu 22.04**
- 1 instancia **RDS PostgreSQL**
- Ambas en la misma VPC

### Software en EC2
```bash
sudo apt update
sudo apt install -y docker.io git
sudo systemctl enable --now docker
```

## 2. Clonar el repositorio

git clone https://github.com/tu_repo/orders-ms.git
cd orders-ms


## 3. Variables de entorno necesarias

```bash
DB_NAME="orders_db"
DB_USER="postgres"
DB_PASSWORD="12345678"
DB_HOST="orders-db.xxxxxx.us-east-1.rds.amazonaws.com"
DB_PORT="5432"
SECRET_KEY="super-secreto-123"
DEBUG="False"
PRODUCTS_MS_URL="http://172.31.26.247:8000"
```


## 4. Construir la imagen de docker
docker build -t orders-ms-image .

## 5. Ejecutar el contenedor

```bash
docker run -d \
  --name orders-ms \
  -e DB_NAME=$DB_NAME \
  -e DB_USER=$DB_USER \
  -e DB_PASSWORD=$DB_PASSWORD \
  -e DB_HOST=$DB_HOST \
  -e DB_PORT=$DB_PORT \
  -e SECRET_KEY=$SECRET_KEY \
  -e DEBUG=$DEBUG \
  -e PRODUCTS_MS_URL=$PRODUCTS_MS_URL \
  -p 8000:8000 \
  --restart unless-stopped \
  orders-ms-image
```

## 6. Crear migrations

```bash
docker exec -it orders-ms bash
python manage.py makemigrations orders
python manage.py migrate
exit
```

## 7. probar el servicio

```bash
curl http://127.0.0.1:8000/orders/
``` 
o

```bash
curl http:<ip-pública>:8000/orders/ 
``` 

## 8. Reiniciar despues de apagar el contenedor

```bash
docker start orders-ms

```

## 9. Detener el contenedor

```bash
docker stop orders-ms
``` 

## 10. Eliminar el contenedor

```bash
docker rm orders-ms
``` 

