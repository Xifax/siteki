詩的なパーサー<br />
Little utility for parsing Japanese texts/lyrics into words list.

---

Launch:

    pythonw siteki.pyw

Notes:

* Runs under **Python** *(preferably 2.6.6)*
* Requires **PyQt** 4.8.1
* Requires **MeCab** binaries
* Makes use of cjktools and cjktools-data packages
* MeCab *(python module)* inside
* Run *./src/install.py* to swiftly download all required packages, PyQt and MeCab
* Pretty fonts included: *./res/fonts*
* MeCab morphological analysis quite often turns up inappropriate parsing, beware *(same problem with igo, apparently)*
* Stores config data in */home/user/.siteki.ini*

How to use:

1. launch
2. paste some (coherent) Japanese text from txt or html *(e.g. /res/data/sample)*
3. click parse/pdf *(first call may take some time to load edict dictionary)*
4. print resulting document or save to pdf file