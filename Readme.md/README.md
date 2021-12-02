# Pakkesporing
(Parceltracker)

Really simple script for tracking packages using Posten/Brings API.

## Help
For convenience, add sporing.py to your path (I keep mine in ~/bin as
'sporing')
``` bash
$ ln -s $(pwd)/sporing.py ~/bin/sporing
$ sporing -h
usage: sporing.py [-h] [-f FILE] [-t PARCEL_ID] [-T PARCEL_IDS]

Track packages via Posten/Bring's API

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Store .js-file to parse (for testing/dev)
  -t PARCEL_ID, --track-id PARCEL_ID
                        Tracking ID of parcel
  -T PARCEL_IDS, --track-id-list PARCEL_IDS
                        List of IDs to track (comma-separated, no spaces)
```

## Track single package
``` bash
sporing -t 3133742
Tracking parcel 3133742 from Tarasin Palace
12.11.2021 08:19 - TILLER       Norway (IN_TRANSIT - The shipment has arrived at terminal and will be forwarded.)
11.11.2021 21:24 - OSLO         Norway (IN_TRANSIT - The shipment is in transit)
11.11.2021 19:30 - OSLO         Norway (IN_TRANSIT - The shipment has been sorted and forwarded.)
11.11.2021 18:59 - OSLO         Norway (IN_TRANSIT - The shipment has arrived at terminal.)
11.11.2021 15:53 - EBOU DAR     Altara (IN_TRANSIT - The shipment is in transit)
11.11.2021 14:53 - EBOU DAR     Altara (IN_TRANSIT - The shipment has been handed in at terminal and forwarded.)
10.11.2021 17:52 -               (PRE_NOTIFIED - No shipment has been received yet, only notification of the shipment.)
```


## Track several packages
Use the track-id-list option, must be a comma-separated list of
tracking-ids, no spaces

``` bash
sporing -T <trackingID1>,<trackingID2>,<trackingID3>
sporing -t 3133742,3133717
Tracking parcel 3133742 from Tarasin Palace
12.11.2021 08:19 - TILLER       Norway (IN_TRANSIT - The shipment has arrived at terminal and will be forwarded.)
11.11.2021 21:24 - OSLO         Norway (IN_TRANSIT - The shipment is in transit)
11.11.2021 19:30 - OSLO         Norway (IN_TRANSIT - The shipment has been sorted and forwarded.)
11.11.2021 18:59 - OSLO         Norway (IN_TRANSIT - The shipment has arrived at terminal.)
11.11.2021 15:53 - EBOU DAR     Altara (IN_TRANSIT - The shipment is in transit)
11.11.2021 14:53 - EBOU DAR     Altara (IN_TRANSIT - The shipment has been handed in at terminal and forwarded.)
10.11.2021 17:52 -               (PRE_NOTIFIED - No shipment has been received yet, only notification of the shipment.)

Tracking parcel 3133717 from Stone of Tear
11.11.2021 07:25 - TILLER       Norway (IN_TRANSIT - The shipment has arrived at terminal and will be forwarded.)
11.11.2021 21:24 - OSLO         Norway (IN_TRANSIT - The shipment is in transit)
11.11.2021 19:30 - OSLO         Norway (IN_TRANSIT - The shipment has been sorted and forwarded.)
11.11.2021 18:59 - OSLO         Norway (IN_TRANSIT - The shipment has arrived at terminal.)
11.11.2021 15:53 - TEAR         Tear (IN_TRANSIT - The shipment is in transit)
11.11.2021 14:53 - STONE        Tear (IN_TRANSIT - The shipment has been handed in at terminal and forwarded.)
```
