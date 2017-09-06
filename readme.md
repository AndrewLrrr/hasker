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
git clone https://github.com/AndrewLrrr/hasker.git .
```

### Build
```
cd hasker
make stage
```

### Author
Андрей Ларин

slack: Andrey Larin (avatara)

email: larin.projects@gmail.com
