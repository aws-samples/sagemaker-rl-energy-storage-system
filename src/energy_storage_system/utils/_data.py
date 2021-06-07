import os
from typing import Union

import requests


def download_aeom_data(
    filepath: Union[str, os.PathLike],
    url: str = "https://aemo.com.au/aemo/data/nem/priceanddemand/PRICE_AND_DEMAND_202103_NSW1.csv",
) -> None:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        )
    }

    r = requests.get(url, headers=headers)
    with open(filepath, "wb") as f:
        f.write(r.content)
