from typing import List

import pandas as pd
from battery_env_sm import SimpleBattery


def evaluate_episode(agent, env_config):
    """
    Run evaluation over a single episode.

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
