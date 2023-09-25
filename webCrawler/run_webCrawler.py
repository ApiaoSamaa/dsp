import subprocess

def run_script(script_name, *args):
    subprocess.run(['python', script_name, *args])

if __name__ == "__main__":
    run_script('/Users/a123/proj/genePaper/dsp/webCrawler/filter_disease_associations.py')
    run_script('/Users/a123/proj/genePaper/dsp/webCrawler/getGenes.py')
    run_script('/Users/a123/proj/genePaper/dsp/webCrawler/parallel_spider.py')
