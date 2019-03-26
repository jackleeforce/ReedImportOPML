#!/usr/bin/env python
# coding: utf-8
# @Author : JackLee 
# @contact: jackleeforce@gmail.com
# @Time : 2019-03-26 14:17 
# @File : ReederImportOPML.py 
# @desc:
import logging
import os
import shutil
import sqlite3
from sys import argv
from xml.dom.minidom import parse


def dom_element_to_insert(elem):
    return (
        elem.getAttribute('xmlUrl'), elem.getAttribute('text'), elem.getAttribute('title'),
        elem.getAttribute('htmlUrl'))


def main(path_to_opml):
    dom = None

    try:

        with open(path_to_opml) as f:
            dom = parse(f)

        db_path = os.path.join(os.environ['HOME'], 'Library', 'Containers', 'com.reederapp.rkit2.mac', 'Data',
                               'Library',
                               'Application Support', 'Reeder', 'rkit', 'rkit.db')
        shutil.copy(db_path, os.path.join(os.environ['HOME'], 'Desktop'))

        inserts = (dom_element_to_insert(x) for x in dom.getElementsByTagName('outline') if x.hasAttribute('xmlUrl'))
        connection = sqlite3.connect(db_path)
        with connection:
            cursor = connection.cursor()
            cursor.execute("SELECT oid FROM rkstream")
            existing = [x[0] for x in cursor.fetchall()]
            cursor.executemany(
                "INSERT INTO rkstream (oid,user,title,htmlTitle,link,listed,isFolder,isSmartStream,'index') VALUES (?,1,?,?,?,1,0,0,0);",
                (x for x in inserts if not x[0] in existing))
            connection.commit()
        print
        "Done"
    except Exception as e:
        logging.e(e)


if __name__ == '__main__':
    main(argv[-1])
