import requests
from bs4 import BeautifulSoup
import csv
import json
import os
import time
import re
from CONSTANTS import gene_disease_association_tsv_path, cookie_json_path, genes_of_diseases_dirpath



def get_diseaseid_from_tsv(filename):
    first_column = []
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            if row[0] == 'diseaseId':
                continue
            first_column.append(row[0])
    return first_column


def fetch_genes(session, term):
    url = f"https://www.disgenet.org/browser/0/1/0/{term}/"
        
    resp = session.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    genes = []
    pattern = re.compile(r"http://www\.ncbi\.nlm\.nih\.gov/gene/(\d+)")
    anchors = soup.find_all('a', href=pattern)
    stored_gene_ids = set()
    for anchor in anchors:
        gene_id = pattern.search(anchor['href']).group(1)
        if gene_id not in stored_gene_ids:
            stored_gene_ids.add(gene_id)
            # Extract the gene_name by looking for the span with class 'dsgn-trunc-hidd' inside the anchor
            gene_name = anchor.text
            genes.append((gene_name, gene_id))
            print(f"gene_id={gene_id}, gene_name={gene_name}")
    return genes


def expiration_time(unix_time):
    return unix_time


def main():
    terms = get_diseaseid_from_tsv(gene_disease_association_tsv_path)
    with open(cookie_json_path, 'r') as file:
        cookies = json.load(file)

    session = requests.Session()
    for cookie_data in cookies:
        cookie = {
            'name': cookie_data['name'],
            'value': cookie_data['value'],
            'path': cookie_data['path'],
            'domain': cookie_data['domain'],
            'secure': cookie_data['secure'],
        }
        if 'expirationDate' in cookie_data and cookie_data['expirationDate'] != 0:
            cookie['expires'] = expiration_time(cookie_data['expirationDate'])
        session.cookies.set(**cookie)

    output_dir = genes_of_diseases_dirpath
    for term in terms:
        # for each term, save a term_genes.csv file
        genes = fetch_genes(session, term)
        # save the genes into term_genes.csv
        with open(os.path.join(output_dir, term + "_genes.csv"), 'w') as file:
            # save the genes into term_genes.csv
            writer = csv.writer(file)
            for gene in genes:
                writer.writerow(gene)
if __name__ == "__main__":
    main()
