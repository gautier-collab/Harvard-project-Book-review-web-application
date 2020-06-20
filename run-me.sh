#!/bin/bash



# Following section avoids error msg such as "ERROR: for nginx  Cannot start service nginx: driver failed programming external connectivity on endpoint[...]Error starting userland proxy: listen tcp 0.0.0.0:80: bind: address already in use"

sudo docker stop $(docker ps -a -q); docker rm $(docker ps -a -q); docker volume rm $(docker volume ls -qf dangling=true)
sudo docker network rm $(docker network ls -q)

# Get every line outputted from (sudo lsof -nP | grep LISTEN) command
declare -a arrayName
while read -r; do
  arrayName+=( "$REPLY" )
done< <(sudo lsof -nP | grep LISTEN)

# Find nginx lines
for i in "${arrayName[@]}"
do
    if [[ $i == *"nginx"* ]]; then
        # Get second field of the line
        target=`echo $i | cut -d ' ' -f 2`
        echo "process to kill is" $target
    fi
done
sudo kill -9 $target



while read -r line; do
    echo "$line"
    if [[ "$line" == *"spawned uWSGI worker 4"* ]]; then
        echo "" && echo "The web application is launched at http://localhost/" && echo ""
        python3 app/website-opening.py
    fi
done< <(sudo docker-compose up --build)