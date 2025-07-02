# energylevel-recalibration

# Sync Service

This dummy service accepts Garmin API data and appends it do `data.json` file. 
It basically accepts any http requests and logs their payload and is currently 
running on the ifi server.
Note that entire file is not a valid JSON file but rather contains multiple 
independent JSON snippets to try out multiple requests at the same time.

## Setup Instructions

Run the service with nohup, which keeps the process running:

```
nohup python main.py &
```

To check the logs for debugging purposes:

```
tail nohup.out -f
```

## Downloading the Data

The data contains the relevant Garmin API payload that may be used on the backend endpoints 
to insert Garmin data to the running MongoDB instance.

Download the JSON data with the following command:

```
scp deployer@130.60.75.173:~/garmin-connect/sync/data.json .
```