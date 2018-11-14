# octabot
Telegram Bot -- GNU Octave (MATLAB) interpreter 

### build & run
```
git clone https://github.com/asapelkin/octabot.gitecho 
cd octabot
echo "token = <YOUR TOKEN HERE>" > config.py
docker build . -t octabot
docker run  --restart=always  -d octabot
```



