from readcalc import readcalc
import math

# Text Readability Score
def return_readability_score(text):
    score = {}

    calc = readcalc.ReadCalc(text)
    score['Flesch_Kincaide'] = return_index_text(math.ceil(calc.get_flesch_reading_ease()))
    # score['LIX_index'] = return_index_text('LIX_index', math.ceil(calc.get_lix_index())) #round(calc.get_lix_index(), 2)
    # score['Chall_readability'] = return_index_text('Chall_readability', math.ceil(calc.get_dale_chall_score()))
    # score['Gunning_fog_index'] = return_index_text('Gunning_fog_index',math.ceil(calc.get_gunning_fog_index()))

    score['Greater_than_6'] = calc.get_words_longer_than_X(6)
    score['Sentences_count'] = len(calc.get_sentences())
    score['Words_count'] = len(calc.get_words())
    score['Character_count'] = len(text)
    score['Average_word_count'] = round(score['Words_count'] / score['Sentences_count'])

    return score


def return_index_text(score):
    # if index_name == 'Flesch_Kincaide':
    if 90 <= score < 100:
        # return str(score) + " (5th grade, Very easy to read. Easily understood by an average 11-year-old student.)"
        return "5th grade,The uploaded text is very easy to read. It can be easily understood by an average 11-year-old student."
    elif 80 <= score < 90:
        # return str(score) + " (6th grade, Easy to read. Conversational English for consumers.)"
        return "6th grade,The uploaded text is easy to read. It is a conversational english for consumers."
    elif 70 <= score < 80:
        return "7th grade,The uploaded text is fairly easy to read."
    elif 60 <= score < 70:
        return "8th & 9th grade,The uploaded text is in plain english. It can be easily understood by 13 to 15-year-old students."
    elif 50 <= score < 60:
        return "10th to 12th grade,The uploaded text is fairly difficult to read."
    elif 30 <= score < 50:
        return "College,The uploaded text is difficult to read."
    elif 0 <= score < 30:
        return "College graduate,The uploaded text is very difficult to read. It can be best understood by university graduates."
    else:
        return "Index error !!"
