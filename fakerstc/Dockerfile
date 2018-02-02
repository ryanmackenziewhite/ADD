FROM python:3.6.4-alpine3.7

RUN wget https://github.com/ryanmackenziewhite/ADD/archive/master.zip
RUN unzip master.zip
RUN mv ADD-master myapp

RUN pip install -r myapp/fakerstc/requirements.txt

ENTRYPOINT ["python", "myapp/fakerstc"]
