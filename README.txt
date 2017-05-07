Setup
From: http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html
virtualenv ~/eb-virt
source ~/eb-virt/bin/activate     (use deactivate)


Installing the requirements
pip install -r requirements.txt

Local testing...




Examples
$ curl --request GET --url http://localhost:8080/
Hello Blah World

$ curl --request GET --url http://localhost:8080/ping
Ping

$ curl --request GET --url http://localhost:8080/secure
{"timestamp":1493588119850,"status":401,"error":"Unauthorized","message":"Unauthorized","path":"/secure"}

$ curl --header 'authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlFqbERRVEpCT0VSRU1EUTRSVVJFTmpnME5FWXhOVVJDTmtVelJFWTJSall5T1RJeU16UkROUSJ9.eyJpc3MiOiJodHRwczovL2FtcGxlcm8uYXV0aDAuY29tLyIsInN1YiI6IlZSTTFvdTVPd0FJaXNXeXVVRXBvc1FHdTRpZXZpWFB6QGNsaWVudHMiLCJhdWQiOiJodHRwczovL3d3dy5hbXBsZXJvLmNvbSIsImV4cCI6MTQ5Mzg3MDkxMSwiaWF0IjoxNDkzNzg0NTExLCJzY29wZSI6IiJ9.O3ldcZlFcU7UIowZNWz3DZHPE--9L-ypoR1rcb-uG3Mk8SaYhVL-BQvoUSB3_7Is2IyE0OMslSdQtw6DxE36XVe-eZo9szKnbkLyrzq0RaUr2y5jaFLVQNjyavJ0-XMyYT9rw4lAjgbuAXNF8zkVx53nfYkr2ZH0WTifIklDHME-gjsgOxv4TZ_Q1KEDNlfnyPhynWAb2vR9kd9TqwGFL1ghQ8GfG204GrXY1Pfj6y_nH2LUCePfYvao2ed02p8XtYpsDKESFamcTYD9DS1JdqSlhKpE5V8nryykcsADKX77sF9qY9wcTPqMEU1q1lkwQremi32qnFMq4QGOUaHLRA' \
       --request GET \
       --url http://localhost:8080/secure
SECURE!

