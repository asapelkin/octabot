Dockerfile


RUN apt update
RUN apt install octave python3 python3-pip git -y

WORKDIR /var

RUN git clone https://github.com/asapelkin/octabot.git
RUN pip install -r requirements.txt

ADD config.py /var/config.py


RUN cat /var/config.py
