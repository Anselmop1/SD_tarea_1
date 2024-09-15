import sys
import requests
import time
import random

# ------------------- READ_TXT ------------------- #
def read_domains_from_file(file_path, max_lines):
    domains = []
    with open(file_path, 'r') as f:
        lines = f.readlines()[1:]  # Skip the header
        for line in lines:
            if len(domains) >= max_lines:
                break
            parts = line.split('\t')
            if parts[4].strip():
                domains.append(parts[4].strip())
    return domains

# ------------------- API REQUEST ------------------- #
def request_to_api(domain, api_url):
    try:
        response = requests.get(f"{api_url}/resolve?domain={domain}")
        if response.status_code == 200:
            print(f"Successfully fetched data for {domain}")
        else:
            print(f"Failed to fetch data for {domain}: Status code {response.status_code}")
    except requests.RequestException as e:
        print(f"Error requesting {domain}: {e}")

# ------------------- MAIN ------------------- #
def main(input_file, api_url, max_lines):
    domains = read_domains_from_file(input_file, max_lines)
    if not domains:
        print("No domains found in the file.")
        return

    print(f"Starting to request {len(domains)} domains...")
    for domain in domains:
        request_to_api(domain, api_url)
        time.sleep(random.uniform(0.5, 2.0))  # Sleep to simulate real user behavior

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 crawler.py (Input file name) (API URL)')
        sys.exit()

    input_file = sys.argv[1]
    api_url = sys.argv[2]
    max_lines = 1000  # Adjust as needed

    main(input_file, api_url, max_lines)
