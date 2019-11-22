#!/usr/bin/env python

import getopt
import re
import sys

import libsvadarts as sva

from pprint import pprint

def main(argv):
    parameters = {
        'filename': '',
    }

    try:
        opts, args = getopt.getopt(
            argv, "hsp:v:",
            [
                "help", "file="])
    except getopt.GetoptError as err:
        print(err)
        usage()

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt in ("-f", "--file"):
            parameters['filename'] = arg

    if not parameters['filename']:
        usage()

    pprint(parameters)
    data = sva.load_xlsx(parameters['filename'])

    # pprint(data)
    json_filename = re.sub(r'xlsx$', r'json', parameters['filename'])
    json_filename = re.sub(r'[^/]+/',r'', json_filename)

    sva.save_data_to_json(data, json_filename)

def usage():
    print('''read_file.py 
        --file <filename>
        ''')
    sys.exit()

if __name__ == "__main__":
    main(sys.argv[1:])

