from bs4 import BeautifulSoup
import urllib.request

siteBase = "https://a826-web01.nyc.gov/DEP.BoilerInformationExt/Home/Success/"
pathBase = "C:/DEPData/"
for year in range( 1965, 2016 ):
    siteEnd = str( year % 100 ).zfill( 2 )
    pathPrefix = ( pathBase + str( year // 100 ) + "xx/" +
                   str( year // 10 ) + "x/" + str( year ) + "/" )
    for i in range(1,5):
        if year < 2000:
            mySite = siteBase + "CA" + str( i ).zfill( 4 ) + siteEnd
            page = urllib.request.urlopen( mySite )
            soup = BeautifulSoup( page.read() )
            f = open( pathPrefix +
                      "CA" + str( i ).zfill( 4 ) + siteEnd + ".html", "w" )
            f.write( str( soup ) )
            f.close
        if year >= 2000:
            mySite = siteBase + "CB" + str( i ).zfill( 4 ) + siteEnd
            page = urllib.request.urlopen( mySite )
            soup = BeautifulSoup( page.read() )
            f = open( pathPrefix +
                      "CB" + str( i ).zfill( 4 ) + siteEnd + ".html", "w" )
            f.write( str( soup ) )
            f.close
        if year > 2011:
            mySite = siteBase + "CR" + str( i ).zfill( 4 ) + siteEnd
            page = urllib.request.urlopen( mySite )
            soup = BeautifulSoup(page.read())
            f = open( pathPrefix +
                      "CR" + str( i ).zfill( 4 ) + siteEnd + ".html", "w" )
            f.write( str( soup ) )
            f.close
        if year > 2014:
            mySite = siteBase + "CW" + str( i ).zfill( 4 ) + siteEnd
            page = urllib.request.urlopen( mySite )
            soup = BeautifulSoup( page.read() )
            f = open( pathPrefix +
                      "CW" + str( i ).zfill( 4 ) + siteEnd + ".html", "w" )
            f.write( str( soup ) )
            f.close

