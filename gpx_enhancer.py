from pathlib import Path
from typing import Tuple
from dataclasses import dataclass
from exif import Image
import gpxpy
import gpxpy.gpx
from datetime import datetime


@dataclass
class PhotoDetail:
    gps_latitude: tuple
    gps_latitude_ref: str
    gps_longitude: tuple
    gps_longitude_ref: str
    timestamp: datetime

    def __post_init__(self):
        self.timestamp = datetime.strptime(self.timestamp, "%Y:%m:%d %H:%M:%S")


def decimal_degrees(details: PhotoDetail) -> Tuple:
    latitude_sign = 1 if "N" == details.gps_latitude_ref else -1
    longitude_sign = 1 if "E" == details.gps_longitude_ref else -1

    latitude = details.gps_latitude[0] + details.gps_latitude[1] / 60 + details.gps_latitude[2] / 3600
    longitude = details.gps_longitude[0] + details.gps_longitude[1] / 60 + details.gps_longitude[2] / 3600

    return latitude * latitude_sign, longitude * longitude_sign


p = Path("photos")

photos_data = []
for file in p.iterdir():
    if "mp4" in file.name:
        continue

    with open(file, "rb") as image_file:
        my_image = Image(image_file)

        try:
            photos_data.append(
                PhotoDetail(
                    gps_latitude=my_image.gps_latitude,
                    gps_latitude_ref=my_image.gps_latitude_ref,
                    gps_longitude=my_image.gps_longitude,
                    gps_longitude_ref=my_image.gps_longitude_ref,
                    timestamp=my_image.datetime,
                )
            )
        except AttributeError:
            print(f"missing data in file {file.name}")


photos_data = sorted(photos_data, key=lambda x: x.timestamp)
# -------------------------

with open("manual.gpx", "r") as track:
    gpx_file = gpxpy.parse(track)

for d in photos_data:
    # create new point
    lat, log = decimal_degrees(d)
    new_point = gpxpy.gpx.GPXTrackPoint(lat, log, time=d.timestamp)

    # find closes point
    picked_point = None
    diff = 10
    for point in gpx_file.tracks[0].segments[0].points:

        # todo unfinished here
        current_diff = abs(picked_point.latitude - lat)
        if current_diff <= diff:
            diff = current_diff

    gpx_file.tracks[0].segments[0].points.append(new_point)

with open("manual_new.gpx", "w") as track:
    track.write(gpx_file.to_xml())
