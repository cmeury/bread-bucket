[![Docker Hub Badge](https://img.shields.io/docker/v/cmeury/bread-bucket)](https://hub.docker.com/repository/docker/cmeury/bread-bucket)

# bread-bucket

Crude web app to enter transactions into 'Budget with Buckets' files. Hacked together to work with
a buckets file synced via Synology Drive and a container running on the same Synology device.

This is heavy work in progress, needs a lot of UI polish and added security.

Bucket file can be configured with an environment variable: `DB_FILE=/path/to/file.buckets`
    
## Build

Generate CSS file:

    npm run css-build

Watch for changes:

    npm start

To build the container:

    npm run docker-build

To test locally:

    docker run -it --publish 5050:5000 \
                   --mount type=bind,source=${HOME}/SynologyDrive/bar.buckets,target=/app/db.buckets \
                   cmeury/bread-bucket:latest

To push the container to Docker Hub:

    npm run docker-push


## Synology Setup

Many screenshots taken, will be added in the future here with more instructions.

### New Image

New image is not recognized by container, need to:
* Docker - Image - Add From URL: Enter `cmeury/bread-bucket`. A little blue bubble should appear next to 'Image' on the left.
* Wait until image is refreshed (bubble is gone)
* Copy configuration of container & start it

### Docker Mounted Folder Sync Problem Workaround

Does not pick up changes in file when mounted in docker container, so we need to 'touch' it after
comitting.

Create a file called `check_buckets.sh` in `/volume1/Drive` and make it executable: `chmod +x check_buckets.sh`

```bash
#!/bin/bash -eu
# script that maintains a hash of a file and touches the file if it has
# changed. this is a workaround of a docker mounted volume shortcoming.

file="bun-bun-test.buckets"
md5_file="${file}.md5"

current_md5sum=$(md5sum "${file}")
stored_md5sum=$(cat "${md5_file}")

if [[ "${current_md5sum}" != "${stored_md5sum}" ]]; then
	echo "File hash changed, updating file (${md5_file}): ${stored_md5sum} -> ${current_md5sum}"
	echo "${current_md5sum}" > "${md5_file}"
	echo "Touching file to trigger Synology Drive update.."
	touch "${file}"
else
	echo "File hash unchanged: ${current_md5sum}"
fi
```

Set up a regular script (every minute) in [Control Panel - Task Scheduler](https://kb.synology.com/en-uk/DSM/help/DSM/AdminCenter/system_taskscheduler?version=7):

```bash
cd /volume1/Drive
./check_buckets.sh
```

