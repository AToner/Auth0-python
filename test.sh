curl --request GET --url http://localhost:8080/ping
curl --request GET --url http://localhost:8080/secure
TOKEN=$(curl --request GET --url 'http://localhost:8080/gettoken?username=auth0-user@andytoner.com&password=atestuser')
curl --header 'authorization: Bearer '$TOKEN \
       --request GET \
       --url http://localhost:8080/secure

