import mysql.connector
import os, time
import pika
import random
import create_database_moneda


print("start lanza_moneda...")
create_database_moneda.main()

DATABASE = "jugadas"

DATABASE_IP = str(os.environ['DATABASE_IP'])

DATABASE_USER = "root"
DATABASE_USER_PASSWORD = "root"
DATABASE_PORT=3300

time.sleep(10)

########### CONNEXIÓN A RABBIT MQ #######################

HOST = os.environ['RABBITMQ_HOST']
print("rabbit:"+HOST)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=HOST))
channel = connection.channel()

#El consumidor utiliza el exchange 'cartero'
channel.exchange_declare(exchange='cartero', exchange_type='topic', durable=True)

#Se crea un cola temporaria exclusiva para este consumidor (búzon de correos)
result = channel.queue_declare(queue="lanza-moneda", exclusive=True, durable=True)
queue_name = result.method.queue

#La cola se asigna a un 'exchange'
channel.queue_bind(exchange='cartero', queue=queue_name, routing_key="lanza-moneda")


##########################################################


########## ESPERA Y HACE ALGO CUANDO RECIBE UN MENSAJE ####

print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
	print(body.decode("UTF-8"))
	arguments = body.decode("UTF-8").split(" ")

	if (arguments[0]=="!lanza-moneda"):
		
		person = arguments[1]
		print(person)
		opcion = arguments[2]
		opc = ['cara','sello']
		aleatorio = random.randrange(0,2)
		ia= opc[aleatorio]
		print("Sale: ",ia)
		db_connection = mysql.connector.connect(user=DATABASE_USER,host=DATABASE_IP,port=DATABASE_PORT, password=DATABASE_USER_PASSWORD)
		cursor = db_connection.cursor()
		cursor.execute(f"USE {DATABASE}")
		if opcion == ia:
			print("Ganaste!...")
			cursor.execute(f'''UPDATE cuenta SET ganadas = ganadas + 1 -> WHERE member="{person}";''')
		
		else: 
			print("Perdiste!...")
			cursor.execute(f'''UPDATE cuenta SET perdidas = perdidas + 1 -> WHERE member="{person}";''')

		cursor.execute(f'''COMMIT;''')

			########## PUBLICA EL RESULTADO COMO EVENTO EN RABBITMQ ##########
		print("send a new message to rabbitmq: "+result)
		channel.basic_publish(exchange='cartero',routing_key="discord_writer",body=result)

	if (arguments[0]=="!resultados"):
		person = arguments[1]
		print(person)
		db_connection = mysql.connector.connect(user=DATABASE_USER,host=DATABASE_IP,port=DATABASE_PORT, password=DATABASE_USER_PASSWORD)
		cursor = db_connection.cursor()
		cursor.execute(f"USE {DATABASE}")
		cursor.execute(f'''SELECT member,ganadas,perdidas FROM cuenta WHERE member="{person}";''')
		for (member, ganadas,perdidas) in cursor:
			result="{} tienes {} ganadas y {} perdidas".format(member,ganadas,perdidas)
			print(result)
			########## PUBLICA EL RESULTADO COMO EVENTO EN RABBITMQ ##########
			print("send a new message to rabbitmq: "+result)
			channel.basic_publish(exchange='cartero',routing_key="discord_writer",body=result)

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()