import requests
from bs4 import BeautifulSoup
import csv
import json
import os
import time


def get_diseaseid_from_tsv(filename):
    first_column = []
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            first_column.append(row[0])
    return first_column


def fetch_genes(session, term):
    url = f"https://www.ncbi.nlm.nih.gov/clinvar/?term={term}"
    resp = session.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    genes = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith("/gene/"):
            gene_id = href.split("/")[-1]
            gene_name = a.text().strip()
            # final_link = "https://www.ncbi.nlm.nih.gov" + href
            # gene_links.append(final_link)
            genes.append((gene_name, gene_id))
    return genes


def expiration_time(unix_time):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(unix_time))


def main():
    terms = get_diseaseid_from_tsv("/Users/a123/proj/genePaper/dsp/webCrawler/disease_associations.tsv")
    with open("myCookie.json", 'r') as file:
        cookies = json.load(file)

    session = requests.Session()
    for cookie_data in cookies:
        cookie = {
            'name': cookie_data['name'],
            'value': cookie_data['value'],
            'path': cookie_data['path'],
            'domain': cookie_data['domain'],
            'secure': cookie_data['secure'],
            'httponly': cookie_data['httpOnly']
        }
        if 'expirationDate' in cookie_data and cookie_data['expirationDate'] != 0:
            cookie['expires'] = expiration_time(cookie_data['expirationDate'])
        session.cookies.set(**cookie)

    output_dir = "/Users/a123/proj/genePaper/dsp/DData"
    for term in terms:
        genes = fetch_genes(session, term)
        for gene in genes:
            # save gene into csv file
            filename = os.path.join(output_dir, gene[0] + ".csv")
            with open(filename, 'w') as file:
                writer = csv.writer(file)
                writer.writerow(["gene_name", "gene_id"])
                writer.writerow(gene)

if __name__ == "__main__":
    main()
