#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import sys
import time
import ConfigParser
import psycopg2
import multiprocessing
import psycopg2.extensions as ext

from dbfpy import dbf

module_name = 'energosite_'


def getConfigValue(option):
    return config.get('Base', option)


def connectDB(autocommit=True):
    dbConnection = psycopg2.connect(host=getConfigValue("host"), database=getConfigValue("database"),
                                    user=getConfigValue("user"), password=getConfigValue("password"))
    if autocommit:
        dbConnection.set_isolation_level(ext.ISOLATION_LEVEL_AUTOCOMMIT)
    else:
        dbConnection.set_isolation_level(ext.ISOLATION_LEVEL_SERIALIZABLE)
    return dbConnection


def setAutocommit(conn, ac):
    if ac:
        conn.set_isolation_level(ext.ISOLATION_LEVEL_AUTOCOMMIT)
    else:
        conn.set_isolation_level(ext.ISOLATION_LEVEL_SERIALIZABLE)
    return conn


def fileExists(fileName):
    if not os.path.isfile(fileName):
        return False
    else:
        return True


def getValidFieldName(name):
    if name.lower() == "saldok":
        return "saldo_k"
    elif name.lower() == "saldo_ka":
        return "saldoka"
    elif name.lower() == "fio1":
        return "fio"
    elif name.lower() == "summa":
        return "opl"
    elif name.lower() == "dkw":
        return "dat_kv"
    elif name.lower() == "ostatok":
        return "dolg"
    else:
        return name.lower()


def deleteData(conn, dbtable, day, month, year, department_id):
    formats = []
    if dbtable == "oplbaza":
        dateCondition = "to_number(to_char(data, '{0}'), '99') = {1} "
        if day:
            formats.append(dateCondition.format('DD', day))
        if month:
            formats.append(dateCondition.format('MM', month))
        if year:
            formats.append(dateCondition.format('YY', year % 100))
    elif dbtable == 'kvitbaza':
        if month:
            formats.append('nmes = {0}'.format(month))
        if year:
            formats.append('god % 100 = {0}'.format(year % 100))
    else:
        return

    formats.append("department_id={0}".format(department_id))
    if not formats:
        return
    sql = "delete from {0} where {1}".format(module_name + dbtable, " and ".join(formats))
    # conn = connectDB(autocommit=True)
    setAutocommit(conn, True)
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()


def clearDBTable(conn, tabname, department_id=None):
    if department_id:
        sql = "delete from {0} where department_id={1}".format(module_name + tabname, department_id)
    else:
        sql = "delete from {0}".format(module_name + tabname)
    # conn = connectDB(autocommit=True)
    setAutocommit(conn, True)
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()


def insertData(fileName, dbTable, charset, department_id):
    current_proc = multiprocessing.current_process()
    print 'Starting:', current_proc.name, current_proc.pid
    sys.stdout.flush()

    dbfFName = os.path.join(PROJECT_PATH, "baza", fileName)
    if not fileExists(dbfFName):
        return

    conn = connectDB(autocommit=False)
    cursor = conn.cursor()

    DbfFile = dbf.Dbf(dbfFName)
    dbFieldNames = [getValidFieldName(name) for name in DbfFile.fieldNames]
    dbFieldNames.append('department_id')
    params = ['%s'] * len(dbFieldNames)
    for rec in DbfFile:
        select = "insert into {0}({1}) values({2}) ".format(module_name + dbTable, ", ".join(dbFieldNames),
                                                            ", ".join(params))
        values = [str(rec[name]).strip().decode(charset).encode('utf8') for name in DbfFile.fieldNames]
        values.append(str(department_id))
        try:
            cursor.execute(select, values)
        except psycopg2.Error:
            print("Error inserting to " + dbTable + " from " + fileName + " for department_id=" + str(department_id))
            sys.stdout.flush()
            continue

    conn.commit()
    DbfFile.close()
    cursor.close()
    conn.close()

    print 'Exiting :', current_proc.name, current_proc.pid
    sys.stdout.flush()


def serviceDB(conn):
    # conn = connectDB(autocommit=True)
    setAutocommit(conn, True)
    cursor = conn.cursor()
    cursor.execute('vacuum full freeze analyze')
    cursor.execute('reindex database {0}'.format(getConfigValue('database')))
    cursor.close()


def setSeqVal(conn, dbTable):
    # connection = connectDB(autocommit=True)
    setAutocommit(conn, True)
    cursor = conn.cursor()
    cursor.execute("select id from {0} order by id desc limit 1;".format(module_name + dbTable))
    id_result = cursor.fetchone()
    if not id_result:
        rowId = 1
    else:
        rowId = id_result[0]
    cursor.execute("SELECT setval('{0}_id_seq', {1}, true);".format(dbTable, rowId))
    cursor.close()


def updateActualDate(conn, department_id, dbTable, actual_date):
    # connection = connectDB(autocommit=True)
    cursor = conn.cursor()
    select = "select * from energosite_actualdate where department_id={0} and dbtable='{1}' limit 1".format(
        department_id, dbTable)
    cursor.execute(select)
    id_result = cursor.fetchone()
    if id_result:
        upd_select = "update energosite_actualdate set actual_date='{0}' where department_id={1} and dbtable='{2}'".format(
            actual_date, department_id, dbTable)
        cursor.execute(upd_select)
    else:
        insert_select = "insert into energosite_actualdate (actual_date, department_id, dbtable) values ('{0}', {1}, '{2}')".format(
            actual_date, department_id, dbTable)
        cursor.execute(insert_select)
    cursor.close()


def deleteDBFiles():
    directory = os.path.join(PROJECT_PATH, "baza")
    for filename in os.listdir(directory):
        fullPath = os.path.join(directory, filename)
        if os.path.isfile(fullPath):
            tableName, extension = os.path.splitext(filename)
            if extension.lower() in ('.dbf', '.txt', '.csv'):
                try:
                    os.remove(fullPath)
                except OSError:
                    pass


def walkTables(conn):
    processes = []
    # connection = connectDB()
    cursor = conn.cursor()
    cursor.execute(
        "select department_id, filename, dbtable, charset, day, month, year, actual_date from energosite_tables;")
    results = cursor.fetchall()
    for result in results:
        department_id = result[0]
        fileName = result[1]
        dbTable = result[2]
        charset = result[3]
        day = result[4]
        month = result[5]
        year = result[6]
        actual_date = result[7]
        intDay = int(day)
        intMonth = int(month)
        intYear = int(year)
        if dbTable == "oplbaza" or dbTable == "kvitbaza":
            deleteData(conn, dbTable, intDay, intMonth, intYear, department_id)
        else:
            clearDBTable(conn, dbTable, department_id)

        setSeqVal(conn, dbTable)
        updateActualDate(conn, department_id, dbTable, actual_date)

        p = multiprocessing.Process(name=fileName, target=insertData,
                                    args=(fileName, dbTable, charset, department_id,))
        processes.append(p)

    cursor.close()
    for prcs in processes:
        prcs.start()
    for prcs in processes:
        prcs.join()


if __name__ == '__main__':
    PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
    config = ConfigParser.RawConfigParser()
    config.read(os.path.join(PROJECT_PATH, "config.ini"))

    seconds = time.time()

    # maintfile = getConfigValue("maintfile")
    # destination = open(maintfile, 'w')
    # destination.close()
    c = connectDB()
    walkTables(c)
    deleteDBFiles()
    clearDBTable(c, "tables")

    print (time.time() - seconds)
    serviceDB(c)
    c.close()

    # try:
    # os.remove(maintfile)
    # except OSError:
    # pass







