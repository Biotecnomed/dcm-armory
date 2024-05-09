#!/usr/bin/env python

import csv
import argparse
from datetime import datetime as dt

parser = argparse.ArgumentParser('dateFix', description='Fix a CSV file turning date value to Standard date format')
parser.add_argument('-s','--skip-header', action='store_true',help='Skip the header')
parser.add_argument('-f','--format',type=str,help='Expected data format',default='%d/%m/%Y')
parser.add_argument('-c','--columns',nargs='+',type=int,help='A list of columns to convert',required=True)
parser.add_argument('input',type=str,help='CSV input file path')
parser.add_argument('output',type=str,help='CSV input file path')

F = '%Y%m%d'

def main():
    args = vars(parser.parse_args())
    print(args)

    input_file = args['input']
    output_file = args['output']
    f1 = args['format']


    try:
        output = open(output_file,'w')
        writer = csv.writer(output,delimiter = ',')

        with open(input_file,'r') as fs:
            reader = csv.reader(fs, delimiter =',')
            if args['skip_header']:
                next(reader)
            for line in reader:
                for c in args['columns']:
                    line[c] = convert(line[c],f1)
                writer.writerow(line)

    except Exception as error:
        print(error)
    finally:
        output.close()


def convert(dateStr,f):
    try:
        d = dt.strptime(dateStr,f).date()
        return d.strftime(F)
    except Exception as e:
        print(f'Warning: {e}')
        return None

if __name__ == '__main__':
    main()