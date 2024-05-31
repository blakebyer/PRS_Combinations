from pathlib import Path

tsv_dir = Path(r'\logical\path\to\parent\directory') #PRSKB TSV Directory
tsv_path = tsv_dir / 'myfile.tsv' # PRSKB File Name
tsv_cols = ['Sample','Study ID','Reported Trait','Percentile'] # TSV Columns

adni_dir = Path(r'\logical\path\to\parent\directory') #ADNIMERGE Directory
adni_path = adni_dir / 'adnimerge.csv' # adnimerge File Name
adni_cols = ['RID','PTID','PTGENDER','PTRACCAT','AGE','APOE4'] # ADNI Demographics

dx_dir = Path(r'\logical\path\to\parent\directory')
dx_path = dx_dir / 'dxsum.csv' # dxsum File Name
dx_cols = ['RID','DIAGNOSIS','EXAMDATE']

