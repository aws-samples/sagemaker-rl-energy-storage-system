import pathlib

import requests


def download_aeom_data(filepath: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }
    url = "https://aemo.com.au/aemo/data/nem/priceanddemand/PRICE_AND_DEMAND_202103_NSW1.csv"

    r = requests.get(url, headers=headers)
    with open(filepath, "wb") as f:
        f.write(r.content)


def check_data_exist():
    data_dir = pathlib.Path(__file__).parent.parent.parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    filepath = data_dir / "sample-data.csv"
    if not filepath.exists():
        print("Downloading data...")
        download_aeom_data(filepath)
    else:
        print("Data already exists...")


if __name__ == "__main__":
    check_data_exist()
