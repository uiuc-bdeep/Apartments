#!/usr/bin/env python

import urllib2
import base64
import datetime
import os
import csv
import sys

# url: the url of the csv to grab
# string filePath: the path of the CSV to append to
# username: usename sign in
# password: password sign in
# removeHeader: if True, will remove the first line of url's CSV because its the header

def concat(url, filePath, username="", password="", removeHeader=False):

    print "Getting POM data..."
    request = urllib2.Request(url)
    if(not username=="" and not password==""):
        base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
    response = urllib2.urlopen(request)

    if(not os.path.exists(filePath)):
        removeHeader=False

    csvIn = csv.reader(response.read().splitlines())
    fileNameTokens = filePath.split('.')
    fileNameTokens[-2] += datetime.datetime.now().strftime("_%H-%M_%d-%m-%y")

    print "Writing new CSV..."
    csvFile = csv.writer(open('.'.join(fileNameTokens), "w"))

    firstline = True
    today = datetime.date.today()
    todayStr = "{:%m-%d-%Y}".format(today)
    for i in csvIn:
        if firstline and (not  removeHeader):
            csvFile.writerow(i + ['Date Added'])
            firstline = False
            continue
        if firstline and removeHeader:
            firstline = False
            continue
        csvFile.writerow(i + [todayStr])
    print "Completed retrieval successfully."

if len(sys.argv) < 5:
    print "Usage: python main.py placeofmine_url output_csv_path username password"
    sys.exit(1)

url = sys.argv[1]
outputCSV = sys.argv[2]
username = sys.argv[3]
password = sys.argv[4]

concat(url, outputCSV, username, password, True)
