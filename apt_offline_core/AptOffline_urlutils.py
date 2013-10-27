#!/usr/bin/env python3
#
# urlutils.py - Simplified urllib handling
#
#   Written by Chris Lawrence <lawrencc@debian.org>
#   (C) 1999-2006 Chris Lawrence
#
# This program is freely distributable per the following license:
#
##  Permission to use, copy, modify, and distribute this software and its
##  documentation for any purpose and without fee is hereby granted,
##  provided that the above copyright notice appears in all copies and that
##  both that copyright notice and this permission notice appear in
##  supporting documentation.
##
##  I DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING ALL
##  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL I
##  BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY
##  DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
##  WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,
##  ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
##  SOFTWARE.
#
# Version 3.35; see changelog for revision history

import http.client
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import getpass
import re
import socket
import subprocess
import os
import sys
from .AptOffline_reportbug_exceptions import *
try:
    import webbrowser
except:
    webbrowser = None

UA_STR = 'reportbug/3.35 (Debian)'

def decode (page):
    "gunzip or deflate a compressed page"
    #print page.info().headers
    encoding = page.info().get("Content-Encoding") 
    if encoding in ('gzip', 'x-gzip', 'deflate'):
        from io import StringIO
        # cannot seek in socket descriptors, so must get content now
        content = page.read()
        if encoding == 'deflate':
            import zlib
            fp = StringIO(zlib.decompress(content))
        else:
            import gzip
            fp = gzip.GzipFile('', 'rb', 9, StringIO(content))
        # remove content-encoding header
        headers = http.client.HTTPMessage(StringIO(""))
        ceheader = re.compile(b"(?i)content-encoding:")
        for h in list(page.info().keys()):
            if not ceheader.match(h):
                headers[h] = page.info()[h]
        newpage = urllib.addinfourl(fp, headers, page.geturl())
        # Propagate code, msg through
        if hasattr(page, 'code'):
            newpage.code = page.code
        if hasattr(page, 'msg'):
            newpage.msg = page.msg
        return newpage
    return page

class HttpWithGzipHandler (urllib.request.HTTPHandler):
    "support gzip encoding"
    def http_open (self, req):
        return decode(urllib.request.HTTPHandler.http_open(self, req))

if hasattr(http.client, 'HTTPS'):
    class HttpsWithGzipHandler (urllib.request.HTTPSHandler):
        "support gzip encoding"
        def http_open (self, req):
            return decode(urllib.request.HTTPSHandler.http_open(self, req))

class handlepasswd(urllib.request.HTTPPasswordMgrWithDefaultRealm):
    def find_user_password(self, realm, authurl):
        user, password = urllib.request.HTTPPasswordMgrWithDefaultRealm.find_user_password(self, realm, authurl)
        if user is not None:
            return user, password

        user = input('Enter username for %s at %s: ' % (realm, authurl))
        password = getpass.getpass(
            "Enter password for %s in %s at %s: " % (user, realm, authurl))
        self.add_password(realm, authurl, user, password)
        return user, password

_opener = None
def urlopen(url, proxies=None, data=None):
    global _opener

    if not proxies:
        proxies = urllib.request.getproxies()

    headers = {'User-Agent': UA_STR,
               'Accept-Encoding' : 'gzip;q=1.0, deflate;q=0.9, identity;q=0.5'}

    req = urllib.request.Request(url, data, headers)

    proxy_support = urllib.request.ProxyHandler(proxies)
    if _opener is None:
        pwd_manager = handlepasswd()
        handlers = [proxy_support,
            urllib.request.UnknownHandler, HttpWithGzipHandler,
            urllib.request.HTTPBasicAuthHandler(pwd_manager),
            urllib.request.ProxyBasicAuthHandler(pwd_manager),
            urllib.request.HTTPDigestAuthHandler(pwd_manager),
            urllib.request.ProxyDigestAuthHandler(pwd_manager),
            urllib.request.HTTPDefaultErrorHandler, urllib.request.HTTPRedirectHandler,
        ]
        if hasattr(http.client, 'HTTPS'):
            handlers.append(HttpsWithGzipHandler)
        _opener = urllib.request.build_opener(*handlers)
        # print _opener.handlers
        urllib.request.install_opener(_opener)

    return _opener.open(req)

# Global useful URL opener; returns None if the page is absent, otherwise
# like urlopen
def open_url(url, http_proxy=None):
    proxies = urllib.request.getproxies()
    if http_proxy:
        proxies['http'] = http_proxy

    try:
        page = urlopen(url, proxies)
    except urllib.error.HTTPError as x:
        if x.code in (404, 500, 503):
            return None
        else:
            raise
    except (socket.gaierror, socket.error, urllib.error.URLError) as x:
        raise NoNetwork
    except IOError as data:
        if data and data[0] == 'http error' and data[1] == 404:
            return None
        else:
            raise NoNetwork
    except TypeError:
        print("http_proxy environment variable must be formatted as a valid URI", file=sys.stderr)
        raise NoNetwork
    return page

def launch_browser(url):
    if not os.system('command -v sensible-browser &> /dev/null'):
        cmd = 'sensible-browser' + subprocess.mkarg(url)
        os.system(cmd)
        return

    if webbrowser:
        webbrowser.open(url)
        return

    X11BROWSER = os.environ.get('X11BROWSER', 'mozilla-firefox')
    CONSOLEBROWSER = os.environ.get('CONSOLEBROWSER', 'lynx')

    if ('DISPLAY' in os.environ and
        not os.system('command -v '+X11BROWSER+' &> /dev/null')):
        cmd = "%s %s &" % (X11BROWSER, subprocess.mkarg(url))
    else:
        cmd = "%s %s" % (CONSOLEBROWSER, subprocess.mkarg(url))

    os.system(cmd)

if __name__ == '__main__':
    page = open_url('http://bugs.debian.org/reportbug')
    content = page.read()
    print(page.info().headers)
