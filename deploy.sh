#!/bin/bash
# This shell file deploys a new version to our server.

export project_name=CourseBuilder

eval "$(ssh-agent -s)" # Start ssh-agent cache
chmod 600 ~/.ssh/id_rsa # Allow read access to the private key
ssh-add ~/.ssh/id_rsa # Add the private key to SSH

echo "SSHing to PythonAnywhere."
ssh -o "StrictHostKeyChecking no" -i ~/.ssh/id_rsa $project_name@ssh.pythonanywhere.com pwd << EOF
    cd ~/$project_name; ~/$project_name/rebuild.sh
EOF
