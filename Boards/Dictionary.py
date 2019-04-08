import codecs
import os
import itertools
import time
import traceback

import main.Dictionary_Wrapper as dict
import utilities.utilities as util

def get_dict_word(features):
    _dictionary_all_paths = []
    # if lingmark files are inside single folder
    _dictionary_all_paths = [os.path.join(lingmark_filepath, file) for file in
                                sorted(os.listdir(lingmark_filepath)) if file not in '.DS_Store']

    # if lingmark files are inside multiple folders
    # types_lingmark = util.get_folder_name(lingmark_filepath)
    #
    # for i in types_lingmark:
    #     _dictionary_all_paths.append(util.get_files_in_folder(lingmark_filepath,i))
    #
    # _dictionary_all_paths = list(itertools.chain.from_iterable(_dictionary_all_paths))

    # Initialize all the user-defined words and phrase in four dictionary:
    _dict_exact_match = {}
    _dict_starts_with = {}
    _dict_ends_with = {}
    _dict_phrase = {}

    # Initialize all the english word dicitonary
    _english_words = codecs.open(basic_words_filepath, encoding='utf-8', mode='r').read().split()
    _dictionary_englishword = initialize_dictionary_english(_english_words)

    for single_dict in _dictionary_all_paths:
        dict_name = single_dict.split('/')[-1]
        with codecs.open(single_dict, encoding='utf-8', mode='r') as f:
            _input_list = list(set(f.read().lower().splitlines()))
            _dict_exact_match, _dict_starts_with, _dict_ends_with, _dict_phrase= \
                initialize_dictionary_user_defined(_input_list, dict_name, _dict_exact_match, _dict_starts_with, _dict_ends_with,_dict_phrase)

    # Map English Dictionary to User Dedfined Dictionary
    _dictionary_englishword = map_english_dicitonary(_dictionary_englishword, _dict_exact_match)

    # Get the maximum lenghth for all the phrases in user defined Dictionary
    has_phrase_three = has_phrase_len_three(_dict_phrase)

    return _dictionary_englishword, _dict_exact_match, _dict_starts_with, _dict_ends_with, _dict_phrase, has_phrase_three

def map_english_dicitonary(english_word_dict, exact_match_dict):
    output = english_word_dict
    for k, v in english_word_dict.items():
        dictObj = exact_match_dict.get(k)
        if dictObj is not None:
            output.__setitem__(k, dictObj.dictname)
    return output


def initialize_dictionary_english(dictionary_words):
    words_dict = {}
    for single_word in dictionary_words:
        words_dict.__setitem__(single_word.lower(),[])
    return words_dict

def has_phrase_len_three(dict_phrase):
    for val in dict_phrase.values():
        if val.phraselen == 3:
            return True
    return False


# Builds one dictionary at a time.
def initialize_dictionary_user_defined(_user_defined_words, dict_name, dict_exact_match, dict_starts_with, dict_ends_with, dict_phrase):
    for val in _user_defined_words:
        startswith = False
        endswith = False
        if val.__contains__('*'):
            startswith = True if val.startswith('*') else False
            endswith = True if val.endswith('*') else False

        isphrase = True if val.__contains__(' ') else False

        # valObj : DictionaryParameter

        if not startswith and not endswith and not isphrase:
            valObj = dict_exact_match.get(val)
        elif startswith:
            valObj = dict_starts_with.get(val)
        elif endswith:
            valObj = dict_ends_with.get(val)
        elif isphrase:
            valObj = dict_phrase.get(val)

        if valObj is not None:
            valObj.dictname.append(dict_name)
            continue

        _parent_dict = []
        _parent_dict.append(dict_name)

        parameters = dict.DictionaryParameter(endswith,
                                     startswith,
                                     isphrase,
                                     val.strip('*').__len__(),
                                     val.strip('*'),
                                     val, _parent_dict,
                                     val.split(' ').__len__() if isphrase else 0)
        # Using replace might be expensive, have to think of alternative, Also its returning 1 less size of the
        # original input value have to see why it happens. Check time analysis for using replace vs strip functionality.
        if not startswith and not endswith and not isphrase:
            dict_exact_match.__setitem__(val, parameters)
        elif startswith:
            dict_starts_with.__setitem__(val, parameters)
        elif endswith:
            dict_ends_with.__setitem__(val, parameters)
        elif isphrase:
            dict_phrase.__setitem__(val, parameters)
    return dict_exact_match, dict_starts_with, dict_ends_with, dict_phrase
