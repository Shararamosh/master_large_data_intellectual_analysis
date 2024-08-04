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

#������ �� �������� hadoop
#https://hadoop.apache.org/docs/r1.0.4/mapred_tutorial.html#Usage

#������������� ���������� �����
export HADOOP_CLASSPATH=$(hadoop classpath)
echo $HADOOP_CLASSPATH

#�������� �������� � �������� ������� HDFS
hadoop fs -mkdir /WordCountTutorial

#C������� �������� ������ ��� �����
hadoop fs -mkdir /WordCountTutorial/Input

#��������� ������� � ��������� ��� ��������� ��������
#localhost:50070
#Utilities > Browser the file system

#��������� ����� � ��������
hadoop fs -put '/home/user/Desktop/WordCountTutorial/input_data/input.txt' /WordCountTutorial/Input

#��������� � ������� ��������
cd /home/home/user/Desktop/WordCountTutorial

#��������� java ��� 
javac -classpath ${HADOOP_CLASSPATH} -d '/home/user/Desktop/WordCountTutorial/tutorial_classes' '/home/user/Desktop/WordCountTutorial/WordCount.java'

#��������� ����� � tutorial_classes �������� � ���� ���� jar
jar -cvf firstTutorial.jar -C tutorial_classes/ .

#��������� ���� .jar 
hadoop jar '/home/user/Desktop/WordCountTutorial/firstTutorial.jar' WordCount /WordCountTutorial/Input /WordCountTutorial/Output

#�����
hadoop dfs -cat /WordCountTutorial/Output/*