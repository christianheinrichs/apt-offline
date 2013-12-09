# This file will be removed soon

# Solution 1:
# The keyword arguments chars="'" and chars="\n" were replaced by "'" and "\n".

def stripper(item):
        '''Strips extra characters from "item".
        Breaks "item" into:
        url - The URL
        file - The actual package file
        size - The file size
        checksum - The checksum string
        and returns them.'''

        item = item.split(' ')
        log.verbose("Item is %s\n" % (item) )

        url = str.rstrip(str.lstrip(''.join(item[0]), "'"), "'")
        file = str.rstrip(str.lstrip(''.join(item[1]), "'"), "'")
        try:
                size = int(str.rstrip(str.lstrip(''.join(item[2]), "'"), "'"))
        except ValueError:
                log.verbose("%s is malformed\n" % (" ".join(item) ) )
                size = 0

        # INFO: md5 ends up having '\n' with it.
        # That needs to be stripped, too.
        try:
                checksum = string.rstrip(string.lstrip(''.join(item[3]), "'"), "'")
                checksum = string.rstrip(checksum, "\n")
        except IndexError:
                if item[1].endswith("_Release") or item[1].endswith("_Release.gpg"):
                        checksum = None
        return url, file, size, checksum

# Solution 2:
# In this solution, chars is a variable defined as a list.
# Its contents are then accessed with either chars[0] or chars[1].

def stripper(item):
        '''Strips extra characters from "item".
        Breaks "item" into:
        url - The URL
        file - The actual package file
        size - The file size
        checksum - The checksum string
        and returns them.'''

        chars = ["'", "\n"]

        item = item.split(' ')
        log.verbose("Item is %s\n" % (item) )

        url = str.rstrip(str.lstrip(''.join(item[0]), chars[0]), chars[0])
        file = str.rstrip(str.lstrip(''.join(item[1]), chars[0]), chars[0])
        try:
                size = int(str.rstrip(str.lstrip(''.join(item[2]), chars[0]), chars[0]))
        except ValueError:
                log.verbose("%s is malformed\n" % (" ".join(item) ) )
                size = 0

        # INFO: md5 ends up having '\n' with it.
        # That needs to be stripped, too.
        try:
                checksum = string.rstrip(string.lstrip(''.join(item[3]), chars[0]), chars[0])
                checksum = string.rstrip(checksum, chars[1])
        except IndexError:
                if item[1].endswith("_Release") or item[1].endswith("_Release.gpg"):
                        checksum = None
        return url, file, size, checksum
