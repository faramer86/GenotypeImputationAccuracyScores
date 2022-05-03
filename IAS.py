#/usr/bin/venv python3

import argparse
from ImputationAccuracyScores.Dataset import make_dataset

if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='./IAS.py',
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

    output_file = make_dataset(args.masked, args.imputed)

    output_file.to_csv(args.output, sep='\t', index=False)
    print('Done!')

