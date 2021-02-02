sudo docker build -t django .
sudo docker run -d -p 9999:80 -e VARIABLE_NAME="application" django
