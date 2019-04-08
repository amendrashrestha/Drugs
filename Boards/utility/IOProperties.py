import os
import sys
from os.path import expanduser

APP_ROOT = os.path.dirname(sys.modules['__main__'].__file__)
USER_HOMEPATH = expanduser("~")

USER_DATA_FILEPATH = os.path.join(USER_HOMEPATH, 'Downloads','BoardDataSet','Posts_All_GT_60')

FUNCTION_WORDS_FILEPATH = os.path.join(APP_ROOT, 'files','lingmarks','Function.txt')

_fv_filepath = os.path.join(APP_ROOT,'files','fv','feature_vector.tsv')