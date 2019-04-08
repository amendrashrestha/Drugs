import codecs
import unidecode

import warnings
from functools import reduce

import re
import nltk

warnings.filterwarnings('ignore')

import utility.IOProperties as props

def read_file(filepath):
    with open(filepath) as content:
        return content.read().splitlines()

def read_codecs_file(filepath):
    with codecs.open(filepath, 'rb', encoding='ISO-8859-1') as content:
        text = unidecode.unidecode(content.read())
        text = re.sub(r'[^\x00-\x7f]',r'', text)
        return text

def write_list_in_file(filepath, features):
    with open(filepath, 'a') as outtsv:
        features = '\t'.join(features)
        outtsv.write(features+"\n")

def cleanText(post):
    replace_punctu = ("’", "'"), ("‘", "'"), ('“', '"'), ('”', '"'), ('—', '-'), ('…', '.'), ('\r', ' '), ('\n', ' ')
    return reduce(lambda a, kv: a.replace(*kv), replace_punctu, post)


# returns features and features header
def feature_vector_items():
    text_length = ['text_length']
    word_size = ['word_size']
    user_id = ['user_id']
    date = ['date']

    word_lengths = [str(x) for x in list(range(1, 21))]
    characters = list('abcdefghijklmnopqrstuvwxyz')
    digits = [str(x) for x in list(range(0, 10))]
    symbols = list('.?!,;:()"-\'')

    pos_tags = pos_header()
    function_words = read_file(props.FUNCTION_WORDS_FILEPATH)

    word_length_header = ['word_length_'+x for x in word_lengths]
    digits_header = [str('digit_'+x) for x in digits]

    symbols_header = ['dot', 'question_mark', 'exclamation', 'comma', 'semi_colon', 'colon', 'left_bracket',
              'right_bracket', 'double_inverted_comma', 'hypen', 'single_inverted_comma']

    header_feature = user_id + date + word_size + text_length + characters + word_length_header + digits_header + symbols_header  + pos_tags + function_words

    features = user_id + date + word_size + text_length + characters + word_lengths + digits + symbols + pos_tags + function_words

    # return user_id, date, word_size, text_length, characters, word_lengths, digits, symbols_header, pos_tags, features, header_feature
    return features, header_feature

# returns POS tagger header
def pos_header():
    header_wo_punct = []
    pos_tags = list(nltk.data.load('help/tagsets/upenn_tagset.pickle').keys())

    for single_pos_head in pos_tags:
        if single_pos_head.isalpha():
            header_wo_punct.append(single_pos_head)

    return sorted(header_wo_punct)