import traceback

import model.connect as conn

'''Getting users posted more than or equal to 60 posts on each year'''

def get_valid_users(table_name):
    try:
        connect = conn.conn_db()
        sql = "select T1.user_id, count(*) as user_count from (select user_id, YEAR(post_date) as post_year, " \
              "count(*) as count from " + table_name + " group by user_id, post_year having count >= 60) T1 " \
              "group by T1.user_id having user_count = 5 order by 1"

        connect.execute(sql)

        return [str(user['user_id']) for user in connect.fetchall()]

    finally:
        connect.close()

# def get_user_fv(table_name, user_id):
#     try:
#         connect = conn.conn_db()
#         sql =
#
#         connect.execute(sql)
#
#         return [user['user_id'] for user in connect.fetchall()]
#
#     except Exception:
#         traceback.print_exc()