
from omegaconf import DictConfig, OmegaConf
import hydra
import requests
from bs4 import BeautifulSoup
import os
from collections import defaultdict
import json
from urllib.parse import urljoin
import time


def get_children(current_url):
    ''' for current url, return list of child urls '''
    print(f'fetching children for {current_url}...')
    response = requests.get(current_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    child_urls = []
    # Find and process links
    for link in soup.find_all('a'):
        href = link.get('href')  # these are relative paths
        child_url = urljoin(current_url, href)
        child_urls.append(child_url)
        
    return child_urls
   

def write_directory_out(directory, config):
    ''' for list of json data objects, write jsonl file out '''
    print('writing directory out...')
    out_dir = f"{config.project_dir}/{config.out_dir}"
    os.makedirs(out_dir, exist_ok=True)
    out_path = f"{out_dir}/directory.jsonl"
    with open(out_path, 'w') as f:
        for entry in directory:
            f.write(f"{json.dumps(entry)}\n")
    print(f"successfully wrote directory to {out_path}")


@hydra.main(version_base=None, config_path="<parentdir>", config_name="<configname>.yaml")
def build_directory_nodes(config):

    print("build directory nodes\n")

    # just using this for duplicate prevention, but this is useful metadata for site map
    url_counts = defaultdict(int)
    directory = []

    # init
    url_queue = []
    url_queue.append(config.top_url)

    while len(url_queue) > 0 \
                            and len(directory) <= config.max_nodes:

        current_url = url_queue.pop(0)

        # add to site directory
        entry = {'url': current_url}
        directory.append(entry)

        # process node
        if '.html' in current_url:
            child_urls = get_children(current_url)
            time.sleep(3)

            for child_url in child_urls:
                if url_counts[child_url] == 0 and config.directory_inclusion_filter in child_url:
                    url_counts[child_url] += 1
                    url_queue.append(child_url)

        


    write_directory_out(directory, config)
    



if __name__ == "__main__":
    build_directory_nodes()

