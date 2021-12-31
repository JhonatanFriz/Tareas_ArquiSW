import pika, sys, os
import pageviewapi.period
#import time

def main():
    #Conexión al servidor RabbitMQ   
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    #Nos aseguramos que existe una cola 'consumidor_vistas'
    channel.queue_declare(queue='consumidor_vistas')

    #Recibir mensajes de la cola es más complejo. Funciona suscribiendo una función de devolución de llamada ("callback"). Cada vez que recibimos un mensaje, esta función "callback" es llamada por la libreria Pika. En nuestro caso, esta función imprimirá en la pantalla el contenido del mensaje.
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        #time.sleep(body.count(b'.'))
        vistas = pageviewapi.period.sum_last('en.wikipedia', body.decode(), last=30,
                            access='all-access', agent='all-agents')
        print(" [x] Numero de vistas en los ultimos 30 dias: %d" %vistas)
        print(" [x] Done")

    channel.basic_consume(queue='consumidor_vistas', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

    #Bocle infinita
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)





