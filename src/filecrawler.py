#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Crawls the given path and subfolders, extracts files, folders, and metadata"""

import os
import pathlib
from datetime import datetime

def convert_bytes(num):
    """converts bytes to adequate unit (KB/MB/GB/TB)"""
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            num_string = "%3.2f %s" % (num, x)
            return num_string
        else: num /= 1024.0

def crawl_folders(path):
    """crawls path, returns contained folders in "folders" """
    folders = []
    for entry in os.scandir(path):
        if entry.is_dir():
            fp = entry.path
            folders.append(fp)
    return folders

def crawl_files(path):
    """crawls path, returns contained files and their metadata in "files" """
    files = []
    for entry in os.scandir(path):
        if entry.is_file():
            info = entry.stat()
            extension = pathlib.Path(entry).suffix
            filepath = os.path.normpath(entry)
            containingfolders = filepath.split('\\',)
            fileinfo = [entry.name, extension, info.st_size, info.st_mtime,
                        info.st_ctime, info.st_atime, filepath, containingfolders]
            files.append(fileinfo)
    return files

def crawl(path):
    """calls crawl_folders and crawl_files for every folder in the given path"""
    start = datetime.timestamp(datetime.now())
    size = 0

    folders = crawl_folders(path)
    files = crawl_files(path)

    for i in folders:
        folders.extend(crawl_folders(i))
        files.extend(crawl_files(i))

    for i in range(0, len(files)):
        size += files[i][2]
    size = convert_bytes(size)

    print('\nFilecrawler runtime: ' + str(datetime.timestamp(datetime.now())-start))
    print('\nNumber of folders: ' + str(len(folders)))
    print('\nNumber of files: ' + str(len(files)))
    print('\nSize: ' + str(size))

    return files


def main(path="D:\\xppu_data"):
    results = crawl(path)
    print('\nFiles: \n')
    print(results)


if __name__ == "__main__":
    main()