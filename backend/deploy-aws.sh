#!/bin/bash
# assumes valid ssh key to access remote VM
scp -r app.py  ec2-user@ec2-3-68-229-63.eu-central-1.compute.amazonaws.com:~/garmin-app/backend/
scp -r config/  ec2-user@ec2-3-68-229-63.eu-central-1.compute.amazonaws.com:~/garmin-app/backend/
scp -r mapping/ ec2-user@ec2-3-68-229-63.eu-central-1.compute.amazonaws.com:~/garmin-app/backend/
scp -r models/ ec2-user@ec2-3-68-229-63.eu-central-1.compute.amazonaws.com:~/garmin-app/backend/
scp -r repositories/  ec2-user@ec2-3-68-229-63.eu-central-1.compute.amazonaws.com:~/garmin-app/backend/
scp -r routers/ ec2-user@ec2-3-68-229-63.eu-central-1.compute.amazonaws.com:~/garmin-app/backend/
scp -r schemas/  ec2-user@ec2-3-68-229-63.eu-central-1.compute.amazonaws.com:~/garmin-app/backend/
scp -r services/  ec2-user@ec2-3-68-229-63.eu-central-1.compute.amazonaws.com:~/garmin-app/backend/
scp -r .env  ec2-user@ec2-3-68-229-63.eu-central-1.compute.amazonaws.com:~/garmin-app/backend/
scp -r requirements.txt  ec2-user@ec2-3-68-229-63.eu-central-1.compute.amazonaws.com:~/garmin-app/backend/
scp -r logging.yaml  ec2-user@ec2-3-68-229-63.eu-central-1.compute.amazonaws.com:~/garmin-app/backend/
scp -r Dockerfile  ec2-user@ec2-3-68-229-63.eu-central-1.compute.amazonaws.com:~/garmin-app/backend/