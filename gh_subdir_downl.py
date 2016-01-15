#!/usr/bin/env python3

'''
description:
    This script was written to download an archive, i.e. no history or
    meta-information of a GitHub repository or subdirectory of a repo..  It was
    created as GitHub doesn't provide archiving, i.e. git-archive, see
    https://help.github.com/articles/can-i-archive-a-repository/

todo:
    1. general addition of error messages

Example usage:
    gh_subdir_downl.py -u 8leggedunicorn -r Udacity -s p1_stroop_effect -f 'README|.*\.(csv|bib|py|tex)'
'''

import requests
import json
import re
import os
import argparse

__author__ = 'Yigal Weinstein'

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
        action="store_true")
parser.add_argument("-u", "--user", type=str, help="specify the GitHub user account",
        required=True)
parser.add_argument("-r", "--repository", type=str, help="specify the GitHub user's repository",
        required=True)
parser.add_argument("-s", "--subdirectory", type=str, help="specify a subdirectory to download",
        required=False)
fhelp = '''
Specify via regex what files to download.  As an example:

-f 'README|.*\.(csv|bib|py|tex)'

to download only csv, bib, py and tex files.
'''
parser.add_argument("-f", "--filetypes", type=str, help = fhelp, required=False)

args = parser.parse_args()

user = args.user
repo = args.repository

if args.subdirectory:
    subdir = args.subdirectory
    path = subdir
else:
    path = ''

if args.filetypes:
    filetypes = args.filetypes
else:
    filetypes = '.*'

if args.verbose:
    print("verbosity turned on")

def gen_url( user, repo, path='' ):
    url = 'https://api.github.com/repos/' + user + '/' + repo + \
        '/contents/' + path
    return url

def ls_subdir_content( url, path ):
    # returns list of objects - files, and directories contained within a
    # repository or subdirectory

    headers = { 'Accept' : 'application/vnd.github.v3.raw' }
    r = requests.get( url, headers = headers )
    contents = json.loads( r.text )
    return contents

def get_file( url, file_name, path ):
    # Function to download a file from GitHub
    if not os.path.exists(path) and path != '':
        os.makedirs(path)
    file_path = os.path.join( path, file_name )
    if os.path.isfile( file_path ):
        print( "{f} already exists on the local file system".format( f = file_path ) )
    else:
        response = requests.get( url, stream=True )
        print( '\nDirect link {url}\nDownloading {s}'.format( url = url, s = file_name ) )

        file_content = requests.get(url).text #.encode('utf-8')
        with open( file_path , 'w' ) as out_file:
            out_file.write(file_content)
        print( '{s} retrieved'.format( s = file_name ) )

def recurs_dl( contents , path ):
    for obj in contents:
        if obj[ 'type' ] == 'file':
            file_name = obj[ 'name' ]
            if re.search(filetypes, file_name):
                url = obj[ 'download_url' ]
                get_file( url, file_name, path )
        elif obj[ 'type' ] == 'dir':
            subdir_path = os.path.join( path , obj[ 'name' ] )
            subdir_url = gen_url( user, repo, subdir_path )
            subdir_contents = ls_subdir_content( subdir_url, subdir_path )
            recurs_dl( subdir_contents , subdir_path )

# Call function to create and dl file/create dir. structure:
url = gen_url( user, repo, path )
contents = ls_subdir_content( url, path )
recurs_dl( contents , path )
