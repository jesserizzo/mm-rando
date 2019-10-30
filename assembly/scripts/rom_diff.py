#!/usr/bin/env/python3

import argparse
import struct

from table import Table

def get_parser():
    """ Get the argument parser. """
    def auto_int(x):
        return int(x, 0)
    parser = argparse.ArgumentParser()
    parser.add_argument('--table-offset', type=auto_int, help='Offset of file table (use with --virtual)')
    parser.add_argument('--virtual', action='store_true', help='Get virtual addresses instead of physical')
    parser.add_argument('BASE_FILE')
    parser.add_argument('COMPARISON_FILE')
    parser.add_argument('OUTPUT_FILE')
    return parser

def main():
    args = get_parser().parse_args()
    create_diff(args.base_file, args.comparison_file, args.output_file,
        offset=args.table_offset, virtual=args.virtual)

chunk_size = 4096
uint32 = struct.Struct('>I')

def unequal_chunks(file1, file2):
    addr = 0
    while True:
        chunk1 = file1.read(chunk_size)
        chunk2 = file2.read(chunk_size)
        if not chunk1:
            return
        if chunk1 != chunk2:
            words1 = [x[0] for x in uint32.iter_unpack(chunk1)]
            words2 = [x[0] for x in uint32.iter_unpack(chunk2)]
            yield (addr, words1, words2)
        addr += chunk_size

def create_diff(base_path, compare_path, output_path, virtual=False, offset=0):
    diffs = []
    with open(base_path, 'rb') as base_f, open(compare_path, 'rb') as comp_f:
        # Read file table if specified
        table = None
        if virtual:
            table = Table.read(comp_f, offset)
            comp_f.seek(0)
        # Find diffs
        for (addr, base_words, comp_words) in unequal_chunks(base_f, comp_f):
            for j in range(len(comp_words)):
                if comp_words[j] != base_words[j]:
                    found = addr + 4*j
                    # Resolve physical address to virtual address if specified
                    if virtual:
                        found = table.resolve(found)
                    diffs.append((found, comp_words[j]))

    with open(output_path, 'w') as out_f:
        for (addr, word) in diffs:
            out_f.write('{0:x},{1:x}\n'.format(addr, word))

if __name__ == '__main__':
    main()
