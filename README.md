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
## Punto 1, Empleados
A. Salario Promedio por Sector Economico  
El output consiste en: El sector economico, el promedio del salario
![1a](https://github.com/SantiagoGonzalezR/Retos-y-labs-TET/assets/68928481/a5868bb7-29cf-44ba-9828-f5994eadd003)

B. Salario Promedio por Empleado  
El output consiste en: ID del empleado, el promedio del salario
![1b](https://github.com/SantiagoGonzalezR/Retos-y-labs-TET/assets/68928481/7bf05046-fab1-43c4-8a33-74a33a561d33)

C. Cantidad de Sectores Economicos por Empleado  
El output consiste en: ID del empleado, la cantidad de sectores economicos  
![1c](https://github.com/SantiagoGonzalezR/Retos-y-labs-TET/assets/68928481/068e93e0-9487-42e0-9f49-36efe29db98c)
## Punto 2, Empresas
A. Dias de menor y mayor valor  
El output consiste en: El nombre de la empresa, el dia de menor valor para sus acciones y el dia de mayor valor para sus acciones
![2a](https://github.com/SantiagoGonzalezR/Retos-y-labs-TET/assets/68928481/3fa251e8-fc0a-469a-b8ca-2106de1638ec)
B. Acciones que suben o mantienen estables  
El output consiste en: El nombre de la empresa, la indicacion de como se comportan sus acciones
![2b](https://github.com/SantiagoGonzalezR/Retos-y-labs-TET/assets/68928481/a887bd41-e885-439d-80d9-faa88ed21019)
C. Dia Negro  
El output consiste en: La fecha del "Dia negro", el precio mas bajo de la accion (En el map reduce lo puse como un contador, no me funcionaba conseguir el valor de la accion)
![2c](https://github.com/SantiagoGonzalezR/Retos-y-labs-TET/assets/68928481/a0907296-8743-4c79-b079-58e7a5ceb759)
## Punto 3, Peliculas
A. Numero de peliculas por usuario, promedio del rating  
El output consiste en: la ID del usuario, la puntuacion promedio, el conteo de ratings que han hecho
![3a](https://github.com/SantiagoGonzalezR/Retos-y-labs-TET/assets/68928481/3f2ddb37-16d7-4a9b-a254-866d1d1cc9b6)
B. Dia en el que mas peliculas se han visto  
El output consiste en: El dia en el que mas peliculas se han visto, la cantidad de peliculas vistas
![3b](https://github.com/SantiagoGonzalezR/Retos-y-labs-TET/assets/68928481/07106c45-0430-49e3-a5b8-b53da784df7d)
C. Dia en el que menos peliculas se han visto  
El output consiste en: El dia en el que menos peliculas se han visto, la cantidad de peliculas vistas
![3c](https://github.com/SantiagoGonzalezR/Retos-y-labs-TET/assets/68928481/e302e93c-f74a-4c30-af75-760c611dd58b)
D. Usuarios que ven una sola pelicula con su rating promedio  
El output consiste en: La ID de la pelicula, el rating promedio y la cantidad de usuarios que la vieron
![3d](https://github.com/SantiagoGonzalezR/Retos-y-labs-TET/assets/68928481/94c8ec9d-186e-4c37-84dc-8cf530360bee)
E. Dia de peor promedio de ratings  
El output consiste en: El dia con los peores ratings, el promedio de los ratings
![3e](https://github.com/SantiagoGonzalezR/Retos-y-labs-TET/assets/68928481/ffb80c0d-2327-4432-8047-0e99063fa284)
F. Dia con el mejor promedio de ratings  
El output consiste en: El dia con los mejores ratings, el promedio de los ratings
![3f](https://github.com/SantiagoGonzalezR/Retos-y-labs-TET/assets/68928481/c90c30f7-91e6-4381-abed-cfc593df69f6)
G. La mejor y peor pelicula por genero  
El output consiste en: El genero de pelicula, la ID de la pelicula con los peores ratings y la ID de la pelicula con los mejores ratings
![3g](https://github.com/SantiagoGonzalezR/Retos-y-labs-TET/assets/68928481/5ffed753-2d28-4308-aa04-cd2cf9e7e7ef)
