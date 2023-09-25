# controller.py

import pandas as pd
from multiprocessing import Process
from scrapy.crawler import CrawlerProcess
from www_spider import WwwSpider
from webCrawler.get_genes_of_diseases_csv import get_diseaseid_from_tsv
from CONSTANTS import gene_disease_association_tsv_path, genes_of_diseases_dirpath

# Define a function to start a CrawlerProcess for each spider instance
def run_spider(genes,term):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    })
    process.crawl(WwwSpider, genes=genes, term=term)
    process.start()

def main():
    # terms = ["/path/to/csv1.csv", "/path/to/csv2.csv"]  # Add paths to your CSVs
    terms = get_diseaseid_from_tsv(gene_disease_association_tsv_path)

    processes = []

    for term in terms:
        csv_name = genes_of_diseases_dirpath+str(term)+"_genes.csv"
        dataframe = pd.read_csv(csv_name, header=None)
        genes = [tuple(x) for x in dataframe.values]

        # Create and start a new process for each CSV file
        p = Process(target=run_spider, args=(genes,term,))
        p.start()
        processes.append(p)

    # Join all the processes
    for p in processes:
        p.join()

if __name__ == "__main__":
    main()
