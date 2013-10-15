This project is work-in-progress, meaning I am working on it, trying to find every bug and get rid of it.

Changes at this point:
- Used 2to3 to convert code
- Removed unneeded whitespace
- Replaced tabs with spaces due to indentation errors
- Applied new syntax to super() functions see [PEP 3135](http://www.python.org/dev/peps/pep-3135/)
- Replaced file() function with open() according to the book [Dive into Python3](http://getpython3.com/diveintopython3/case-study-porting-chardet-to-python-3.html#namefileisnotdefined)
- Defined regular expression patterns as byte arrays. Described [here](http://getpython3.com/diveintopython3/case-study-porting-chardet-to-python-3.html#cantuseastringpattern). Although I am not sure if this is right.
- Modified test cases, so they are run with the Python 3 interpreter
- Added Python 3 Shebang line to every Python script, to make this ported version more Posix compliant 
- Recompiled apt-offline GUI resource file, so it can be run with Python 3
- Replaced ord(*) with *, as described [here](http://getpython3.com/diveintopython3/case-study-porting-chardet-to-python-3.html#ordexpectedstring). Not sure about this one, too. Might get reverted.
- Replaced _func_name with __name__ Read [What's new in Python 3.0](http://docs.python.org/3.0/whatsnew/3.0.html#operators-and-special-methods)
- Implemented a quick list fix regarding map(): list(map()) Mentioned [here](http://docs.python.org/3.0/whatsnew/3.0.html#views-and-iterators-instead-of-lists)
