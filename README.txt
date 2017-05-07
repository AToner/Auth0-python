Setup
From: http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html
virtualenv ~/eb-virt
source ~/eb-virt/bin/activate     (use deactivate)


Installing the requirements
pip install -r requirements.txt

Local testing...
python application.py



Examples
$ curl --request GET --url http://localhost:8080/ping
Ping

$ curl --request GET --url http://localhost:8080/secure
[NOTHING.. 401]

curl --request GET --url 'http://localhost:8080/gettoken?username=auth0-user@andytoner.com&password=atestuser'
Spits out a token to use in the secure calls.

$ curl --header 'authorization: Bearer [token from previous call]' \
       --request GET \
       --url http://localhost:8080/secure
SECURE!


Bash script playing
curl --request GET --url http://localhost:8080/ping
curl --request GET --url http://localhost:8080/secure
TOKEN=$(curl --request GET --url 'http://localhost:8080/gettoken?username=auth0-user@andytoner.com&password=atestuser')
curl --header 'authorization: Bearer '$TOKEN \
       --request GET \
       --url http://localhost:8080/secure

