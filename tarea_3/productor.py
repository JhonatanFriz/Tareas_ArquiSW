#!/usr/bin/env python
import pika
import sys

#Nuestra tarea pasada como argumento
arg = input("Busqueda en wikipedia: ")

#Conexión al servidor RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

#Creación de la cola
channel.queue_declare(queue='consumidor_datos')
channel.queue_declare(queue='consumidor_vistas')

#Publicación del mensaje
channel.basic_publish(exchange='',
                      routing_key='consumidor_datos',
                      body=arg)

channel.basic_publish(exchange='',
                      routing_key='consumidor_vistas',
                      body=arg)

print(" [x] Sent %r" % arg)

connection.close()