
from omegaconf import DictConfig, OmegaConf
import hydra
import requests
import os
from collections import defaultdict
import json
import time

def load_directory_data_urls(config):

    dataset = []
    with open(f"{config.out_dir}/directory.jsonl", 'r') as f:
        for line in f:
            obj = json.loads(line)
            if config.file_inclusion_filter in obj['url']:
                dataset.append(obj['url'])
    return dataset



@hydra.main(version_base=None, config_path="<parentdir>", config_name="<configname>.yaml")
def mirror_data(config):

    pdf_urls = load_directory_data_urls(config)
    print(f'pdfs to mirror: \n {pdf_urls} \n ----------------')

    out_dir = f"{config.project_dir}/{config.out_dir}/pdfs"
    os.makedirs(out_dir, exist_ok=True)

    # filtered list of pdfs
    with open(f"{out_dir}/directory.jsonl", 'w') as f:
        for url in pdf_urls:
            f.write(f"{url}\n")

     # pdf data
    file_counts = defaultdict(int)
    for pdf_url in pdf_urls:
        name = pdf_url.split('/')[-1]
        if file_counts[pdf_url] == 0:
            file_counts[pdf_url] += 1            
            out_path = f"{out_dir}/{name}"
            response = requests.get(pdf_url)
            with open(out_path, 'wb') as f:
                f.write(response.content)

            time.sleep(config.pause_seconds)

if __name__ == "__main__":
    mirror_data()

