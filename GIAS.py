#! venv/bin/python

import argparse
from GIAS.Dataset import make_dataset
from GIAS.InputChecks import is_exist, is_gz

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='./GIAS.py',
                                     usage='%(prog)s [options]',
                                     description="""
                                     This tool compare two VCF.GZ files (masked and imputed genotypes)
                                     and calculate several commonly used accuracy scores.
                                     """)
    parser.add_argument('-m', '--masked', required=True, metavar='',
                        help='VCF.GZ with actual masked genotypes.')
    parser.add_argument('-i', '--imputed', required=True, metavar='',
                        help='VCF.GZ with imputed genotypes.')
    parser.add_argument('-o', '--output', required=True, metavar='',
                        help='Output file path/name.')
    args = parser.parse_args()

    # Check VCF files
    is_exist([args.masked, args.imputed])
    is_gz([args.masked, args.imputed])

    # Create dataset with scores
    make_dataset(args.masked, args.imputed).to_csv(args.output, sep='\t', index=False)

    print('Done!')
