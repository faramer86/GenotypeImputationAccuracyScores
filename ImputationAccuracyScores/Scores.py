import numpy as np
from functools import reduce


def give_ns(gt_masked: np.array) -> np.array:
    """
    Action:
    Calculate total number of individuals
    for each actual genotype type.

    For more info:
    see ImputationQualityScore()
    """
    return np.array([sum(gt_masked == i) for i in range(3)])


def give_ms(prob_imp: np.array) -> np.array:
    """
    Action:
    Calculate sum of marginal probabilities
    for each imputed genotype type.

    For more info:
    see ImputationQualityScore()
    """
    return reduce(lambda x, y: x + y, prob_imp)


def give_po(geno_mask: np.array,
            geno_imp: np.array,
            prob_imp: np.array) -> float:
    """
    Action:
    Calculate Po (Concordance rate)*

    Note: In comparison with Concordance(...),
    this coefficient uses imputed probabilities
    instead of best guess genotypes

    For more info:
    see ImputationQualityScore()
    """
    prob_imp_max = np.array(list(map(lambda x: max(x), prob_imp)))
    return sum(prob_imp_max[geno_mask == geno_imp]) / len(prob_imp_max)


def give_pc(ms: np.array,
            ns: np.array) -> float:
    """
    Action:
    Calculate Po (Concordance rate)

    For more info:
    see ImputationQualityScore()
    """
    return np.dot(ns, ms) / sum(ns) ** 2


def imputation_quality_score(geno_mask: np.array,
                             prob_imp: np.array,
                             Po: float) -> float:
    """
    Action:
    Calculate IQS (imputation quality score)
    Formula - (Po - Pc)/(1 - Pc)

    Input:
    1) encoded masked genotypes {0, 1, 2}*
    1) encoded imputed genotypes {0, 1, 2}*
    1) imputed genotype probabilities [0-1]
    (FORMAT = GP)

    *Note:
    Counted allele - alternative

    References:
    https://doi.org/10.1371/journal.pone.0137601
    https://doi.org/10.1371/journal.pone.0009697
    """

    ns = give_ns(geno_mask)
    ms = give_ms(prob_imp)
    Pc = give_pc(ns, ms)

    return (Po - Pc) / (1 - Pc)


def r_square(geno_mask: np.array,
             dasage_imp: np.array) -> float:
    """
    Action:
    Calculate Squared Correlation coefficient
    between encoded genotypes and imputed dosages

    Input:
    1) encoded masked genotypes {0, 1, 2}*
    2) imputed dosages [0-2]

    *Note:
    Counted allele - alternative
    """
    return np.corrcoef(geno_mask, dasage_imp)[0, 1] ** 2


def concordance(geno_mask: np.array,
                geno_imp: np.array) -> float:
    """
    Action:
    Calculate Concordance coefficient
    between encoded actual and imputed genotypes.

    Input:
    1) encoded masked genotypes {0, 1, 2}*
    2) encoded imputed genotypes {0, 1, 2}*

    *Note:
    Counted allele - alternative
    """
    return sum(geno_mask == geno_imp) / len(geno_mask)
