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
