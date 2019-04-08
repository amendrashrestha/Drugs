import model.sqlScript as sql
import utility.parseXML as parser
import utility.utilities as util
import utility.IOProperties as props
import Dictionary as dict
import os

def init(parse=False):
    post_table_name = 'tbl_boards_posts_03_07_new'

    if parse:
        parser.init_parse_XML(post_table_name)

    # valid_users = sql.get_valid_users(post_table_name)
    # print(valid_users.__len__())

    # features, header = util.feature_vector_items()
    #
    # if not os.path.exists(props._fv_filepath):
    #     util.write_list_in_file(props._fv_filepath, header)


if __name__ == '__main__':
    init(parse=True)