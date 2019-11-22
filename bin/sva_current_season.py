#!/usr/bin/env python

import re
import os
import sys

import libsvadarts as sva

from pprint import pprint

file = '~/src/dartsense/data/Austerlitz_seizoen_2019-2020.xlsx'
filename = os.path.expanduser(file)

pprint(filename)


def main(argv):
    data = sva.load_xlsx(filename)

    # pprint(data)
    json_filename = re.sub(r'xlsx$', r'json', filename)
    json_filename = re.sub(r'[^/]+/',r'', json_filename)
    json_filename = '~/src/dartsense/docs/uitslagen/' + json_filename 
    json_filename = os.path.expanduser(json_filename)

    pprint(json_filename)
    
    sva.save_data_to_json(data, json_filename)




if __name__ == "__main__":
    main(sys.argv[1:])