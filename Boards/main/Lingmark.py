import time
import nltk
from readcalc import readcalc

import utilities.utilities as util

class Lingmark:

    def __init__(self, data_type, fv_filepath, features, dict_english, dict_exact_match, dict_starts_with, dict_ends_with, dict_phrase, has_phrase_three, post):
        self.post = post
        self.data_type = data_type
        self.fv_filepath = fv_filepath
        self.features = features
        self.dict_english = dict_english
        self.dict_exact_match = dict_exact_match
        self.dict_starts_with = dict_starts_with
        self.dict_ends_with = dict_ends_with
        self.dict_phrase = dict_phrase
        self.has_phrase_three = has_phrase_three

        self.count_linkgmark()

    def count_linkgmark(self):
        acutal_search_time = time.time()
        output = {}

        phrase_two = ''
        phrase_three = ''

        for val in self.features[1:]:
            output.__setitem__(val, 0)

        for username, input_file_words in self.post.items():
            # input_file_words = '): ability? proficiency identical skin "before" this is. !!!!'
            # Text Readability Test
            calc = readcalc.ReadCalc(input_file_words.lower())
            LIX_index = calc.get_lix_index()
            Flesch_Kincaide_score = calc.get_flesch_kincaid_grade_level()

            input_file_words = util.clean_text(input_file_words.lower()).split()

            post_size = input_file_words.__len__()
            # Part of Speech tagger
            POS = nltk.FreqDist([b for (a, b) in nltk.pos_tag(input_file_words)])

            i = 0

            for word in input_file_words:
                # word_len = word.__len__()
                if (i >= 1):
                    phrase_two = input_file_words[i-1] + ' ' + input_file_words[i]
                if not self.has_phrase_three:
                    if (i >=2):
                        phrase_three = input_file_words[i-2] + ' ' + input_file_words[i-1] +  ' ' +input_file_words[i]

                i = i + 1
                flag = False
                if word in self.dict_english:
                    # print('dict_english:', word)
                    tmp_basic_word_list = self.dict_english.__getitem__(word)
                    # print('dict_english:',dict_english.get(word))

                    for val in tmp_basic_word_list:
                        output.__setitem__(val, output.__getitem__(val) + 1)
                        flag = True


                if not flag:
                    exactFlag = False
                    if word in self.dict_exact_match:
                        # print('dict_exact_match:', word)
                        # print('dict_exact_match:',dict_exact_match.get(word)._dict_name)
                        tmp_basic_word_list = self.dict_exact_match.__getitem__(word).dictname

                        for val in tmp_basic_word_list:
                            output.__setitem__(val, output.__getitem__(val) + 1)

                    if not exactFlag:
                        startFlag = False
                        # find words end with *
                        temp_char = ''
                        for single_char in word:
                            temp_char = temp_char + single_char
                            # print(temp_char)
                            val = self.dict_ends_with.get(temp_char + '*')
                            if val is not None:
                                # print('dict_ends_with:', word)
                                # print('dict_ends_match:',dict_ends_with.get(temp_char+'*')._dict_name)
                                startFlag = True
                                for dict_name in val.dictname:
                                    output.__setitem__(dict_name, output.__getitem__(dict_name) + 1)

                        # find words start with *
                        if not startFlag:
                            temp_char = ''
                            for single_char in word[::-1]:
                                temp_char = temp_char + single_char
                                # print(temp_char)
                                val = self.dict_starts_with.get('*' + temp_char[::-1])
                                if val is not None:
                                    # print(temp_char)
                                    for dict_name in val.dictname:
                                        # print('dict_starts_with:', word)
                                        output.__setitem__(dict_name, output.__getitem__(dict_name) + 1)

                if phrase_two in self.dict_phrase:
                    tmp_basic_word_list = self.dict_phrase.__getitem__(phrase_two).dictname

                    for val in tmp_basic_word_list:
                        output.__setitem__(val, output.__getitem__(val) + 1)

                if self.has_phrase_three:
                    if phrase_three in self.dict_phrase:
                        tmp_basic_word_list = self.dict_phrase.__getitem__(phrase_three).dictname

                        for val in tmp_basic_word_list:
                            output.__setitem__(val, output.__getitem__(val) + 1)

        # ordering dict with key and stroring value scores in list
        vector = [str(round(((v/post_size) * 100), 2)) for k, v in sorted(output.items(), key=lambda x: x[0])]
        vector.insert(0,username)
        # vector.insert(0,classType)
        # vector.insert(1,str(post_size))
        # print(vector)

        util.write_list_in_file(self.fv_filepath, vector)

        print("Counting elapsed time in %s seconds: " % round(time.time() - acutal_search_time, 4))
        print('---------------------')
