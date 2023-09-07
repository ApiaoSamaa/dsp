# %%
from pathlib import Path

proj_path = Path.cwd()
relative_train_path = "DataBase/Primates"
train_path = proj_path / relative_train_path
# %%
def extract_fasta_to_csv(dir_path, dir_name, csv_path):
    fasta_info = []
    for txt_file in dir_path.glob('*.txt'):
        with open(txt_file, 'r') as file, open(csv_path, 'a') as ofile:
            for line in file:
                # Check if the line starts with '>'
                if line.startswith('>'):
                    info = line[1:].strip()
                    fasta_info.append(info)
                    ofile.write(f'{info},{dir_name}\n')
    return fasta_info

# %%
for sub_dir in train_path.iterdir():
    if sub_dir.is_dir():
        cls_name = sub_dir.name
        tmp = extract_fasta_to_csv(sub_dir, cls_name, proj_path / 'DataBase' / 'Primates.csv')

# %%
