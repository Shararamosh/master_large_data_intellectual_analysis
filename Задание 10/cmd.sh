#!/bin/bash
sudo apt update
sudo apt install default-jdk
java -version

wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.1/hadoop-3.3.1.tar.gz
tar -xzvf hadoop-3.3.1.tar.gz
sudo mv hadoop-3.3.1 /usr/local/hadoop

readlink -f /usr/bin/java | sed "s:bin/java::"
sudo nano /usr/local/hadoop/etc/hadoop/hadoop-env.sh

export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/

#/usr/local/hadoop/bin/hadoop

hadoop version

#Ссылка на материал hadoop
#https://hadoop.apache.org/docs/r1.0.4/mapred_tutorial.html#Usage

#Устанавливаем переменные среды
export HADOOP_CLASSPATH=$(hadoop classpath)
echo $HADOOP_CLASSPATH

#Создание каталого в файловой системе HDFS
hadoop fs -mkdir /WordCountTutorial

#Cоздание каталога внутри для ввода
hadoop fs -mkdir /WordCountTutorial/Input

#Открываем браузер и проверяем что создались каталоги
#localhost:50070
#Utilities > Browser the file system

#Загружаем файлы в каталоги
hadoop fs -put '/home/user/Desktop/WordCountTutorial/input_data/input.txt' /WordCountTutorial/Input

#Переходим в каталог учебника
cd /home/home/user/Desktop/WordCountTutorial

#Выполняем java код 
javac -classpath ${HADOOP_CLASSPATH} -d '/home/user/Desktop/WordCountTutorial/tutorial_classes' '/home/user/Desktop/WordCountTutorial/WordCount.java'

#Созданные файлы в tutorial_classes помещаем в один файл jar
jar -cvf firstTutorial.jar -C tutorial_classes/ .

#Запускаем файл .jar 
hadoop jar '/home/user/Desktop/WordCountTutorial/firstTutorial.jar' WordCount /WordCountTutorial/Input /WordCountTutorial/Output

#Вывод
hadoop dfs -cat /WordCountTutorial/Output/*