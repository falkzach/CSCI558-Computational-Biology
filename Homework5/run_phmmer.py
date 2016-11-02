#!/usr/local/bin/python3

import argparse
import subprocess
import re

def get_input_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='Input File')
    parser.add_argument('output_file', help='Output File')
    parser.add_argument('threshold', help='E-value Threshold')
    args = parser.parse_args()
    if args.input_file is None or args.output_file is None or args.threshold is None:
        print('Useage: {} [if <filename.fa>] '.format(__file__))
        exit(1)
    return args.input_file, args.output_file, args.threshold


if __name__ == '__main__':
    input_file, output_file, threshold = get_input_arguments()
    call = ['phmmer', '-E {}'.format(threshold), '--noali', '--notextw', input_file, output_file]

    process = subprocess.Popen(call,stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    clean = [line.decode('UTF-8') for line in out.splitlines()]

    query_regex = 'Query:\s+(?P<sequence_id>\S+)\s+\[.*\]'
    value_regex = '\\s+(?P<eval>\S*)\s+(\S*)\s+(?P<bias>\S*).*'
    query_pattern = re.compile(query_regex)
    value_pattern = re.compile(value_regex)

    count = 0
    match = False
    sequence = ''
    results = []
    for line in clean:
        # print(line)
        if count >= 0:
            count -= 1
            if count != 0:
                continue
        else:
            match = query_pattern.match(line)

        if match and (count == 0):
            values = value_pattern.match(line)
            eval = values.group('eval')
            bias = values.group('bias')
            results.append((sequence, eval, bias))
            match = False

        if match:
            sequence = match.group('sequence_id')
            count = 5

    for result in results:
        print('{}\t{}   {}'.format(result[0], result[1], result[2]))