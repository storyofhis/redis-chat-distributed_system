# Chat Application
## presequite
- install python
- install redis
- install docker & docker-compose

## run the apps
- clone this repo
- first running the container
  ```
  docker-compose up -d
  ```
- check the container already run or not ??
  ```
  docker ps
  ```
- there's 2 containers : 
  - workmesin1 in `http://0.0.0.0:60001/lab`
password : mesin1
  - workmesin2 in `http://0.0.0.0:60002/lab`
password : mesin2

## server : 
- go to workmesin2
- change the directory into `/home/jovyan/work`
```
cd /home/jovyan/work
```
- run the server firstly :
```
python server.py
```

## client : 
- go to workmesin1
- change the directory into `/home/jovyan/work`
```
cd /home/jovyan/work
```
- make it 2 clients, in orther to communicate one client to each other
```
python client.py [someone_1]
```
```
python client.py [someone_2]
```

### chat apps display :
during the server has already on, the communication between alex and bobby as client1 and client2 can send and receive to each other.
<img width="1440" alt="Screenshot 2023-12-28 at 16 11 13" src="https://github.com/storyofhis/redis-chat-distributed_system/assets/72302421/05aa516d-d71a-4dad-997e-13cba04e495d">


