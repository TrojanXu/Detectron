import os
import argparse
import sys
import json
import math
from collections import OrderedDict

def parse_args():
    parser = argparse.ArgumentParser(
        description='Generate log csv from screenlog file'
    )
    parser.add_argument(
        '--input',
        dest='screenlog_file',
        help='path to screenlog_file',
        default='screenlog.0',
        type=str
    )

    parser.add_argument(
        '--output',
        dest='csvlog_file',
        help='path to csvlog_file',
        default='log.csv',
        type=str
    )

    if len(sys.argv) == 1:
        print "generate log csv from default: screenlog.0, output log.csv"
    return parser.parse_args()


def generate_csv(screenlog_file, csvlog_file):
    if not os.path.exists(screenlog_file):
        print 'screenlog_file does not exist.'
        return
    
    csv_col = None
    dict_slice = slice(11,-1)
    with open(csvlog_file, 'w') as out:
        with open(screenlog_file, 'r') as f:
            for line in f:
                if 'json_stats' not in line:
                    continue
                iter_dict = json.loads(line.strip('\n')[dict_slice], object_pairs_hook=OrderedDict)
                if not csv_col:
                    csv_col = list(iter_dict.keys())+['lg_loss']
                    out.write(','.join(csv_col))
                out.write('\n'+','.join(str(value).replace(',', ' ') for value in iter_dict.values())+','+str(math.log10(1.0e-5+float(iter_dict['loss']))))


if __name__ == '__main__':
    args = parse_args()
    generate_csv(args.screenlog_file, args.csvlog_file)
