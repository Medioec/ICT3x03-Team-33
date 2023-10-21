# ICT3x03-Team-33
## Important note for Windows environment
### Fixing problems with CRLF
Github Desktop changes LF to CRLF for linux .sh files which will break app functionality. Run the following commands in repository base directory after saving and committing your code to fix CRLF problems.
```
git rm -rf --cached .
git reset --hard HEAD
```

## Deployment in local dev environment
Run the dev scripts in scripts/ directory from the repo base directory to build and deploy.

### Example
#### Windows
```.\scripts\dev-build.bat```
#### Linux
```./scripts/dev-build.sh```

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
or
`docker-compose down --volumes` (This removes all containers and database information. Remove `--volumes` if u want to keep database information. Keep if you want to reset database from init.sql) 
**OR** \
On Docker Desktop
Press the stop button on the "cinema-booking" main container
