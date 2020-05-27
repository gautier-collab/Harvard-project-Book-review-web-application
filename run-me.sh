while read -r line; do
    echo "$line"
    if [[ "$line" == *"spawned uWSGI worker 4"* ]]; then
        echo "IT IS WORKING"
        sudo python3 app/website-opening.py
    fi
done< <(sudo docker-compose up --build)
