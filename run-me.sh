#!/bin/bash

while read -r line; do
    echo "$line"
    if [[ "$line" == *"spawned uWSGI worker 4"* ]]; then
        echo "" && echo "The web application is launched at http://localhost/" && echo ""
        python3 app/website-opening.py
    fi
done< <(sudo docker-compose up --build)
