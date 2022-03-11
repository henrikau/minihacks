#!/usr/bin/env python3

import argparse
import json
import requests
import sys
import urllib.parse


def strip_urlspace(line):
    return line.replace("&nbsp;","")


rows = ['00-01','01-02','02-03','03-04','04-05','05-06',
        '06-07','07-08','08-09','09-10','10-11','11-12',
        '12-13','13-14','14-15','15-16','16-17','17-18',
        '18-19','19-20','20-21','21-22','22-23','23-00',
        'Min','Max','Average','Peak','Off-peak 1','Off-peak 2']

def row_to_idx(row):
    r = strip_urlspace(row)
    if r in rows:
        return rows.index(r)
    return 0


def norm_price(price):
    p = price.replace(' ','')
    p = p.replace(',','.')
    return float(p)/1000.0*1.25


def grab_json():
    # https://www.nordpoolgroup.com/api/marketdata/page/23?currency=NOK,NOK,EUR,EUR
    url= "https://www.nordpoolgroup.com/api/marketdata/page/23"
    params = {'currency': "NOK"}
    res = requests.get(url, params)
    return res.json()


def parse_json(jsond):
    if not jsond or \
       'data' not in jsond or \
       'currency' not in jsond or \
       jsond['currency'] != 'NOK':
        print("Missing vital keys in json, cannot parse")
        sys.exit(0)

    # print(jsond.keys())
    # print(jsond['data'].keys())
    start = jsond['data']['DataStartdate']
    end = jsond['data']['DataEnddate']

    # dict
    # 'city': {'oslo': [...], trheim: [..],...}
    dataset = {}
    print("Got {} rows of data".format(len(jsond['data']['Rows'])))
    for row in jsond['data']['Rows']:
        # print("{}: {} - {}".format(strip_urlspace(row['Name']), row['StartTime'], row['EndTime']))
        for col in row['Columns']:
            if col['Name'] not in dataset:
                dataset[col['Name']] = [0]*30
            idx = row_to_idx(row['Name'])
            dataset[col['Name']][idx] = col['Value']

    return start, end, dataset

def pretty_print(start, end, dataset, filter=None):
    print("Strømpriser for {} - {}".format(start,end))

    hdr = "{:9s} | ".format("")
    for idx in range(24):
        hdr += "{:>6s} ".format(rows[idx][:2])
    print("-"*len(hdr))
    print(hdr)
    print("-"*len(hdr))
    for city in dataset.keys():
        if filter and city not in filter:
            continue
        cstr = "{:9s} | ".format(city) 
        for idx in range(24):
            cstr += " {:.3f} ".format(norm_price(dataset[city][idx]))
        print(cstr)


    hdr = "{:9s}  ".format("")
    for idx in range(24,30):
        hdr += " {:>9s}  ".format(rows[idx])
    print("-"*len(hdr))
    print(hdr)
    print("-"*len(hdr))
    for city in dataset.keys():
        if filter and city not in filter:
            continue
        cstr = "{:9s} | ".format(city)
        for idx in range(24,30):
            cstr += "{:s}{:>.3f}  ".format(" "*5,norm_price(dataset[city][idx]))
        print(cstr)


def main():
    """
    mainloop
    """
    parser = argparse.ArgumentParser(description="Track packages via Posten/Bring's API")
    parser.add_argument("-f", "--file",
                        dest='file',
                        metavar="FILE",
                        help="Store .js-file to parse (for testing/dev)")
    parser.add_argument("-c", "--city",
                        dest='city',
                        help="Only display city")

    args = parser.parse_args()
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as jsonfd:
            jsonset = json.load(jsonfd)
    else:
        jsonset = grab_json()

    start, end, dataset = parse_json(jsonset)

    pretty_print(start, end, dataset, args.city)


if __name__ == "__main__":
    main()
