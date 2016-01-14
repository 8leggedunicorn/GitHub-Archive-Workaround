#!/usr/bin/env python3

'''
description:
    This script was written to download subdirectories of GitHub repositories.
    It was created as GitHub doesn't provide archiving, i.e. git-archive, see
    https://help.github.com/articles/can-i-archive-a-repository/

todo: 
    1. will only download at a depth of 1, that is if the directory contains
    directories script won't succeed at downloading, i.e. needs recursive downloads
    2. general addition of error messages

Example usage:
    gh_subdir_downl.py -u 8leggedunicorn -r Udacity -s p1_stroop_effect
'''

import requests
import json
import re
import os
import argparse

__author__ = 'Yigal Weinstein'

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
parser.add_argument("-u", "--user", type=str, help="specify the GitHub user account", required=True)
parser.add_argument("-r", "--repository", type=str, help="specify the GitHub user's repository", required=True)
parser.add_argument("-s", "--subdirectory", type=str, help="specify the subdirectory to download", required=True)

args = parser.parse_args()

user = args.user
repo = args.repository
subdir = args.subdirectory
path = subdir


if args.verbose:
    print("verbosity turned on")

url = 'https://api.github.com/repos/' + user + '/' + repo + \
    '/contents/' + path

if not os.path.exists(path):
    os.makedirs(path)

headers = { 'Accept' : 'application/vnd.github.v3.raw' }
r = requests.get( url, headers = headers )

contents = json.loads(r.text)

def get_file( url, file_name, path):
    file_path = os.path.join( path, file_name )
    response = requests.get( url, stream=True )
    file_content = requests.get(url).text #.encode('utf-8')
    with open( file_path , 'w' ) as out_file:
        out_file.write(file_content)

filetypes = 'README|.*\.(csv|bib|py|tex)'

for file in contents:
    file_name = file[ 'name' ]
    if re.search(filetypes, file_name):
        url = file[ 'download_url' ]
        print('Direct link {}'.format(url))
        print( 'Downloading {s}'.format( s = file_name ) )
        get_file( url, file_name, path )
        print( '{s} retrieved'.format( s = file_name ) )
