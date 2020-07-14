import app.utilities as util

# Readability test
def return_readability_score(text):
    readability_score = util.return_readability_score(text)
    flesch_readability_score = readability_score['Flesch_Kincaide'].split(',')

    if flesch_readability_score.__len__() > 1:
        grade_level = flesch_readability_score[0]
        readability_info = flesch_readability_score[1]
    else:
        grade_level = 'Unknown'
        readability_info = ''

    return readability_score, grade_level, readability_info