The status of this project is work-in-progress, meaning I am working on it, trying to find every bug and get rid of it.

Changes at this point:
- Used the 2to3 tool to convert code
- Removed unneeded whitespace
- Replaced tabs with spaces due to indentation errors
- Applied new syntax to `super()` functions. See [PEP 3135](http://www.python.org/dev/peps/pep-3135/).
- Replaced `file()` functions with `open()` according to the book [Dive into Python 3](http://getpython3.com/diveintopython3/case-study-porting-chardet-to-python-3.html#namefileisnotdefined).
- Defined regular expression patterns as byte arrays. Described [here](http://getpython3.com/diveintopython3/case-study-porting-chardet-to-python-3.html#cantuseastringpattern). Although I am not sure if this is right.
- Modified test cases, so they are run with the Python 3 interpreter.
- Added Python 3 shebang lines to every Python script to make them more Python 3 compatible.  
  Discussions about this topic were posted on [Gmane](http://comments.gmane.org/gmane.comp.python.porting/192) and [Stack Overflow](http://stackoverflow.com/questions/7670303/purpose-of-usr-bin-python3). The [PEP 394](http://www.python.org/dev/peps/pep-0394/) article also mentions it.
- Recompiled apt-offline GUI resource file, so it can be run with Python 3.
- Replaced `ord(*)` with `*`, as described [here](http://getpython3.com/diveintopython3/case-study-porting-chardet-to-python-3.html#ordexpectedstring). Not sure about this one, too. Might get reverted.
- Replaced `_func_name` with `__name__`. Read about it in the article: [What's new in Python 3.0](http://docs.python.org/3.0/whatsnew/3.0.html#operators-and-special-methods).
- Implemented the quick fix `list(map())` concerning the `map()` function. Mentioned [here](http://docs.python.org/3.0/whatsnew/3.0.html#views-and-iterators-instead-of-lists).
- Fixed critical bug where `python3 apt-offline get apt-offline.sig` and `./apt-offline get apt-offline.sig` would always result in:

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
