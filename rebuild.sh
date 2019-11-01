#!/bin/bash
# This runs on the production server: fetches new code,
# installs needed packages, and restarts the server.

export project_name=CourseBuilder

# get new source code onto the server
git pull origin master
# activate our virtual env:
source /home/CourseBuilder/.virtualenvs/CourseBuilder/bin/activate
# install all of our packages:
pip install -r docker/requirements.txt
echo "Going to reboot the webserver"
API_TOKEN=10a10802d8fe9c6cce0181d30f0074fd6180cf5c pa_reload_webapp.py CourseBuilder.pythonanywhere.com
touch reboot
