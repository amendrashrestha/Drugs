import traceback

import model.connect as conn

def group_concat():
    connect = conn.conn_db()
    sql = "set GLOBAL group_concat_max_len = 10000000000000"
    connect.execute(sql)

'''Getting users posted more than or equal to 60 posts on each year'''

def get_extreme_users(table_name):
    try:
        connect = conn.conn_db()
        sql = "select distinct user from " + table_name
        connect.execute(sql)

        return [user['user'] for user in connect.fetchall()]

    finally:
        connect.close()


def get_normal_users(table_name):
    try:
        connect = conn.conn_db()
        sql = "SELECT T1.user FROM " + table_name + " T1 " \
              "LEFT JOIN tbl_extreme_adopters_info T2 " \
              "ON T1.user = T2.user " \
              "WHERE T2.user is NULL " \
              "group by T1.user " \
              "having count(*) >= 60 " \
              "limit 700"

        connect.execute(sql)

        return [str(user['user']) for user in connect.fetchall()]

    finally:
        connect.close()

def get_user_post(user):
    try:
        connect = conn.conn_db()
        post = []

        sql = "SELECT Text FROM tbl_flashback_posts_user_day " \
              "where user = " + "\'" + user + "\'"

        connect.execute(sql)

        for text in connect.fetchall():
            post.append(text['Text'])

        return ''.join(post)

    finally:
        connect.close()