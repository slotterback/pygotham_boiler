import urllib.request
from bs4 import BeautifulSoup

def getDOBBoilerData( boroNum, houseNum, houseStreet ):
    url = requestToDOBUrl( boroNum, houseNum, houseStreet )
    soup = urlToSoup( url )
    if hasDOBData( soup ):
        return extractDOBDataFromSoup( soup )
    else:
        return "Invalid Query"

def requestToDOBUrl( boroNum, houseNum, houseStreet ):
    return ("http://a810-bisweb.nyc.gov/bisweb/PropertyProfileOverviewServlet" +
            "?boro=" + str(boroNum) +
            "&houseno=" + str(houseNum) +
            "&street=" + houseStreet.replace(' ','+'))

def urlToSoup( url ):
    "Takes in URL and returns a soup object of the contents."
    webpage = urllib.request.urlopen( url )
    soup = BeautifulSoup( webpage )
    soup.unicode
    return soup

def hasDOBData( soup ):
    "Checks to see whether DEP data exist for a given application number."
    tables = soup.find_all("table")
    return tables[1].get_text().find("NO RECORD") == -1
    
def extractDOBDataFromSoup( soup ):
    """
    Takes in data structure from BeautifulSoup and parses for DOB Boiler Data.  
    We assume that the soup has been prescreened to ensure that data exist.
    """
    allUrls = soup.find_all('a')
    #get the url with the reference to the "BoilerComplianceQueryServlet".
    #There should be exactly one such url.
    for i in allUrls:
        if i['href'].find("BoilerComplianceQueryServlet") != -1:
            url = "http://a810-bisweb.nyc.gov/bisweb/" + i['href']

    soup2 = urlToSoup(url)

    boilerTables = soup2.find_all('table') 

    records = list()
    for row in boilerTables[3].find_all('tr'): #grab the table with boiler data
        records.append(row.get_text().strip('\n').split('\n'))

    return records

