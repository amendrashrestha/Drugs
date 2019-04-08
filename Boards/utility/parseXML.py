import os
import traceback
from bs4 import BeautifulSoup

from pymysql import escape_string

from multiprocessing import Pool
from functools import partial

import model.connect as conn
import utility.utilities as util

def init_parse_XML(table_name):

    year = ['2003','2004','2005','2006', '2007']

    for single_year in year:
        print(">>>> " + single_year + " >>>>>")
        root = os.path.join('/Users/amendrashrestha/Downloads/Data/BoardDataSet',single_year,'posts')
        # pool = Pool()

        try:
            for path, subdirs, files in os.walk(root):
                if files.__len__() > 1:
                    # For multi processing
                    # pool.map(partial(parseXML, path, table_name), files)
                    for single_file in files:
                        parseXML(path, table_name, single_file)

        except Exception:
            traceback.print_exc()


def parseXML(path, table_name, filename):
    filepath = os.path.join(path,filename)
    xml_file = util.read_codecs_file(filepath)
    y = BeautifulSoup(xml_file, "lxml")

    try:
        user = y.find("sioc:user")['rdf:about']
        user = user.split("=")[-1]
        user = user.split("#")[0]

        post_date = y.find("dcterms:created").text
        post = util.cleanText(y.find("sioc:content").text)
        post = escape_string(post)

        try:
            connect = conn.conn_db()
            sql = "insert into " + table_name + " VALUES('%s', '%s', '%s')" % (user.strip(), post_date.strip(), post)
            connect.execute(sql)
        finally:
            connect.close()

    except Exception:
        traceback.print_exc()