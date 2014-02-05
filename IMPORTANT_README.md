apt-offline-python3-dev
=======================
This is apt-offline (almost) ported to Python 3.

Much testing is to be done yet and you should only use this program when you know what you are doing.

Credit goes to [Ritesh Raj Sarraf](https://github.com/rickysarraf) for creating apt-offline, [Manish Sinha](https://github.com/manish) and [Abhishek Mishra](https://github.com/ideamonk) for creating the apt-offline GUI,  
Chris Lawrence for writing several scripts (debianbts.py, reportbug_exceptions.py, urlutils.py), Jason Petrone for magic.py,  
[Kunal P. Bharati](https://github.com/kunal) for getting the GUI to work,  Steven J. Bethard for argparse, and to [Y Giridhar Appaji Nag](https://github.com/appaji) for modifications to apt-offline's manpage.

This porting project would not be possible without all the answers on Gmane, Dive into Python 3, Stack Overflow, the Python documentation and other ressources as well.

apt-offline-python3-dev was most active in October 2013, but kind of halted from there on,
because the remaining bugs are too complex for me to figure out and patch.

So here are the remaining bugs I found, which I cannot get working, despite all approaches:
- When you invoke the CLI version with Python 3.3 like so: `python3.3 apt-offline`

  You will get:
  ```
  Traceback (most recent call last):
  File "apt-offline", line 28, in <module>
    main()
  File "/apt-offline/apt_offline_core/AptOfflineCoreLib.py", line 1956, in main
    args.func(args)
AttributeError: 'Namespace' object has no attribute 'func'
  ```
  A workaround has been found, but it's not the proper way to fix this bug.
- There is a problem with the DebianBTS module. No matter, what version you are using (be it CLI or GUI), trying to download bug reports will always result in:
  `http_proxy environmental variable must be formatted as a valid URI`
- Trying to install downloaded packages leads to: `ERROR: I couldn't understand file type PKG.deb.`

If you know how to fix those bugs or want to improve the code, there are two ways you can contribute:

1. Fork this repository:
    - If you want to improve or patch one specific thing, create a topic branch like **`installpkg-patch`** and commit your changes there
    - If there are multiple fixes, work on the **`apt-offline-python3-dev`** branch
    - Send a pull request
2. Or, another way:
    - Send an email to <netcyphe@openmailbox.org> with the diff and changed files.
    - After a short review, I will implement those changes in this repository and notify you

You will of course be credited properly and mentioned as contributor.

**Run this program at your own risk. It is unstable and not tested enough.**
