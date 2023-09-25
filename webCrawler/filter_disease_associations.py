import csv
from CONSTANTS import num_filter_gene, original_disease_csv_path, gene_disease_association_tsv_path

filename = original_disease_csv_path
filter_num = num_filter_gene
with open(filename, 'r') as infile, open(gene_disease_association_tsv_path, 'w', newline='') as outfile:
    reader = csv.reader(infile, delimiter='\t')
    writer = csv.writer(outfile, delimiter='\t')
    for row in reader:
        if row[0] == 'diseaseId' or int(row[-2]) >=filter_num:
            writer.writerow(row)
