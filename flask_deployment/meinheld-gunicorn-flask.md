## Meinheld

Meinheld is a high-performance WSGI-compliant web server.

## Gunicorn

You can use Gunicorn to manage Meinheld and run multiple processes of it.

## Flask

Flask is a microframework for Python based on Werkzeug, Jinja 2 and good intentions.

## Alternatives

This image was created to be an alternative to tiangolo/uwsgi-nginx-flask, providing about 400% the performance of that image.

It is based on the more generic image tiangolo/meinheld-gunicorn. That's the one you would use for other WSGI frameworks, like Django.

## How to use

You don't need to clone the GitHub repo. You can use this image as a base image for other images, using this in your Dockerfile:

    FROM tiangolo/meinheld-gunicorn-flask:python3.7

    COPY ./app /app


Then you can build your image from the directory that has your Dockerfile, e.g:

    docker build -t myimage ./
        
## Advanced usage

####  Environment variables

These are the environment variables that you can set in the container to configure it and their default values:

MODULE_NAME

The Python "module" (file) to be imported by Gunicorn, this module would contain the actual Flask application in a variable.

By default:

app.main if there's a file /app/app/main.py or

main if there's a file /app/main.py

For example, if your main file was at /app/custom_app/custom_main.py, you could set it like:

docker run -d -p 80:80 -e MODULE_NAME="custom_app.custom_main" myimage

####  VARIABLE_NAME

The variable inside of the Python module that contains the Flask application.

By default:

app

For example, if your main Python file has something like:

from flask import Flask

api = Flask(__name__)

@api.route("/")

def hello():

    return "Hello World from Flask"
    
In this case api would be the variable with the "Flask application". You could set it like:

docker run -d -p 80:80 -e VARIABLE_NAME="api" myimage

#### APP_MODULE

The string with the Python module and the variable name passed to Gunicorn.

By default, set based on the variables MODULE_NAME and VARIABLE_NAME:

app.main:app or

main:app

You can set it like:

docker run -d -p 80:80 -e APP_MODULE="custom_app.custom_main:api" myimage

####  GUNICORN_CONF

The path to a Gunicorn Python configuration file.

By default:

/app/gunicorn_conf.py if it exists

/app/app/gunicorn_conf.py if it exists

/gunicorn_conf.py (the included default)

You can set it like:

docker run -d -p 80:80 -e GUNICORN_CONF="/app/custom_gunicorn_conf.py" myimage

####  WORKERS_PER_CORE

This image will check how many CPU cores are available in the current server running your container.

It will set the number of workers to the number of CPU cores multiplied by this value.

By default:

2

You can set it like:

docker run -d -p 80:80 -e WORKERS_PER_CORE="3" myimage

If you used the value 3 in a server with 2 CPU cores, it would run 6 worker processes.

You can use floating point values too.

So, for example, if you have a big server (let's say, with 8 CPU cores) running several applications, and you have an ASGI application that you know won't need high performance. And you don't want to waste server resources. You could make it use 0.5 workers per CPU core. For example:

docker run -d -p 80:80 -e WORKERS_PER_CORE="0.5" myimage

In a server with 8 CPU cores, this would make it start only 4 worker processes.

####  WEB_CONCURRENCY

Override the automatic definition of number of workers.

By default:

Set to the number of CPU cores in the current server multiplied by the environment variable WORKERS_PER_CORE. So, in a server with 2 cores, by default it will be set to 4.

You can set it like:

docker run -d -p 80:80 -e WEB_CONCURRENCY="2" myimage

This would make the image start 2 worker processes, independent of how many CPU cores are available in the server.

#### HOST
The "host" used by Gunicorn, the IP where Gunicorn will listen for requests.

It is the host inside of the container.

So, for example, if you set this variable to 127.0.0.1, it will only be available inside the container, not in the host running it.

It's is provided for completeness, but you probably shouldn't change it.

By default:

0.0.0.0

#### PORT

The port the container should listen on.

If you are running your container in a restrictive environment that forces you to use some specific port (like 8080) you can set it with this variable.

By default:

80

You can set it like:

docker run -d -p 80:8080 -e PORT="8080" myimage


####  BIND

The actual host and port passed to Gunicorn.

By default, set based on the variables HOST and PORT.

So, if you didn't change anything, it will be set by default to:

0.0.0.0:80

You can set it like:

docker run -d -p 80:8080 -e BIND="0.0.0.0:8080" myimage

#### LOG_LEVEL

The log level for Gunicorn.

One of:

debug

info

warning

error

critical

By default, set to info.

If you need to squeeze more performance sacrificing logging, set it to warning, for example:

You can set it like:

docker run -d -p 80:8080 -e LOG_LEVEL="warning" myimage

Logs are sent to the container's stderr and stdout, meaning you can view the logs with the docker logs -f your_container_name_here command.


