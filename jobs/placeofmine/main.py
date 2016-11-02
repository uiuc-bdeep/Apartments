#!/usr/bin/env python

import urllib2
import base64
import datetime
import os
import csv
import logging

from bdeep.context import generateOutputPath, getJobArgs

log = logging.getLogger("BDEEP")

# url: the url of the csv to grab
# string filePath: the path of the CSV to append to
# username: usename sign in
# password: password sign in
# removeHeader: if True, will remove the first line of url's CSV because its the header
def concat(url, filePath, username="", password="", removeHeader=False):

    log.info("Making request")

    request = urllib2.Request(url)
    if(not username=="" and not password==""):
        base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
    response = urllib2.urlopen(request)

    if(not os.path.exists(filePath)):
        removeHeader=False

    log.info("Reading CSV")
    csvIn = csv.reader(response.read().splitlines())
    fileNameTokens = filePath.split('.')
    fileNameTokens[-2] += datetime.datetime.now().strftime("_%H-%M_%d-%m-%y")

    log.info("Writing CSV")
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

    log.info("Finished Successfully")

args = getJobArgs()

url = args['url']
outputCSV = generateOutputPath(args['outputCSV'])
username = args['username']
password = args['password']

'''
url="http://samplecsvs.s3.amazonaws.com/Sacramentorealestatetransactions.csv"
pathOfCSV=      "/Users/dimyr7/code/python/BDEEP/csvConcat/rents.csv"
username=""
password=""
'''
concat(url, outputCSV, username, password, True)
