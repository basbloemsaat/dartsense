from dartsense import config
import MySQLdb

connection = None


def get_connection(force=False):
    global connection
    if force or not connection:
        connection = MySQLdb.connect(
            host=config.database['host'],
            user=config.database['username'],
            passwd=config.database['password'],
            db=config.database['schema'],
            charset='utf8',
            use_unicode=True
        )
        connection.autocommit(True)

    return connection


def get_cursor(force=False):
    return get_connection(force).cursor()


def exec_sql(sql, arguments=[]):
    try:
        cur = get_cursor()
        cur.execute(sql, arguments)
    except:
        cur = get_cursor(True)
        cur.execute(sql, arguments)
    return cur


def exec_select(sql, arguments=[]):
    cur = exec_sql(sql, arguments)
    des = cur.description
    names = [d[0] for d in cur.description]
    rows = [dict(zip(names, row)) for row in cur.fetchall()]
    return rows


def exec_insert(sql, arguments=[]):
    cur = exec_sql(sql, arguments)
    return cur.lastrowid
