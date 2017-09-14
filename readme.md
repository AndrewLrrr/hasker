# Django web application for Otus python developer course.

## Question-answer site, analogue of stackoverflow.com

### Docker image
```
Ubuntu 16.04
```

### Run
```
docker run --rm -it -p 8000:80 ubuntu /bin/bash
```

### Prepare
```
apt-get update
apt-get upgrade
apt-get install -y git
apt-get install -y make
mkdir apps && cd apps
git clone https://github.com/AndrewLrrr/hasker.git .
```

### Build
```
cd hasker
make stage
```

### API description
```
List of new questions        curl -X GET -H "Content-Type: application/json" http://localhost:8000/api/v1/questions/
List of trending questions   curl -X GET -H "Content-Type: application/json" http://localhost:8000/api/v1/trending/
Search questions             curl -X GET -H "Content-Type: application/json" http://localhost:8000/api/v1/search/?q=query
List of question answers     curl -X GET -H "Content-Type: application/json" http://localhost:8000/api/v1/questions/({pk}/answers/
Search questions by tag      curl -X GET -H "Content-Type: application/json" http://localhost:8000/api/v1/tags/{pk}/questions/
Obtain the auth token        curl -X POST -H "Content-Type: application/json" -d '{"username":"user","password":"secret"}' http://localhost:8000/api/v1/api-token-auth/
Vote up for the question     curl -X POST -H "Content-Type: application/json" -H "Authorization: JWT <your_token>" -d '{"value": "true"}'  http://localhost:8000/api/v1/questions/{pk}/vote/
Vote down for the question   curl -X POST -H "Content-Type: application/json" -H "Authorization: JWT <your_token>" -d '{"value": "false"}'  http://localhost:8000/api/v1/questions/{pk}/vote/
Vote up for the answer       curl -X POST -H "Content-Type: application/json" -H "Authorization: JWT <your_token>" -d '{"value": "true"}'  http://localhost:8000/api/v1/answers/{pk}/vote/
Vote down for the answer     curl -X POST -H "Content-Type: application/json" -H "Authorization: JWT <your_token>" -d '{"value": "false"}'  http://localhost:8000/api/v1/answers/{pk}/vote/
```

### Author
Андрей Ларин

slack: Andrey Larin (avatara)

email: larin.projects@gmail.com
