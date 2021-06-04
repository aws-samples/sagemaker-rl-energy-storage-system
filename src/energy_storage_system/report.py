import json
import os
import warnings
from functools import partial
from typing import List, Sequence, Union

import matplotlib
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
    """A container to hold episodes's rewards and training history."""

    def __init__(self, rewards_list: Sequence[float], df_history: pd.DataFrame) -> None:
        """Initialize a `Report` instance.

        Args:
            rewards_list (Sequence[float]): mean rewards of all episodes.
            df_history (pd.DataFrame): training history.
        """
        self.rewards_list = rewards_list
        self.df_history = df_history


class ReportIO:
    """A class to load an existing report, and to save a new report."""

    def __init__(self, prefix: Union[str, os.PathLike]) -> None:
        """Initialize a `ReportIO` instance.

        Args:
            prefix (Union[str, os.PathLike]): directory of an existing report, or for new report.
        """
        self.prefix = Path(prefix)

    def load(self) -> Report:
        """Load an existing report.

        Returns:
            Report: the loaded report.
        """
        with (self.prefix / "rewards_list.json").open() as f:
            rewards_list = json.load(f)
        df_history = pd.read_csv(self.prefix / "df_history.csv", low_memory=False)
        return Report(rewards_list, df_history)

    def save(self, report: Report, close_fig: bool = False) -> None:
        """Save an in-memory report to disk.

        Args:
            report (Report): an in-memory report to save.
            close_fig (bool, optional): set to ``True`` to prevent Jupyter to auto-display the
                generated figures. Defaults to False.
        """
        self.save2(report.rewards_list, report.df_history, close_fig)

    def save2(
        self,
        rewards_list: Sequence[float],
        df_history: pd.DataFrame,
        close_fig: bool = False,
    ) -> None:
        """Save the mean rewards-per-episode and training history to disk.

        Args:
            rewards_list (Sequence[float]): Save mean rewards-per-episode and training history to
                disk.
            df_history (pd.DataFrame): training history.
            close_fig (bool, optional): set to ``True`` to prevent Jupyter to auto-display the
                generated figures. Defaults to False.
        """
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


def plot_reward(rewards_list: Sequence[float]) -> matplotlib.figure.Figure:
    """Plot the mean reward of each episode.

    Args:
        rewards_list (Sequence[float]): mean rewards from all episodes.

    Returns:
        matplotlib.figure.Figure: the plot.
    """
    average_reward = sum(rewards_list) / len(rewards_list)
    fig = plt.figure(figsize=(20, 5))
    ax = sns.lineplot(data=rewards_list)
    ax.set_ylabel("Mean reward per episode", fontsize=20)
    ax.set_xlabel("Iteration", fontsize=20)
    plt.axhline(y=average_reward, color="r")
    return fig


def plot_analysis(df_history: pd.DataFrame, episode: List = None) -> matplotlib.figure.Figure:
    """Plot analysis charts of an episode.

    Args:
        df_history (pd.DataFrame): [description]
        episode (List, optional): [description]. Defaults to None.

    Returns:
        matplotlib.figure.Figure: [description]
    """
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
