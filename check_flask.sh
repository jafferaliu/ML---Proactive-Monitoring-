## check process and run 

ps -ef | grep -i flask_token.py | grep -v grep > /dev/null 2>&1
if [ $? -ne 0 ]
then 
    /usr/bin/python /root/flask_token.py > /tmp/log.txt 2>&1 &
fi 
