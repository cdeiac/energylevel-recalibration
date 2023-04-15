#!/bin/bash
# assumes valid ssh key to access remote VM
scp -r app.py  deployer@130.60.75.173:~/garmin-connect/backend
scp -r /model  deployer@130.60.75.173:~/garmin-connect/backend
scp -r /config  deployer@130.60.75.173:~/garmin-connect/backend
scp -r .env  deployer@130.60.75.173:~/garmin-connect/backend
scp -r requirements.txt  deployer@130.60.75.173:~/garmin-connect/backend
scp -r logging.yaml  deployer@130.60.75.173:~/garmin-connect/backend