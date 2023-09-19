import scrapy
from scrapy.utils.response import open_in_browser
import json


# just put your genes here!
# [(full_name, only_id), (full_name, only_id), ...]
genes = [("LOC106627981", "106627981")]



# usage: run `scrapy runspider path\to\this\file.py`
# make sure you run `pip install scrapy` first!
class WwwSpider(scrapy.Spider):
    name = "dataset"
    start_urls = ["https://www.baidu.com"]

    def __init__(self, *args, **kwargs):
        super(WwwSpider, self).__init__(*args, **kwargs)

        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

    def parse(self, response):
        for gene in genes:
            payload = {
                "gene_ids": [gene[1]],
                "include_annotation_type": ["FASTA_GENE"],
            }
            headers = {"Content-Type": "application/json"}
            yield scrapy.Request(
                "https://api.ncbi.nlm.nih.gov/datasets/v1/gene/download?filename="
                + gene[0]
                + "_datasets.zip",
                method="POST",
                body=json.dumps(payload),
                headers=headers,
                callback=self.save_file,
                meta={"filename": gene[0]},
            )

    def save_file(self, response):
        filename = response.meta["filename"] + ".zip"
        with open(filename, "wb") as f:
            f.write(response.body)
        self.log("Saved file %s" % filename)
