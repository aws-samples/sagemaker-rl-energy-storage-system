import argparse
import warnings
from typing import Tuple

import bokeh as bk
import pandas as pd
import pandas_bokeh  # noqa

try:
    from smallmatter.pathlib import Path2 as Path
except ImportError:
    warnings.warn(
        "smallmatter.pathlib.Path2 not importable. Direct r/w to Amazon S3 not available."
    )
    from pathlib import Path

from .utils import Report, ReportIO


def load_energy_inventories(input_dir: Path) -> pd.DataFrame:
    """Load energy inventory levels of all reports under ``input_dir/``."""
    dfs = []
    for report_dir in input_dir.iterdir():
        try:
            report: Report = ReportIO(report_dir).load()
            ser = report.df_history["energy"]
            ser.rename(report_dir.name, inplace=True)
            dfs.append(ser)
        except Exception:
            # Skip non-reports files or dirs, such as .DS_Store etc.
            print("Skipping", report_dir)

    return pd.concat(dfs, axis=1)


def to_html(df: pd.DataFrame, output_dir: Path, figsize: Tuple[int, int] = (1280, 240), **kwargs):
    """Plot the interactive inventory chart of an episode.

    Args:
        df (pd.DataFrame): energy inventory level.
        output_dir (Path): the output directory to save the generated interactive html.
        figsize (Tuple[int, int], optional): size of individual chart. Defaults to (1280, 240).
        kwargs: additional ``kwargs`` to `pandas_bokeh.plot_bokeh()`.
    """
    kwargs = dict(**kwargs, figsize=figsize, show_figure=False)
    plot = df.plot_bokeh(kind="line", title="Energy (Inventory Level)", **kwargs)
    bk.io.save(
        plot,
        filename=(output_dir / "energy_inventory.html"),
        resources=bk.resources.INLINE,
        title="Energy (Inventory Level)",
    )


def main(input_dir, output_dir):
    """CLI functionalities."""
    output_dir.mkdir(parents=True, exist_ok=True)
    df_all_agents = load_energy_inventories(input_dir)
    to_html(df_all_agents, output_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=Path, metavar="INPUT_DIR")
    parser.add_argument("-o", "--output-dir", type=Path, default=".")
    args = parser.parse_args()
    main(args.input_dir, args.output_dir)
