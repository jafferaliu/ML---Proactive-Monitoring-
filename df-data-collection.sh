###  df data collection

#/bin/bash

FILE=/tmp/df-opt.csv
TIME=$(date +"%F %T")
HOST_NAME=$(hostname)
df -Tm | egrep -v 'devtmpfs|tmpfs|nfs' | grep -v "Filesystem" | awk -v v1=$HOST_NAME -v v2="$TIME" '{print v1","v2","$3","$4","$5","$7}' >$FILE

export ACCESS_TOKEN=$(curl http://xx.xx.xx.xxx)

while IFS= read -r line; do
    HN=$(echo $line | awk -F "," '{print $1}')
    TIME1=$(echo $line | awk -F "," '{print $2}')
    Size=$(echo $line | awk -F "," '{print $3}')
    Used=$(echo $line | awk -F "," '{print $4}')
    Avail=$(echo $line | awk -F "," '{print $5}')
    Mounted_on=$(echo $line | awk -F "," '{print $6}')
    TIME=$(echo $TIME1 | sed 's/./ /11')
    curl --location --request POST 'https://pubsub.googleapis.com/v1/projects/project-id/topics/topic:publish' \
        --header 'Content-Type: application/json' \
        -H "Authorization: Bearer $ACCESS_TOKEN" \
        --data-raw "{\"messages\":[{\"data\":\"$(echo "{\"hostname\":\"$HN\",\"TIME\":\"$TIME\",\"Size\":\"$Size\",\"Avail\":\"$Avail\",\"Mounted\":\"$Mounted_on\",\"Used\":\"$Used\"}" | base64 -w 0)\",\"attributes\":{}}]}"
done <"$FILE"

