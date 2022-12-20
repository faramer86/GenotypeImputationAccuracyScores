# **Genotype Imputation Accuracy Scores**
This script compare two VCF.GZ files and output several commonly used accuracy
scores (R2, IQS, CR etc.). This is especially handy when you want to estimate
true genotype imputation accuracy using masking approach.

Initially, it was optimized to work with `BEAGLE 5.2` output. 

## **Reference**

Kolosov N, Rezapova V, Rotar O, Loboda A, Freylikhman O, et al. (2022) Genotype imputation and polygenic score estimation in northwestern Russian population. PLOS ONE 17(6): e0269434. https://doi.org/10.1371/journal.pone.0269434

## **Dependencies** 

Make sure that you have `python` version >= 3.8 and latest version of `pip`.
You can check it by running:

```bash
 python --version
 pip --version
```

If you do not have Python, please install the latest 3.x version from python.org.

In order to help keep our project dependencies separated and avoid conflicts
between package versions we uses `virtualenv`.
If you do not have it you can install it using `pip`:

```bash
pip install virtualenv
```

If you have any problems with the installation or usage of `virtualenv` be free
to consult the official documentation: https://virtualenv.pypa.io/en/latest/

## **Installation**

Firstly, clone this repository to your local machine. 

```bash
git clone https://github.com/faramer86/GenotypeImputationAccuracyScores.git
```

Go to the "GenotypeImputationAccuracyScores" repository, create and launch virtual environment:

```bash
virtualenv venv
source venv/bin/activate
```

If you see `(venv)` prefix in your terminal, then everything goes well so far.

Install the requirements from the home repository. 
This command will install all the necessary python packages:

```bash
pip install -r requirements.txt
```

**Now you can launch `GIAS.py`, it should work!**

#### NOTE:

1) Do not forget to exit virtual environment after you are done:

```bash
deactivate
```

2) Do not forget to activate `venv` everytime you want to launch tool:

```bash
source vprior/bin/activate
```

#### Fow Windows users:

https://stackoverflow.com/questions/17737203/python-and-virtualenv-on-windows

## **Usage**

```bash
  -h, --help       show this help message and exit
  -m , --masked    VCF.GZ with actual masked genotypes.
  -i , --imputed   VCF.GZ with imputed genotypes.
  -o , --output    Output file path/name.
```

example/test:

```bash
./GIAS.py \
    -i data/imputed.test.vcf.gz \
    -m data/masked.test.vcf.gz \
    -o test.scores.tsv
```

If it have worked well (no bugs), then everything is OK! 

## **Input requirements:**

1) Both VCF files have to be properly "gzipped"!
2) Both files have to include the same amount of variants in the same order!
3) Both files have to include variants with Call Rate = 1.0!

   (If some variant violates this rule - we skip the latter)
4) Imputed genotypes have to include Dosages and Probabilities (FORMAT - GT:DS:GP)

   (If you use `BEAGLE` - do not forget to set `gp=true`)

## **Output example:**

|   **ID**   | **AF** | **IQS** | **R2** | **CR** | **...** |
|:----------:|:------:|:------:|:------:|:------:|:---:|
| rs3828049  |  0.80  |  0.92   |  0.81  |  1.0   | ... |
| rs61766340 |  0.01  |  0.21   |  0.30  |  0.97  | ... |
| rs72642184 |   0.18 |  0.63   |  0.67  |  0.94  | ... |
|    ...     |  ...   |   ...   |  ...   |  ...   | ... |

- **ID** - variant ID from dataset with actual genotypes
- **AF** - allele frequency
- **IQS** - imputation quality score
- **R2** - squared correlation coefficient
- **DR2** - Dosage-R2 from Beagle output (if exists)
- **CR_GT** - Concordance rate (discrete version)
- **CR_GP** - Concordance rate (incorporates probabilities)
