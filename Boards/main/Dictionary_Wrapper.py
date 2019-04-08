class DictionaryParameter:
    def __init__(self, endflag, startflag, phraseflag, wordlen, searchtext, initialtext, dictname, phraselen):
        self._endswith = endflag
        self._startswith = startflag
        self._isphrase = phraseflag
        self._wordlength = wordlen
        self._search_text = searchtext
        self._initial_text = initialtext
        self._dict_name = dictname
        self._phrase_len = phraselen

    @property
    def endswith(self):
        return self._endswith

    @property
    def startswith(self):
        return self._startswith

    @property
    def isphrase(self):
        return self._isphrase

    @property
    def wordlength(self):
        return self._wordlength

    @property
    def searchtext(self):
        return self._search_text

    @property
    def initialtext(self):
        return self._initial_text

    @property
    def dictname(self):
        return self._dict_name

    @property
    def phraselen(self):
        return self._phrase_len

    @endswith.setter
    def endswith(self, value):
        self._endswith = value

    @startswith.setter
    def startswith(self, value):
        self._startswith = value

    @isphrase.setter
    def isphrase(self, value):
        self._isphrase = value

    @wordlength.setter
    def wordlength(self, value):
        self._wordlength = value

    @searchtext.setter
    def searchtext(self, value):
        self._search_text = value

    @initialtext.setter
    def initialtext(self, value):
        self._initial_text = value

    @dictname.setter
    def dictname(self, value):
        self._dict_name = value

    @phraselen.setter
    def phraselen(self, value):
        self._phrase_len = value