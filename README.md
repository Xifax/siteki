Little utility for parsing Japanese texts/lyrics into words list.

---

Launch:

    pythonw siteki.pyw

Notes:

* Runs under Python (preferably 2.6.6)
* Requires PyQt 4.8.1
* Also makes use of cjktools and cjktools-data
* MeCab (python module) inside
* Run ./src/install.py to swiftly download all required packages
* Fonts package included: ./res/fonts
* MeCab morphological analysis quite often turns up inappropriate parsing, beware (same problem with igo, apparently)
