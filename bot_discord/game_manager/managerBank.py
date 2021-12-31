import mysql.connector
import os, time
import pika
import create_databasegame
import random

print("start cuenta manager...")
create_databasegame.main()

DATABASE = "bank"

DATABASE_IP = str(os.environ['DATABASE_IP'])

DATABASE_USER = "root"
DATABASE_USER_PASSWORD = "root"
DATABASE_PORT=3306

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
result = channel.queue_declare(queue="saldo", exclusive=True, durable=True)
queue_name = result.method.queue

#La cola se asigna a un 'exchange'
channel.queue_bind(exchange='cartero', queue=queue_name, routing_key="saldo")


##########################################################


########## ESPERA Y HACE ALGO CUANDO RECIBE UN MENSAJE ####

print(' [*] Waiting for messages. To exit press CTRL+C')
#!saldo
#!cachipun cara 50
def callback(ch, method, properties, body):
	print(body.decode("UTF-8"))
	arguments = body.decode("UTF-8").split(" ")

	if (arguments[0]=="!saldo"):
		person = arguments[1]
		print(person)
		db_connection = mysql.connector.connect(user=DATABASE_USER,host=DATABASE_IP,port=DATABASE_PORT, password=DATABASE_USER_PASSWORD)
		cursor = db_connection.cursor()
		cursor.execute(f"USE {DATABASE}")
		cursor.execute(f'''SELECT member,saldo FROM cuentas WHERE member="{person}";''')
		for (member, saldo) in cursor:
			result="{} te queda {} coins".format(member,saldo)
			print(result)
						########## PUBLICA EL RESULTADO COMO EVENTO EN RABBITMQ ##########
			print("send a new message to rabbitmq: "+result)
			channel.basic_publish(exchange='cartero',routing_key="discord_writer",body=result)

	

	if (arguments[0]=="!lanza_moneda"):
		person = arguments[1]
		print(person)
		opcion = arguments[2]
		apuesta = arguments[3]
		opc = ['cara', 'sello']
		aleatorio = random.randrange(0, 2)
		bot = opc[aleatorio]

		print("Sale: ", bot)
		db_connection = mysql.connector.connect(user=DATABASE_USER,host=DATABASE_IP,port=DATABASE_PORT, password=DATABASE_USER_PASSWORD)
		cursor = db_connection.cursor()
		cursor.execute(f"USE {DATABASE}")
		if opcion == bot:
			print("Ganaste!")
			cursor.execute(f'''UPDATE cuentas SET saldo = saldo + apuesta -> WHERE member = person");''')

		else:
			print("Perdiste!")
			cursor.execute(f'''UPDATE cuentas SET saldo = saldo - apuesta -> WHERE member = person");''')
		cursor.execute(f'''COMMIT;''')


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()