The status of this project is work-in-progress, meaning I am working on it, trying to find every bug and get rid of it.

Changes at this point:

Commit [ba8662eb8e01cebc969126650baa22776a27430d](https://github.com/codingaround/apt-offline-python3-dev/commit/ba8662eb8e01cebc969126650baa22776a27430d) submitted on Sep 30, 2013:

- Used the 2to3 tool to convert code
- Replaced tabs with spaces due to indentation errors
- Recompiled apt-offline GUI resource file, so it can be run with Python 3.

Commit [70b646d8fb7b562b3a5ce0f009b9500a8ab7eae7](https://github.com/codingaround/apt-offline-python3-dev/commit/70b646d8fb7b562b3a5ce0f009b9500a8ab7eae7) submitted on Oct 14, 2013:

- Added Python 3 shebang lines to every Python script to make them more Python 3 compatible.  
  Discussions about this topic were posted on [Gmane](http://comments.gmane.org/gmane.comp.python.porting/192) and [Stack Overflow](http://stackoverflow.com/questions/7670303/purpose-of-usr-bin-python3). The [PEP 394](http://www.python.org/dev/peps/pep-0394/) article also mentions it.
- Removed unneeded whitespace
- Modified test cases, so they are run with the Python 3 interpreter.
- Replaced `file()` functions with `open()` according to the book [Dive into Python 3](http://getpython3.com/diveintopython3/case-study-porting-chardet-to-python-3.html#namefileisnotdefined).
- Defined regular expression patterns as byte arrays. Described [here](http://getpython3.com/diveintopython3/case-study-porting-chardet-to-python-3.html#cantuseastringpattern). Although I am not sure if this is right.
- Replaced `ord(*)` with `*`, as described [here](http://getpython3.com/diveintopython3/case-study-porting-chardet-to-python-3.html#ordexpectedstring). Not sure about this one, too. Might get reverted.
- Applied new syntax to `super()` functions. See [PEP 3135](http://www.python.org/dev/peps/pep-3135/).
- Replaced `_func_name` with `__name__`. Read about it in the article: [What's new in Python 3.0](http://docs.python.org/3.0/whatsnew/3.0.html#operators-and-special-methods).
- Implemented the quick fix `list(map())` concerning the `map()` function. Mentioned [here](http://docs.python.org/3.0/whatsnew/3.0.html#views-and-iterators-instead-of-lists).

Commit [0a81e988b2892431163de115f20e41e5e4245902](https://github.com/codingaround/apt-offline-python3-dev/commit/0a81e988b2892431163de115f20e41e5e4245902) submitted on Oct 17, 2013:

- Fixed bug where `python3 apt-offline get apt-offline.sig` and `./apt-offline get apt-offline.sig` would always result in:

    ````
      Traceback (most recent call last):
      File "./apt-offline", line 28, in <module>
        main()
      File "/apt-offline-python3-dev/apt_offline_core/AptOfflineCoreLib.py", line 1949, in main
        args.func(args)
      File "/apt-offline-python3-dev/apt_offline_core/AptOfflineCoreLib.py", line 539, in fetcher
        (ItemURL, ItemFile, ItemSize, ItemChecksum) = stripper(item)
      File "/apt-offline-python3-dev/apt_offline_core/AptOfflineCoreLib.py", line 339, in stripper
        url = str.rstrip(str.lstrip(''.join(item[0]), chars="'"), chars="'")
    TypeError: lstrip() takes no keyword arguments
    ````

    As I could not find out the real cause of this issue, I found out two solutions mentioned in [this](https://github.com/codingaround/apt-offline-python3-dev/blob/master/apt_offline_core/bugfix_examples.py) file.  
    The first solution was implemented.
    
    In my research of this bug most clues point to a [question](http://stackoverflow.com/q/11716687) posted on Stack Overflow.  
    Another similar question was asked [here](http://stackoverflow.com/questions/13217056/python-accepts-keyword-arguments-in-cpython-functions).  
    Like the OP mentioned, he could reproduce the bug in Python 2 and Python 3.  
    The problem he mentioned occured when using a [string method](http://docs.python.org/3.2/library/stdtypes.html?highlight=str.lstrip#string-methods).  
    2 symptoms, which are identical.
    
    And here are the results of running the line of code in both Python versions:

    **Python 2**
    
    ````
    Python 2.7.3 (default, Sep 26 2013, 20:03:06) 
    [GCC 4.6.3] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> item = ["foo", "bar"]
    >>> str.rstrip(str.lstrip(''.join(item[0]), chars="'"), chars="'")
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: lstrip() takes no keyword arguments
    ````
    
    **Python 3**
    
    ````
    Python 3.2.3 (default, Sep 25 2013, 18:22:43) 
    [GCC 4.6.3] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> item = ["foo", "bar"]
    >>> str.rstrip(str.lstrip(''.join(item[0]), chars="'"), chars="'")
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: lstrip() takes no keyword arguments
    ````
    
    As you can see the problem applies to both versions.  
    So it is most likely that those two string methods don't accept keyword arguments (also take a look at these three bug reports mentioned in the questions: [Issue 1176](http://bugs.python.org/issue1176), [Issue 8350](http://bugs.python.org/issue8350), [Issue 8626](http://bugs.python.org/issue8626) and [this documentation entry](http://docs.python.org/dev/reference/expressions.html#calls)).  
    But then again, I ask myself how that could work in the Python 2 version of apt-offline.

- Moved `string.lstrip()` and `string.rstrip()` to `str.lstrip()` and `str.rstrip()`

Commit [beed00f005ccf67d34b04363fcb2a4e388a379b8](https://github.com/codingaround/apt-offline-python3-dev/commit/beed00f005ccf67d34b04363fcb2a4e388a379b8) submitted on Oct 27, 2013:

- Modified code with optional 2to3 fixers `buffer`, `idioms`, `set_literal` and `ws_comma`
- Corrected `xxx_todo_changeme` leftover by 2to3 in some files
- Changed solution 1 to solution 2 in the `TypeError: lstrip() takes no keyword arguments` bug after a discussion with [Ritesh Raj Sarraf](https://github.com/rickysarraf).
- Switched back `AptOfflineMagicLib.open` to `AptOfflineMagicLib.file`
- Fixed bug printing the error:
  ````
  Couldn't find debianbts module.
  Cannot fetch Bug Reports.
  ````
- Replaced [sgmllib](http://docs.python.org/2.7/library/sgmllib.html) module with [html.parser](http://docs.python.org/3/library/html.parser.html).  
  This is more a problem than a fix, because I hoped that `html.parser.HTMLParser` would be a proper replacement for a SGML parser taking care of malformed HTML.
- Replaced [rfc822](http://docs.python.org/2.7/library/rfc822.html) with [email](http://docs.python.org/3/library/email.html) package
- Moved `email.Errors` to `email.errors`
- Fixed `UnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 133: invalid start byte` in apt-offline-python3-dev/apt_offline_core/AptOfflineMagicLib.py, line 1109
- Replaced [htmllib](http://docs.python.org/2.7/library/htmllib.html) module with [http.client](http://docs.python.org/3/library/http.client.html) module
- Moved `urllib.getproxies()` to `urllib.request.getproxies()`
- Because PyQt4 handles `QString` objects as `str` and `unicode` objects in combination with Python 3, `isEmpty()` can't be used anymore. It was replaced with `not`.

Commit submitted on Jan 11, 2014:

- Added missing class `NoNetwork` from AptOffline_reportbug_exceptions.py
- Removed unneeded import line in AptOffline_urlutils.py