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
* Pretty Japanese fonts included: *./res/fonts*
* MeCab morphological analysis quite often turns up inappropriate parsing, be aware *(same problem with igo, apparently)*
* Stores config data in */home/user/.siteki.ini*
* As of yet, due to uromkan glitches there is no romaji/kana conversion *(use IME instead)*
* Corpus frequencies are normalised by sequential numbers, not by their actual frequency values

How to use:

1. launch
* paste some (coherent) Japanese text from txt or html *(e.g. /res/data/sample)*
 - adjust font family/size as you see fit
 - specify excluded items manually or using frequency range
* click parse/pdf *(first call may take some time to load edict dictionary)*
* print resulting document or save it to pdf file