import argparse
import warnings
from typing import Sequence, Tuple

import bokeh as bk
import pandas as pd
import pandas_bokeh  # noqa
from bokeh.layouts import column, gridplot
from bokeh.models import Div

try:
    from smallmatter.pathlib import Path2 as Path
except ImportError:
    warnings.warn(
        "smallmatter.pathlib.Path2 not importable. Direct r/w to Amazon S3 not available."
    )
    from pathlib import Path

from .utils import Report, ReportIO


# Rewards chart.
def plot_rewards(rewards_list: Sequence[float], **kwargs) -> bk.models.plots.Plot:
    """Plot the interactive mean reward of each episode.

    Args:
        rewards_list (Sequence[float]): mean rewards from all episodes.

    Returns:
        matplotlib.figure.Figure: the plot.
    """
    df = pd.DataFrame(
        {
            "rewards": rewards_list,
            "mean": sum(rewards_list) / len(rewards_list),
        }
    )

    plot = df.plot_bokeh(
        kind="line",
        title="Rewards",
        xlabel="Episode",
        ylabel="Mean reward per episode",
        colormap=["blue", "red"],
        show_figure=False,
        **kwargs,
    )

    # We don't want tooltip on the mean line. Is there a better way than this hack?
    # NOTE: hvplot allows specifying df columns to enable hover using `hover_col`.
    #       See https://hvplot.holoviz.org/user_guide/Customization.html
    #       Seems like a good reason to move to hvplot (though I prefer pandas_bokeh's
    #       default layout better).
    plot.tools.remove(plot.tools[-1])

    return plot


def plot_analysis(df: pd.DataFrame, **kwargs) -> bk.models.plots.Plot:
    """Plot the interactive evaluation charts of an episode.

    Args:
        df (pd.DataFrame): training history.
        kwargs: additional ``kwargs`` to `pandas_bokeh.plot_bokeh()`.

    Returns:
        bk.models.plots.Plot: the plot.
    """
    kwargs = dict(**kwargs, show_figure=False)
    plots = [
        df[["cost", "price"]].plot_bokeh(
            kind="line", title="Cost vs Price", **kwargs
        ),  # TODO: off tooltip on all-but-one line.
        df[["action"]].plot_bokeh(kind="scatter", title="Actions Taken", **kwargs),
        df[["reward"]].plot_bokeh(kind="line", title="Rewards", **kwargs),
        df[["total_reward"]].plot_bokeh(kind="line", title="Total Reward", **kwargs),
        df[["energy"]].plot_bokeh(kind="line", title="Energy (Inventory Level)", **kwargs),
    ]
    return plots


def to_html(report: Report, output_dir: Path, figsize: Tuple[int, int] = (1280, 240)) -> None:
    """Generate an interactive html report and save to disk.

    Args:
        report (Report): generate interactive html of this in-memory report.
        output_dir (Path): the output directory.
        figsize (Tuple[int, int], optional): size of individual charts. Defaults to (1280, 240).
    """
    bk.io.save(
        plot_rewards(report.rewards_list, figsize=figsize),
        filename=(output_dir / "rewards.html"),
        resources=bk.resources.INLINE,
        title="Rewards",
    )

    grid_analysis = gridplot(
        plot_analysis(report.df_history, figsize=figsize),
        ncols=1,
        merge_tools=False,
    )
    bk.io.save(
        grid_analysis,
        filename=(output_dir / "analysis.html"),
        resources=bk.resources.INLINE,
        title="Analysis",
    )

    # Save another all-in-one .html
    # NOTE: with pandas-bokeh, save() requires new grid AND p_*, or else exception:
    #
    #     RuntimeError: Models must be owned by only a single document, SaveTool(id='1243', ...)
    #     is already in a doc
    #
    grid_all = column(
        Div(text="<h1>plot_rewards()</h1>"),
        plot_rewards(report.rewards_list, figsize=figsize),
        Div(),
        Div(text="<h1>plot_analysis()</h1>", sizing_mode="scale_width", width=figsize[0]),
        gridplot(plot_analysis(report.df_history, figsize=figsize), ncols=1, merge_tools=False),
    )
    bk.io.save(
        grid_all,
        filename=(output_dir / "all.html"),
        resources=bk.resources.INLINE,
        title="All-in-One",
    )


def main(input_dir, output_dir):
    """CLI functionality."""
    report = ReportIO(input_dir).load()
    output_dir.mkdir(parents=True, exist_ok=True)
    to_html(report, output_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=Path, metavar="INPUT_DIR")
    parser.add_argument("-o", "--output-dir", type=Path, default=".")
    args = parser.parse_args()
    main(args.input_dir, args.output_dir)
