# ICT3x03-Team-33
## Important note for Windows environment
### Fixing problems with CRLF
Github Desktop changes LF to CRLF for linux .sh files which will break app functionality. Run the following commands in repository base directory after saving and committing your code to fix CRLF problems.
```
git rm -rf --cached .
git reset --hard HEAD
```

## Deployment in dev environment
Run the dev scripts in scripts/ directory from the repo base directory to build and deploy.

### Example
#### Windows
```.\scripts\dev-build.bat```
#### Linux
```./scripts/dev-build.sh```
