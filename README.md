# ICT3x03-Team-33
## Important note for Windows environment
### Fixing problems with CRLF
Github Desktop changes LF to CRLF for linux .sh files which will break app functionality. Run the following commands in repository base directory when checking out the branch to fix CRLF problems.
```
git rm -rf --cached .
git reset --hard HEAD
```

## Deploying containers in local dev environment
1. Download Docker Desktop
From this link: https://docs.docker.com/get-docker/

2. Command to run all containers:
Ensure you are in repository base directory (directory with README.md)
then, run the dev scripts in the scripts/ directory

#### Windows
```
.\scripts\dev-build.bat
.\scripts\dev-deploy.bat
```
#### Linux
```
./scripts/dev-build.sh
./scripts/dev-deploy.sh
```

3. Check if containers are running:\
On CLI, use these commands:\
`docker ps` (lists running containers)\
Then, navigate to the port number on your browser (e.g., `localhost:8080` for frontend)\
**OR** \
On Docker Desktop\
Navigate to "Containers" section. Then, click on the ports for any of the containers to access it.\

4. Stop containers before building & making changes\
On CLI, use the dev-deploy convenience script for redeploying after making changes. This does not remove the db volume. Alternatively, dev-kill will just stop all the deployed containers.\
or\
Use these commands:\
`docker stop [container name]` (e.g., docker stop cinema-booking-database-1)\
or\
`docker-compose down --volumes` (This removes all containers and database information. Remove `--volumes` if u want to keep database information. Keep if you want to reset database from init.sql)\
**OR** \
On Docker Desktop\
Press the stop button on the "cinema-booking" main container
