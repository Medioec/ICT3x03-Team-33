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
In windows powershell, to down all containers and volumes: `.\scripts\dev-kill-volumes.bat`
Linux: `./scripts/dev-kill-volumes.bat`

In windows powershell to ONLY down the containers without messing with db: `.\scripts\dev-kill`
Linux: `./scripts/dev-kill`
