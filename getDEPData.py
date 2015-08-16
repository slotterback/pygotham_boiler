import urllib.request
from bs4 import BeautifulSoup

def getDEPData( appNum ):
    url = requestToDEPUrl( appNum )
    soup = urlToSoup( url )
    if hasDEPData( soup ):
        return extractDEPDataFromSoup( soup )
    else:
        return "No Boiler Data For Given Application Number"

def requestToDEPUrl( appNum ):
    "This assumes the appNumber is known to be a valid DEP application number."
    urlPrefix = "file:///C:/DEPData/"
    appYear   = int( appNum[-2:] )
    if appYear > 65:
        return ( urlPrefix + "19xx/19" + appNum[-2] + "x/"+
                 "19" + appNum[-2:] + "/" + appNum + ".html")
    else:
        return ( urlPrefix + "20xx/20" + appNum[-2] + "x/"+
                 "20" + appNum[-2:] + "/" + appNum + ".html")

def urlToSoup( url ):
    "Takes in URL and returns a soup object of the contents."
    webpage = urllib.request.urlopen( url )
    soup    = BeautifulSoup( webpage )
    soup.unicode
    return soup

def hasDEPData( soup ):
    "Checks to see whether DEP data exist for a given application number."
    tables = soup.find_all("table")
    return tables[1].get_text().find( "NO RECORD" ) == -1
    

def extractDEPDataFromSoup( soup ):
    """
    Takes in data structure from BeautifulSoup and parses for DEP Boiler Data.  
    We assume that the soup has been prescreened to ensure that data exist.
    """
    tables = soup.find_all( "table" )

    #get premise address, boro name, BIN, block #, and lot #
    #This part has the following format:
    #'\n\n\n\r\n                PREMISES: [address] \xa0\xa0[boro name]\r\n...
    #\xa0\xa0 BIN: [BIN, last 6]\xa0\xa0BLOCK:\r\n                [block #]...
    #\xa0\xa0LOT: [lot #]\r\n            \n\n\n'
    locationData  = tables[ 1 ].get_text()
    locationData  = locationData.replace( '\n', '' )#removes '\n's
    locationData  = locationData.replace( '\r' , '' )#removes '\r's
    locDataSplit  = locationData.split( ": " )
    locDataSplit2 = locDataSplit[ 1 ].split( "\xa0" )
    appAddress    = locDataSplit2[ 0 ][ 0:-1 ]
    appBoro       = locDataSplit2[2].partition( '  ')[0]
    print( repr( locDataSplit ) )
    #check for case where BIN, Block, Lot are missing
    appBIN   = "NA"
    appBlock = "NA"
    appLot   = "NA"
    try:
        appBIN   = int( locDataSplit[2].partition( '\xa0' )[ 0 ] )
    except:
        pass
    try:
        appBlock = int( locDataSplit[3].partition( '\xa0' )[ 0 ] )
    except:
        pass
    try:
        appLot   = int( locDataSplit[4].partition( '\xa0' )[ 0 ] )
    except:
        pass
    allLocationData = [ appAddress, appBoro, appBIN, appBlock, appLot ] 

    #get DEP Application Data
    
    applicationData = tables[2].find_all("td") #Grab individual table entries.

    allDEPData = [ ( i.get_text()         #Get the text,
	              .replace('\r','')   #then remove the '\r's,
                      .replace('\n','')   #then remove the '\n's,
	              .partition(': ')[2] #then remove everything before ": ",
	              .partition('  ')[0] #and finally remove trailing spaces.
                    )
	            for i in applicationData ]
    del allDEPData[-2] #Field is known to always be empty. Remove from output.

    return allLocationData + allDEPData
