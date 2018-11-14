FROM debian:latest

RUN apt update
RUN apt install octave python3 python3-pip git -y

WORKDIR /var

RUN git  clone  https://github.com/asapelkin/octabot.git 
WORKDIR /var/octabot
RUN pip3 install -r requirements.txt

ADD config.py /var/octabot/config.py

RUN ls
RUN cat start.sh

CMD ["sh","/var/octabot/start.sh"]
