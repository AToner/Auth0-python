URL=http://python-flask-dev.us-east-1.elasticbeanstalk.com
#URL=http://localhost:8080
curl --request GET --url $URL/ping
echo
sleep 1
curl --request GET --url $URL/secure
echo
sleep 1
TOKEN=$(curl --request GET --url $URL'/gettoken?username=auth0-user@andytoner.com&password=atestuser')
echo $TOKEN
sleep 1
curl --header 'authorization: Bearer '$TOKEN \
       --request GET \
       --url $URL/secure
echo
