#!/usr/bin/env python3
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Supersimple script for tracking pacages via Posten/Brings's API
"""
import argparse
import json
import requests


def retrieve_tracking(parcel_id):
    """
    Grab JSON from bring's API (v2)
    Need a valid consignmentId (parcel_id)

    @returns json blob of tracking data
    """
    url="https://tracking.bring.com/api/v2/tracking.json"
    params = {'q':parcel_id}
    res = requests.get(url, params)
    return res.json()


def parse_tracking(jsond):
    """
    parse trackign json and format a simple, short list of steps where the parcel has been

    @param: json data blob

    @returns: nothing, it prints directly
    """
    if 'consignmentSet' not in jsond or len(jsond['consignmentSet']) != 1:
        return

    cset = jsond['consignmentSet'][0]
    if 'error' in cset:
        print("Cannot track - {}".format(cset['error']['message']))
        return

    print("Tracking parcel {} from {}".format(cset['consignmentId'], cset['senderName']))
    if 'packageSet' not in cset or len(cset['packageSet']) < 1:
        return

    if 'eventSet' not in cset['packageSet'][0] or len(cset['packageSet'][0]['eventSet']) < 1:
        return

    for eset in cset['packageSet'][0]['eventSet']:
        print("{} {} - {:12s} {} ({} - {})".format(eset['displayDate'], eset['displayTime'],
                                        eset['city'], eset['country'],
                                        eset['status'], eset['description']))


def main():
    """
    mainloop
    """
    parser = argparse.ArgumentParser(description="Track packages via Posten/Bring's API")
    parser.add_argument("-f", "--file",
                        dest='file',
                        metavar="FILE",
                        help="Store .js-file to parse (for testing/dev)")
    parser.add_argument("-t", "--track-id",
                        dest="parcel_id",
                        type=str,
                        help="Tracking ID of parcel")
    parser.add_argument("-T", "--track-id-list",
                        dest="parcel_ids",
                        help="List of IDs to track (comma-separated, no spaces)")
    args = parser.parse_args()
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as jsonfd:
            parse_tracking(json.load(jsonfd))

    elif args.parcel_id:
        parse_tracking(retrieve_tracking(args.parcel_id))

    elif args.parcel_ids:
        ids = args.parcel_ids.split(',')
        for i in ids:
            parse_tracking(retrieve_tracking(i))
            print("")
    else:
        print("No valid switches and no data found")


if __name__ == "__main__":
    main()
