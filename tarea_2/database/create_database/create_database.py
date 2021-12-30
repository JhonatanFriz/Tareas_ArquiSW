import mysql.connector
import os, time

def create_database(db_connection,db_name,cursor):
	cursor.execute(f"CREATE DATABASE {db_name};")
	cursor.execute(f"COMMIT;")
	cursor.execute(f"USE {db_name};")
	
	# Tabla news
	cursor.execute('''CREATE TABLE news (
		id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        title TEXT,
        date DATE,
		url TEXT NOT NULL, 
		media_outlet VARCHAR(25),
		category VARCHAR(15)
        );''')

	cursor.execute("SET GLOBAL time_zone = 'UTC';")
	cursor.execute("SET SESSION time_zone = 'UTC';")

	cursor.execute("COMMIT;") 

def insert_data(cursor):
    print("insert")
    cursor.execute('''INSERT INTO news (title,date,url,media_outlet,category) VALUES
    ('Unicef pide trabajar por la recuperación de los aprendizajes en la enseñanza parvularia', '2021-12-03', 'https://www.eldinamo.cl/educacion/2021/12/03/unicef-pide-trabajar-por-la-recuperacion-de-los-aprendizajes-en-la-ensenanza-parvularia/', 'El Dinamo', 'educacion'),
    ('Un desastre climático en cámara lenta: la propagación de tierras estériles','2021-12-04' ,'https://www.nytimes.com/es/2021/12/04/espanol/brasil-desertificacion.html', 'The New York Times', 'ecologia'),
    ('Seremi de Salud confirma primer caso de variante Ómicron en Chile', '2021-12-04', 'https://www.lacuarta.com/cronica/noticia/seremi-de-salud-confirma-primer-caso-de-variante-omicron-en-chile/XUPHUZKYPNAYHK5Q5R3KAQP3WM/', 'La Cuarta', 'salud'),
    ('Colo Colo y la UC aportan nuevos nombres a la Roja: Lasarte convoca a Arriagada y Montes', '2021-12-05', 'https://www.latercera.com/el-deportivo/noticia/colo-colo-y-la-uc-aportan-nuevos-nombres-a-la-roja-lasarte-convoca-a-arriagada-y-montes/M2BVJ62L6BBVTFPWXCY5ZDANFY/', 'La Tercera', 'deporte'),
    ('Más de 275 mil postulantes: Mineduc realiza balance tras rendición de Prueba de Transición', '2021-12-10', 'https://www.eldinamo.cl/educacion/2021/12/10/mineduc-realiza-balance-tras-rendicion-de-prueba-de-transicion/', 'El Dinamo', 'educacion'),
    ('Alexis Sánchez y Arturo Vidal ya tienen rival: así quedaron los cruces de octavos de la Champions', '2021-12-13', 'https://www.lacuarta.com/deportes/noticia/alexis-sanchez-y-arturo-vidal-ya-tienen-rival-asi-quedaron-los-cruces-de-octavos-de-la-champions/4DR6OGMGWFH7HEN72PMIWLCDQY/', 'La Cuarta', 'deporte');
    ''')
    cursor.execute("COMMIT;") 

#######################
DATABASE = "sun"

DATABASE_IP = str(os.environ['DATABASE_IP'])

DATABASE_USER = "root"
DATABASE_USER_PASSWORD = "root"
DATABASE_PORT=3306

not_connected = True

while(not_connected):
	try:
		print(DATABASE_IP,"IP")
		db_connection = mysql.connector.connect(user=DATABASE_USER,host=DATABASE_IP,port=DATABASE_PORT, password=DATABASE_USER_PASSWORD)
		not_connected = False

	except Exception as e:
		time.sleep(3)
		print(e, "error!!!")
		print("can't connect to mysql server, might be intializing")
		
cursor = db_connection.cursor()

try:
	cursor.execute(f"USE {DATABASE}")
	print(f"Database: {DATABASE} already exists")
except Exception as e:
    create_database(db_connection,DATABASE,cursor)
    insert_data(cursor)
    print(f"Succesfully created: {DATABASE}")
