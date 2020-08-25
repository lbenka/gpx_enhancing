# gpx_enhancing
Merge gpx info from Mapy.cz route and Google Photos metadata as location and time to create Strava compatible and upload-able workout

seems like tools that I am gonna use are:
1. https://github.com/tkrajina/gpxpy
2. https://gitlab.com/TNThieding/exif
3. python 3.8

## Approach

1. identify where can timestamp from photos can be place in timeline for each photo
2. fill in missing timestamps by averaging time
