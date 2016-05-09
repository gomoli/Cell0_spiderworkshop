def geturl(url, data=None, headers=None, tries=3, timeout=5, gZip=False):
    """Try to fetch the URL 'url' (default = 'GET')
    -header- and postdata can be supplied (expects a dictionary)
    -gZip can be enabled to uncompress gzip data (.gz files)
    -tries specifies the number of attempts that should be made to retrieve the page
    -timeout specifies the number of seconds to wait between tries

    If data is set, POST the URL with the data
    By default the following user-agent is supplied: Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)
    Optionally, a CookieJar to be used can be created by calling init_cookiejar()
    """
    if not headers:
        headers = {}
    if 'User-Agent' not in headers:
        headers[ 'User-Agent' ] = 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)'

    req = None
    if isinstance(data, dict):
        req = urllib2.Request(url, urllib.urlencode(data), headers=headers)
    else:
        req = urllib2.Request(url, data, headers=headers)

    # try to open the webservice
    maxtries = tries
    while maxtries > 0:
        maxtries -= 1
        try:
            ufp = urllib2.urlopen(req)
        except Exception, inst:
            sys.stderr.write("There was an exception trying to open url %s\nError: %s\n" % (url, inst))
        else:
                # Decompress the file if gzip is enabled
            if gZip == True:
                ufp = gzip.GzipFile(fileobj = StringIO.StringIO(ufp.read()))
            break

        sys.stderr.write("Sleeping for %d seconds\n" % timeout)
        if maxtries != 0:
            time.sleep(timeout)
        else:
            sys.stderr.write("Giving up\n")
            return None

    return ufp
