import os
from pathlib import Path
from typing import List, Union

import pandas as pd
import requests
from battery_env_sm import SimpleBattery


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


def check_data_exist(data_dir: Union[str, os.PathLike] = Path("data")):
    return Path(data_dir) / "sample-data.csv"


def evaluate_episode(agent, env_config):
    """
    Run evaluation over a single episode.

    FIXME: this is for non-gym agent.

    Input:
        agent: trained agent.
    """

    evaluation_list: List = []
    done = False
    env = SimpleBattery(env_config)
    state = env.reset()
    print(f"Index: {env.index}")
    total_rewards = 0

    while not done:
        action = agent.get_action(state)
        next_state, reward, done, info = env.step(action)
        total_rewards += reward
        evaluation_list.append([reward] + [total_rewards] + [action] + state)
        state = next_state

    df_cols = [
        "reward",
        "total_reward",
        "action",
        "energy",
        "average_energy_cost",
        "market_electric_price",
        "price_t1",
        "price_t2",
        "price_t3",
        "price_t4",
        "price_t5",
    ]
    df_eval = pd.DataFrame(evaluation_list, columns=df_cols)

    return df_eval
