from typing import List, Optional

import numpy as np
import pandas as pd
from tqdm import tqdm

from .agents import Agent
from .envs import SimpleBattery


class TrainResult:
    def __init__(self, rewards_list: List[float], history_list: List[float]) -> None:
        self.rewards_list = rewards_list
        self.history_list = history_list

    @property
    def mean_rewards(self) -> float:
        """Mean of episodes's total rewards."""
        return sum(self.rewards_list) / len(self.rewards_list)


def train(env: SimpleBattery, agent: Agent, episodes: int = 3000, seed: Optional[int] = None):
    if episodes < 1:
        raise ValueError(f"Number of episodes must be >1, but getting {episodes}.")

    rewards_list: List[float] = []
    history_list: List[float] = []

    for i in tqdm(range(episodes)):
        done = False
        state = env.reset()
        total_rewards = 0

        while not done:
            action = agent.get_action(state)
            next_state, reward, done, info = env.step(action)
            total_rewards += reward
            history_list.append([i] + [total_rewards] + [action] + state)
            state = next_state

        # print(f"Episode {i+1} ({env.counter}):{total_rewards}")
        rewards_list.append(total_rewards)

    return TrainResult(rewards_list, history_list)


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
