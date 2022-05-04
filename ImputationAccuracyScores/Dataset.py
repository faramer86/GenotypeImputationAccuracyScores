import subprocess
import sys
import numpy as np
import pandas as pd
from cyvcf2 import VCF
from tqdm import trange
from colorama import Fore
from ImputationAccuracyScores.Scores import *
from ImputationAccuracyScores.InputChecks import is_equal


def make_dataset(mask_path: str, imp_path: str) -> pd.DataFrame:
    # Dataset template
    scores = pd.DataFrame(columns=['ID', 'AF', 'CR_GT', 'CR_GP', 'R2', 'IQS', 'DR2'])

    # Bar formatting variables to make processing bar pretty
    n_vars = int(subprocess.run(f'zcat {imp_path} | grep -v "#" | cut -f1 | wc -l',
                                shell=True,
                                capture_output=True).stdout)
    bar_format = "{l_bar}%s{bar}%s{r_bar}" % (Fore.LIGHTRED_EX, Fore.RESET)

    # Here we iterate through each pair of variants from provided vcfs and calculate scores
    for masked, imputed, _ in zip(VCF(mask_path),
                                  VCF(imp_path),
                                  trange(n_vars, bar_format=bar_format)):
        var_id = masked.ID
        var_af = imputed.aaf

        # Comparability checks
        is_equal(masked.ID, imputed.ID)

        if masked.call_rate != 1:
            print(f'Warning: Call rate of {var_id} is not 1 -> We will skip it!\n')
            continue

        # Inputs: genotypes, imputation probabilities and dosages
        gt_masked = np.array(list(map(lambda x: x[0] + x[1], masked.genotypes)))
        gt_imputed = np.array(list(map(lambda x: x[0] + x[1], imputed.genotypes)))
        gp_imputed = imputed.format('GP')
        ds_imputed = np.squeeze(imputed.format('DS'))

        # Scores
        DR2 = round(imputed.INFO.get('DR2'), 3) if imputed.INFO.get('DR2') else None
        CR_GT = concordance(gt_masked, gt_imputed)
        CR_GP = give_po(gt_masked, gt_imputed, gp_imputed)
        IQS = imputation_quality_score(gt_masked, gp_imputed, CR_GP)
        R2 = r_square(gt_masked, ds_imputed)

        df_tmp = pd.DataFrame({'ID': [var_id],
                               'AF': [round(var_af, 3)],
                               'CR_GT': [round(CR_GT, 3)],
                               'CR_GP': [round(CR_GP, 3)],
                               'R2': [round(R2, 3)],
                               'IQS': [round(IQS, 3)],
                               'DR2': [DR2]})

        scores = pd.concat([scores, df_tmp])
    return scores
