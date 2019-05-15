# Windows Powershell Script for coursebuilder Docker Container
docker rm coursebuilder | true
docker run -it -p 8000:8000 -v ${PWD}:/home/coursebuilder coursebuilder bash
