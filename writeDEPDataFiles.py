import urllib.request
import csv
from bs4 import BeautifulSoup
from getDEPData import *

urlBase = "file:///C:/DEPData/"
outputPathBase = "C:/"

def tryAndAddDEPApplication( urlPrefix, appPrefix, i, urlSuffix, data ):
    url = urlPrefix + appPrefix + str(i).zfill(4) + urlSuffix
    try:
        soup = urlToSoup(url)
        if hasDEPData( soup ):
            print( appPrefix, str(i).zfill(4), appYearYY, sep = '')
            data.writerow( extractDEPDataFromSoup(soup) )
    except:
        pass

for appYear in range( 1965, 2016 ):

    appYearYYxx = str( appYear // 100 ) + "xx"
    appYearYYYx = str( appYear // 10  ) + "x"
    appYearYY   = str( appYear %  100 ).zfill(2)

    outputPath = outputPathBase
    urlPrefix = urlBase + appYearYYxx + "/" + appYearYYYx + "/" + str(appYear) + "/"
    urlSuffix = appYearYY + ".html"

    f = open(outputPath + "Applications" + str(appYear) + ".csv", "w", newline = '')
    data = csv.writer(f)
    data.writerow(["Building Address", "Boro", "BIN", "Block", "Lot",
                "Application Number", "Application Type", "Owner",
                "Issue Date", "Expiration Date", "Application Status",
                "Boiler Make and Model", "Primary Fuel", "Secondary Fuel",
                "Burner Make and Model", "Number of Identical Units",
                "Building Alias"])

    for i in range(1,5000):
        
        if appYear < 2000:
            tryAndAddDEPApplication( urlPrefix, "CA", i, urlSuffix, data )
        else:
            tryAndAddDEPApplication( urlPrefix, "CB", i, urlSuffix, data )
            if appYear > 2011:
                tryAndAddDEPApplication( urlPrefix, "CR", i, urlSuffix, data )
                if appYear < 2015:
                    tryAndAddDEPApplication( urlPrefix, "CW", i, urlSuffix, data )
    del data
    f.close()
