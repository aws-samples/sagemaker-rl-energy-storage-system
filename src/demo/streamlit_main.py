import argparse
import os
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import pandas_bokeh  # noqa
import streamlit as st
import streamlit.components.v1 as components


def display_battery(st_batt_text, st_batt, percentage: int = 50):
    st_batt_text.markdown(f"#### Battery: {percentage}%")

    if percentage <= 20:
        st_batt.markdown(
            """
            <div class="container">
            <svg viewBox="0 0 50 100" width="50" height="100" style="border:black solid" fill="red">
                <rect x="0.5" y="80.7" width="49" height="17.8" />
            </svg>
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif percentage <= 40:
        st_batt.markdown(
            """
            <div class="container">
            <svg viewBox="0 0 50 100" width="50" height="100" style="border:black solid"
            fill="green">
                <rect x="0.5" y="60.7" width="49" height="17.8" />
                <rect x="0.5" y="80.7" width="49" height="17.8" />
            </svg>
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif percentage <= 60:
        st_batt.markdown(
            """
            <div class="container">
            <svg viewBox="0 0 50 100" width="50" height="100" style="border:black solid"
            fill="green">
                <rect x="0.5" y="40.7" width="49" height="17.8" />
                <rect x="0.5" y="60.7" width="49" height="17.8" />
                <rect x="0.5" y="80.7" width="49" height="17.8" />
            </svg>
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif percentage <= 80:
        st_batt.markdown(
            """
            <svg viewBox="0 0 50 100" width="50" height="100" style="border: black solid"
            fill="green">
                <rect x="0.5" y="20.7" width="49" height="17.8" />
                <rect x="0.5" y="40.7" width="49" height="17.8" />
                <rect x="0.5" y="60.7" width="49" height="17.8" />
                <rect x="0.5" y="80.7" width="49" height="17.8" />
            </svg>
            """,
            unsafe_allow_html=True,
        )
    else:
        st_batt.markdown(
            """
            <div class="container">
            <svg viewBox="0 0 50 100" width="50" height="100" style="border: black solid"
            fill="green">
                <rect x="0.5" y="0.5" width="49" height="17.8" />
                <rect x="0.5" y="20.7" width="49" height="17.8" />
                <rect x="0.5" y="40.7" width="49" height="17.8" />
                <rect x="0.5" y="60.7" width="49" height="17.8" />
                <rect x="0.5" y="80.7" width="49" height="17.8" />
            </svg>
            </div>
            """,
            unsafe_allow_html=True,
        )


def display_action(st_act_text, st_act, action: int):
    if action == 0:
        st_act_text.markdown("#### RL Action: Charge")
        st_act.markdown(
            """
            <svg width="100" height="200">
            <rect x="2" y="0" height="80" width="80" stroke="orange" stroke-width="2" fill="green"/>
            </svg>
            """,
            unsafe_allow_html=True,
        )
    elif action == 1:
        st_act_text.markdown("#### RL Action: Discharge")
        st_act.markdown(
            """
            <svg width="100" height="200">
            <rect x="2" y="0" height="80" width="80" stroke="orange" stroke-width="2" fill="red" />
            </svg>
            """,
            unsafe_allow_html=True,
        )
    else:
        st_act_text.markdown("#### RL Action: Hold")
        st_act.markdown(
            """
            <svg width="100" height="200">
            <rect x="2" y="0" height="80" width="80" stroke="orange" stroke-width="2" fill="white"/>
            </svg>
            """,
            unsafe_allow_html=True,
        )


def display_arrow(st):
    s1 = (
        "M3.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L9.293 8 "
        "3.646 2.354a.5.5 0 0 1 0-.708z"
    )
    s2 = (
        "M7.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L13.293 8 "
        "7.646 2.354a.5.5 0 0 1 0-.708z"
    )
    st.markdown(
        f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="50" height="200" fill="orange"
        class="bi bi-chevron-double-right" viewBox="0 0 16 16">
            <path fill-rule="evenodd"
                d="{s1}" />
            <path fill-rule="evenodd"
                d="{s2}" />
        </svg>
        """,
        unsafe_allow_html=True,
    )


def display_metrics_table(st_metrics, *args):
    price, cost, capacity, action, total_reward = args
    md_str = f"""
    **Environment states**:

    | Metrics         | Values        |
    | -------------   |:-------------:|
    | Price ($/MWh)   | {price}       |
    | Cost ($/MWh)    | {cost}        |
    | Capacity (MWh)  | {capacity}    |
    | Action          | {action}      |
    | Total reward ($)| {total_reward}|
    """
    st_metrics.markdown(
        md_str,
        unsafe_allow_html=False,
    )


def display_price(st_price, curr_df):
    fig1 = curr_df.plot_bokeh(
        show_figure=False,
        figsize=(400, 200),
        legend="top_left",
        title="Market Electric Price vs Average Energy Cost",
    )
    st_price.bokeh_chart(fig1, use_container_width=True)


def display_rewards(st_rewards, df):
    fig2 = df.plot_bokeh(
        show_figure=False,
        figsize=(550, 200),
        legend="top_left",
        title="Accumlated rewards (RL vs Baseline)",
    )
    st_rewards.bokeh_chart(fig2, use_container_width=False)


def display_time(st):
    data = datetime.now()
    fmt = "%d-%m-%Y %H:%M:%S"
    data = data.strftime(fmt)
    st.subheader(data)


@st.cache
def load_dqn_data(filepath: str = "data/result_dqn.csv"):
    df = pd.read_csv(filepath)
    df = df.rename(columns={"market_electric_price": "price", "average_energy_cost": "cost"})
    return df


@st.cache
def load_pvc_data(filepath: str = "data/result_price_vs_cost_agent.csv"):
    df = pd.read_csv(filepath)
    return df


@st.cache
def load_hist_data(filepath: str = "data/result_hist_price_agent.csv"):
    df = pd.read_csv(filepath)
    return df


def display_html_file(filename: str = "data/analysis.html"):
    f = open(filename, "r", encoding="utf-8")
    source_code = f.read()
    components.html(
        source_code,
        height=50,
    )


#######################
# HMI
#######################


def main(input_dir: Path, update_seconds: float = 0.5):
    st.set_page_config(layout="wide")
    df = load_dqn_data(input_dir / "result_dqn.csv")
    df_pvc = load_hist_data(input_dir / "result_hist_price_agent.csv")

    st.header("Energy Storage Demo")
    st.markdown("***")
    st.text("")

    st.button("Run simulation")
    a1, b1, c1, d1, e1 = st.beta_columns((6, 1, 2, 1, 2))
    st_price, arrow1, st_act_text, st_act, arrow2, st_batt_text, st_batt = (
        a1.empty(),
        b1.empty(),
        c1.empty(),
        c1.empty(),
        d1.empty(),
        e1.empty(),
        e1.empty(),
    )
    st_rewards = st.empty()
    st_metrics = st.empty()

    for index in range(100, df.shape[0] - 1, 1):
        curr_df = df.iloc[:index]
        curr_pvc_dr = df_pvc.iloc[:index]
        print(curr_df.shape)
        curr_price = int(curr_df.iloc[-1]["price"])
        curr_cost = int(curr_df.iloc[-1]["cost"])
        curr_energy = int(curr_df.iloc[-1]["energy"])
        curr_action = int(curr_df.iloc[-1]["action"])
        curr_total_reward = int(curr_df.iloc[-1]["total_reward"])
        curr_energy_pct = int(curr_energy / 80 * 100)
        metrics = (curr_price, curr_cost, curr_energy, curr_action, curr_total_reward)

        display_price(st_price, curr_df[["price", "cost"]])
        display_arrow(arrow1)
        display_action(st_act_text, st_act, curr_action)
        display_arrow(arrow2)
        display_battery(st_batt_text, st_batt, curr_energy_pct)

        df_acc_rewards = pd.DataFrame(
            {"RL": curr_df["total_reward"], "Baseline": curr_pvc_dr["total_reward"]}
        )
        display_rewards(st_rewards, df_acc_rewards)
        display_metrics_table(st_metrics, *metrics)
        # time.sleep(update_seconds)
        time.sleep(0.5)

    st.markdown("***")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_dir",
        metavar="INPUT_DIR",
        type=Path,
        nargs="?",
        default="data/streamlit_input",
        help="Directory of exploitation results.",
    )
    parser.add_argument(
        "-s",
        "--update-seconds",
        type=float,
        default=1,
        help="Update charts for every specified seconds (a float).",
    )

    # https://github.com/streamlit/streamlit/issues/337#issuecomment-544860528
    try:
        args = parser.parse_args()
    except SystemExit as e:
        # This exception will be raised if --help or invalid command line arguments
        # are used. Currently streamlit prevents the program from exiting normally
        # so we have to do a hard exit.
        os._exit(e.code)

    main(args.input_dir, args.update_seconds)
