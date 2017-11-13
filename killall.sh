#!/bin/bash
NODE_ID=$(ps -e | grep "node app" | cut -d " " -f 1)
PYTHON_ID=$(ps -e | grep "python" | cut -d " " -f 1)
kill -9 $NODE_ID
kill -9 $PYTHON_ID


exit
echo "Processes using ports"
echo "--------------"
echo "Port 8888 in use?"
P1=$(lsof -a -i:8888 | awk '{print $2}')
echo $P1 
echo "--------------"
echo "Port 5000 in use?"
P2=$(lsof -a -i:5000 | awk '{print $2}')
echo $P2
echo "--------------"

