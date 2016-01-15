#!/usr/bin/env python3

'''
description:
    This script was written to download subdirectories of GitHub repositories.
    It was created as GitHub doesn't provide archiving, i.e. git-archive, see
    https://help.github.com/articles/can-i-archive-a-repository/

    There is an internal variable specifying via regex the file filter to use
    to only download the desired files, called 'filetypes'.
todo:
    1. general addition of error messages

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

#filetypes = 'README|.*\.(csv|bib|py|tex)'
filetypes = '.*'

if args.verbose:
    print("verbosity turned on")

def gen_url( user, repo, path ):
    url = 'https://api.github.com/repos/' + user + '/' + repo + \
        '/contents/' + path
    return url

def ls_subdir_content( url, path ):
    # creates subdir and returns list of objects - files, and directories
    if not os.path.exists(path):
        os.makedirs(path)

    headers = { 'Accept' : 'application/vnd.github.v3.raw' }
    r = requests.get( url, headers = headers )
    contents = json.loads( r.text )
    return contents


def get_file( url, file_name, path ):
    # Function to download a file
    file_path = os.path.join( path, file_name )
    response = requests.get( url, stream=True )

    print( 'Direct link {url}\nDownloading {s}'.format( url = url, s = file_name ) )

    file_content = requests.get(url).text #.encode('utf-8')
    with open( file_path , 'w' ) as out_file:
        out_file.write(file_content)
    print( '{s} retrieved'.format( s = file_name ) )

def recurs_dl( contents , path ):
    for obj in contents:
        if obj[ 'type' ] == 'file':
            file_name = obj[ 'name' ]
            if re.search(filetypes, file_name): # only download selected files
                url = obj[ 'download_url' ]
                get_file( url, file_name, path )
        elif obj[ 'type' ] == 'dir':
            subdir_path = os.path.join( path , obj[ 'name' ] )
            print(subdir_path)
            subdir_url = gen_url( user, repo, subdir_path )
            subdir_contents = ls_subdir_content( subdir_url, subdir_path )
            recurs_dl( subdir_contents , subdir_path )

url = gen_url( user, repo, path )
contents = ls_subdir_content( url, path )
recurs_dl( contents , path )
