from dartsense import config
import MySQLdb
import sqlite3
import re

connection = None


def get_connection(force=False):
    global connection
    if force or not connection:
        if config.database['type'] == 'mysql':
            connection = MySQLdb.connect(
                host=config.database['host'],
                user=config.database['username'],
                passwd=config.database['password'],
                db=config.database['schema'],
                charset='utf8',
                use_unicode=True
            )
            connection.autocommit(True)
        else:
            connection = sqlite3.connect(config.database['file'],isolation_level=None)

    return connection


def get_cursor(force=False):
    return get_connection(force).cursor()

def sql_to_sqlite(sql):
    # replace $s with ? for sqlite
    if config.database['type'] != 'mysql':
        sql = re.sub('\\%s', '?', sql)

        if sql == 'show tables':
            sql = "select name from sqlite_master where type = 'table'"
    
    return sql

def exec_sql(sql, arguments=[]):
    sql = sql_to_sqlite(sql)
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
