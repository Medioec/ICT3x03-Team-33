# ICT3x03-Team-33
## Docker containers setup
**All instructions are for windows powershell/cmd**
For now, the environment variables are ran before `docker-compose`. Credentials are in our telechat group ;)
1. Download Docker Desktop
From this link: https://docs.docker.com/get-docker/

2. Command to run all containers:
Ensure you are in repository directory `cd cinema-booking` 
then, run these commands in a batch

```
$Env:DB_NAME = <insert db name from tele>
$Env:DB_USER = <insert db user from tele>
$Env:DB_PASSWORD = <insert db password from tele>
docker-compose up -d
```

3. Check if containers are running:
On CLI, use these commands:
`docker ps` (lists running containers)
Then, navigate to the port number on your browser (e.g., `localhost:8080` for frontend)\
**OR** \
On Docker Desktop
Navigate to "Containers" section. Then, click on the ports for any of the containers to access it.

4. Stop containers before building & making changes
On CLI, use these commands:
`docker stop [container name]` (e.g., docker stop cinema-booking-database-1)\
**OR** \
On Docker Desktop
Press the stop button on the "cinema-booking" main container
