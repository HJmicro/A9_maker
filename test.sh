#!/bin/bash
while true;do
	ps -ef|grep main.py
	if [[ $? -eq 1 ]];then
		echo "main.py failed"
		python main.py
		sleep 3
	else
		sleep 3
	fi
done
