import json
import warnings
from functools import partial
from typing import List

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

try:
    from smallmatter.pathlib import Path2 as Path
except ImportError:
    warnings.warn(
        "smallmatter.pathlib.Path2 not importable. Direct r/w to Amazon S3 not available."
    )
    from pathlib import Path


class Report:
    def __init__(self, rewards_list, df_history):
        self.rewards_list = rewards_list
        self.df_history = df_history


class ReportIO:
    def __init__(self, prefix):
        self.prefix = Path(prefix)

    def load(self):
        with (self.prefix / "rewards_list.json").open() as f:
            rewards_list = json.load(f)
        df_history = pd.read_csv(self.prefix / "df_history.csv", low_memory=False)
        return Report(rewards_list, df_history)

    def save(self, report, close_fig=False):
        self.save2(report.rewards_list, report.df_history, close_fig)

    def save2(self, rewards_list, df_history, close_fig=False):
        """if `auto_close=True`, then Jupyter notebook will show the plots."""
        p = self.prefix
        p.mkdir(exist_ok=True)

        with (p / "rewards_list.json").open("w") as f:
            json.dump(rewards_list, f)

        fig = plot_reward(rewards_list)
        fig.savefig(p / "reward.png")
        if close_fig:
            plt.close()

        df_history.to_csv(p / "df_history.csv", index=False)
        fig = plot_analysis(df_history)
        fig.savefig(p / "analysis.png")
        if close_fig:
            plt.close()


def plot_reward(rewards_list: List):
    average_reward = sum(rewards_list) / len(rewards_list)
    print(f"Average reward: {average_reward}")
    fig = plt.figure(figsize=(20, 5))
    ax = sns.lineplot(data=rewards_list)
    ax.set_ylabel("Mean reward per episode", fontsize=20)
    ax.set_xlabel("Iteration", fontsize=20)
    plt.axhline(y=average_reward, color="r")
    return fig


def plot_analysis(df_history, episode: List = None):
    if episode is not None:
        df_temp = df_history[df_history["episode"].isin(episode)]
    else:
        df_temp = df_history

    nrows, ncols = 5, 1
    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(16 * ncols, 3 * nrows))

    print(f"Average reward: {df_temp['reward'].sum():.02f}")

    funcs = (
        partial(sns.lineplot, data=df_temp[["average_energy_cost", "market_electric_price"]]),
        partial(sns.scatterplot, data=df_temp[["action"]]),
        partial(sns.lineplot, data=df_temp[["reward"]]),
        partial(sns.lineplot, data=df_temp[["total_reward"]]),
        partial(sns.lineplot, data=df_temp[["energy"]]),
    )
    for ax, f in zip(axs, funcs):
        f(ax=ax)

    fig.tight_layout()
    fig.subplots_adjust(hspace=0.25)
    return fig
