# Retos y labs TET
 Retos y laboratorios de Big Data, realizado por Santiago Gonzalez Rodriguez

# Lab 6 y reto 5
Empezando con el lab 6, se creo un S3 como fue solicitado 
![image](https://github.com/SantiagoGonzalezR/Retos-y-labs-TET/assets/68928481/3ffaa698-69f4-44e4-a2b3-315aa5648019)

Despues de esto se crea la llave, la cual llame emr-key.pem, esta se encuentra dentro de Access Keys

Ahora, se crea el EMR, con animo de que no extienda la guia, la crearemos directamente desde el CLI para mostrar el reto, pero dejare constancia de que se crearon algunos EMR antes de la ejecucion del CLI:
![image](https://github.com/SantiagoGonzalezR/Retos-y-labs-TET/assets/68928481/57f60540-2321-4529-ab01-14dc7a9fde8b)

Para iniciar debemos instalar el awscli dentro de nuestra maquina, esto se hace de la siguiente manera:
```sh
pip install awscli
```
Despues configuramos las credenciales y la configuracion de la sesion de AWS:
```sh
aws configure
AWS Access Key ID [None]: <Access key>
AWS Secret Access Key [None]: <Secret Access Key>
Default region name [None]: <La region seleccionada en el S3, en este caso es "us-east-1">
Default output format [None]:
```
Esto crea una carpeta llamada .aws en la carpeta root, donde encontraremos lo siguiente:
![image](https://github.com/SantiagoGonzalezR/Retos-y-labs-TET/assets/68928481/385ad259-37b0-4bd1-94a5-836dfcf1d0f1)

Como nuestro AWS es de educacion, nos falta un dato dentro de las credenciales, asi que entraremos a esta con un editor de texto e insertamos el AWS session token, el cual se encuentra de la siguiente manera:
![image](https://github.com/SantiagoGonzalezR/Retos-y-labs-TET/assets/68928481/46ea40cc-fcf7-48be-af89-73e2a3092c7f)

Podremos revisar si la conexion esta realizada si corremos lo siguiente:
```sh
aws s3 ls
```
Y no suelta el/los s3 que tenemos creados:
![image](https://github.com/SantiagoGonzalezR/Retos-y-labs-TET/assets/68928481/2e9c08e7-66ea-4f82-95d0-2c8ac86e1018)

Ahora, a crear el EMR, para esto necesitamos correr lo siguiente:
```sh
aws emr create-cluster --name cli-emr --release-label emr-6.10.0 --instance-type m4.large --instance-count 3 --log-uri s3://santiago-lab-emr/logs --use-default-roles --ec2-attributes KeyName=emr-key,SubnetId=subnet-054cf2ee6f1206990 --no-termination-protected
```
Esto crea el cluster con unas especificaciones diferentes a las solicitadas en el lab #6, pero con las que se fueron solicitadas no me funcionaba el pip3 y el mrjob no funcionaba a la hora de ejecutar las cosas en el cluster, ahora esperamos unos minutos mientras inicializa.  
Despues de que inicialize corremos el siguiente comando:
```sh
ssh -i emr-key.pem hadoop@<publicDNS>
```
El "Public DNS" lo sacamos del DNS publico de la instancia de EC2 que quedo como primaria, y lo corremos despues de editar los permisos del security group para permitir la conexion ssh.  
![image](https://github.com/SantiagoGonzalezR/Retos-y-labs-TET/assets/68928481/938066e1-637c-439e-bd4b-a827264849bf)

Y con eso concluimos la creacion del cluster EMR por medio del CLI.
##Laboratorio 7 y reto 6
Ahora vamos a realizar el laboratorio 7 antes de realizar el reto 6:  
Primero instalemos git en la maquina para clonar el repositorio del laboratorio:
```sh
 sudo yum install git
 sudo git clone https://github.com/ST0263/st0263-2023-1
 ```
 Entramos a la carpeta que contiene el codigo a ejecutar
 ```sh
 cd st0263-2023-1/Laboratorio\ N6-MapReduce/wordcount/
 ```
 Debido a un problema de ejecucion en el codigo de wordcount-local.py, haremos una modificacion para que convierta las mayusculas en minusculas:
 ```sh
 sudo nano wordcount-local.py
 ```
 ```python
 import os
import sys
import glob
import codecs

inputdir = "."

if len(sys.argv) >= 2:
    inputdir = sys.argv[1]

def processdir(dir):
    dirList = glob.glob(dir)
    wordcount = {}
    for f in dirList:
        wordcountfile(f, wordcount)
    for w in wordcount:
        print(w, wordcount[w])

def wordcountfile(f, wordcount):
    file = codecs.open(f, "r", "utf-8")
    for word in file.read().split():
        word = word.lower() #Nueva linea para convertir todo a minusculas
        if word not in wordcount:
            wordcount[word] = 1
        else:
            wordcount[word] += 1
    file.close()
    return wordcount

processdir(inputdir)
 ```
 Y para finalizar corremos los comandos solicitados (El comando de ejecucion de wordcount-local esta modificado, el que nos fue dado pone problemas de permisos a la hora de crear el archivo)
 ```sh
 python wordcount-local.py /home/hadoop/st0263-2023-1/datasets/gutenberg-small/*.txt | sudo tee salida-serial.txt > /dev/null
 more salida-serial.txt
```
Y en consola deberia aparecer lo siguente:  
![image](https://github.com/SantiagoGonzalezR/Retos-y-labs-TET/assets/68928481/38c1b2b8-13b7-4b3a-b1ee-6b1ebd8d162b)

Corremos el codigo de python con mrjob despues de haberlo instalado, con las especificaciones con las que fue creado, ya estan python3 y pip3 actualizados
```sh
sudo pip3 install mrjob
python wordcount-mr.py /home/hadoop/st0263-2023-1/datasets/gutenberg-small/*.txt
```
Y obtenemos el siguiente output:
![image](https://github.com/SantiagoGonzalezR/Retos-y-labs-TET/assets/68928481/03f17825-ccf7-41c0-8e2b-7aad0901cb9f)

Ahora hagamos el reto de ejecutarlo en los clusters:  
Primero creamos la carpeta de admin por consola (si se deberia crear por medio de Hue, por algun motivo no me permite la conexion)
```sh
hdfs dfs -mkdir /user/admin/
```
Despues copiamos el dataset al EMR
```sh
hdfs dfs -copyFromLocal /home/hadoop/st0263-2023-1/datasets/ /user/admin/
```
Y por ultimo corremos el comando para ejecutar el wordcount-mr.py en el cluster
```sh
python wordcount-mr.py hdfs:///user/admin/datasets/gutenberg-small/*.txt -r hadoop --output-dir hdfs:///user/admin/result3
```
Deberiamos obtener una respuesta de que las respuestas estan en la carpeta "result3", corremos el comando -cat para leer el documento y deberia salir lo siguiente:
```sh
hdfs dfs -cat /user/admin/result3/part-00000 #Puede ser 00000, 00001 o 00002#
```
![image](https://github.com/SantiagoGonzalezR/Retos-y-labs-TET/assets/68928481/77d98df5-81e1-4d22-b217-013cb967f511)
Con esto se da por concluido el laboratorio N7 y seguimos a los retos de programacion
# Retos de programacion en Map/Reduce
Todos los codigos ejecutados estaran adjuntos en el github bajo diferentes carpetas
## Punto 1, DIAN
