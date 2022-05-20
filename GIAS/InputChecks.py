import os
import sys


def is_exist(paths: list) -> None:
    for path in paths:
        if not os.path.exists(path):
            print(f'Error: {path} - do not exist!')
            sys.exit()
    return None


def is_gz(paths: list) -> None:
    for path in paths:
        if not path.endswith('.vcf.gz'):
            print(f'Error: {path} are not .vcf.gz!\n' +
                  'Use `bgzip -c file.vcf > file.vcf.gz` command.')
            sys.exit()
    return None


def is_equal(marker_id1: str,
             marker_id2: str) -> None:
    if marker_id1 != marker_id2:
        print(f'Error: Masked id {marker_id1} != Imputed id {marker_id2} -> We will stop the analysis!\n' +
              'Make sure that both files are sorted and include the same set of variants.\n')
        sys.exit()
    return None
