# ICT3x03-Team-33
## Docker containers setup

For now, the environment variables are ran before `docker-compose`. Credentials are in our telechat group ;)
1. Download Docker Desktop
From this link: https://docs.docker.com/get-docker/
Or if you are on linux/ubuntu gang you alrdy have it installed

2. Command to run all containers:
Ensure you are in repository directory `cd cinema-booking` 
then, run these commands in a batch

```
$Env:DB_NAME = "cinema_db"
$Env:DB_USER = "cinema_user"
$Env:DB_PASSWORD = "mysecretpassword"
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

## Database setup
1. Ensure Docker is up and running with `docker ps`
2. In the `database` container, run the command `ls` to look for the directory called `sql_files`. Path into it with `cd sql_files`
3. Run the following command `psql -d cinema_db -U cinema_user -a -f init.sql`. Key in password if necessary (probably dont need)
4. Ensure no errors, and database should be set up.
