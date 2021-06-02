"""

# Reference papers
- [Arbitrage of Energy Storage in Electricity Markets with Deep Reinforcement Learning](https://arxiv.org/abs/1904.12232)

"""

import io
import logging
import os
from typing import Dict, List

import boto3
import gym
import numpy as np
import pandas as pd
from gym.spaces import Box, Discrete

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s %(levelname)s] %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)


class SimpleBattery(gym.Env):
    """
    Actions:
        Type: Discrete(3)
        Num   Action
        0     Push cart to the left
        1     Push cart to the right

    Observation:
        Type: Box(8)
        Num     Observation               Min                 Max
        0       Energy storage level      -Inf                Inf
        1       Electric Cost - $/MWh     -Inf                Inf
        2       Electric Price - $/MWh    -Inf                Inf
        3       Electric Price (t-1)      0                   Inf
        4       Electric Price (t-2)      0                   Inf
        5       Electric Price (t-3)      0                   Inf
        6       Electric Price (t-4)      0                   Inf
        7       Electric Price (t-5)      0                   Inf
    """

    PI = 3.14159
    # Actions
    CHARGE = 0
    DISCHARGE = 1
    HOLD = 2

    def __init__(self, env_config: Dict):
        # Capacity: Min energy storage level (MWh)
        self.ENERGY_MIN = 0.0
        # Capacity: Max energy storage level (MWh), battery capacity
        self.ENERGY_MAX = 80.0
        # Starting capacity
        self.STARTING_ENERGY = 40.0
        # Power rating: Max charge rate (MW)
        self.MAX_CHARGE_PWR = 4.0
        # Power rating: Max discharge rate (MW)
        self.MAX_DISCHARGE_PWR = 2.0
        # wear and tear ($/MW)
        self.BETA = 1.0
        # every step is 1 hour
        self.DURATION = 1
        # efficiency constant
        self.EFF = 1.0
        # Historical price horizon for states
        self.HIST_PRICE_HORIZON = 5
        # Each trajectories is one week (168h)
        self.MAX_STEPS_PER_EPISODE = 168

        self.LOCAL = None
        self.FILEPATH = None

        # Default environment configuration. which will be added to env_config
        config_defaults = {
            "ENERGY_MIN": 0.0,
            "ENERGY_MAX": 80.0,
            "STARTING_ENERGY": 40.0,
            "MAX_CHARGE_PWR": 4.0,
            "MAX_DISCHARGE_PWR": 2.0,
            "BETA": 1.0,
            "DURATION": 1,
            "EFF": 1.0,
            "HIST_PRICE_HORIZON": 5,
            "MAX_STEPS_PER_EPISODE": 168,
            "FILEPATH": "data/PRICE_AND_DEMAND_202103_NSW1.csv",
            "LOCAL": True,
        }

        # Add new environment config passed in as params
        for key, default_val in config_defaults.items():
            # Get value for key, if none then return 'val'. env_config take priority
            new_val = env_config.get(key, default_val)  # Override defaults with constructor parameters
            self.__dict__[key] = new_val
            if key not in env_config:
                env_config[key] = new_val

        # Load energy price ($/MWh)
        if self.LOCAL:
            self.df_price = self._get_data(self.FILEPATH)
        else:
            self.df_price = self._get_data_s3()
        self.price_length = self.df_price.shape[0]

        # TODO Create features
        # self.df_price["time"] = self.df_price["time"]
        # self.df_price["hour"] = self.df_price.time.dt.hour
        # self.df_price["week"] = self.df_price.time.dt.week
        # self.df_price["sin_time"] = np.sin(2 * PI * self.df_price.hour / 24)
        # self.df_price["cos_time"] = np.cos(2 * PI * self.df_price.hour / 24)
        # self.df_price["sin_week"] = np.sin(2 * PI * self.df_price.week / 52)
        # self.df_price["cos_week"] = np.cos(2 * PI * self.df_price.week / 52)

        # ACTION/OBSERVATION space, this will change according hist horizon
        self.action_space = Discrete(3)
        self.observation_space = Box(-np.inf, np.inf, shape=(3 + self.HIST_PRICE_HORIZON,), dtype=np.float64)
        self.initialized = False

    def _get_data(self, fullpath):
        """Return price series."""
        if os.getenv("SM_HOSTS") is not None:
            sagemaker_mount = "/opt/ml/code/"
            fullpath = sagemaker_mount + fullpath
            print("Runing on SageMaker:")
            print(f"Loading data from: {fullpath}")

        df = pd.read_csv(fullpath)
        df["SETTLEMENTDATE"] = pd.to_datetime(df["SETTLEMENTDATE"])  # type:ignore
        df = df.resample("1h", on="SETTLEMENTDATE").mean()
        df = df.reset_index(drop=False)
        df = df.rename(columns={"TOTALDEMAND": "demand", "RRP": "price", "SETTLEMENTDATE": "time"})
        # Remove outlier (> $100)
        df = df[df["price"] <= 100]
        print(f"Data size: {df.shape}")
        return df

    def _get_data_s3(self):
        """Return price series."""

        def _read_s3_file_csv(bucket, key, header=None, usecols=None, index_col=None):
            s3_client = boto3.client("s3")
            response = s3_client.get_object(Bucket=bucket, Key=key)
            response_body = response["Body"].read()
            df = pd.read_csv(
                io.BytesIO(response_body),
                header=header,
                delimiter=",",
                low_memory=False,
                # encoding="iso-8859-1",
                usecols=usecols,
                index_col=index_col,
            )
            return df

        print("Read from S3...")
        df = _read_s3_file_csv(bucket="demo-rl", key="battery/PRICE_AND_DEMAND_202103_NSW1.csv", header=0)
        df["SETTLEMENTDATE"] = pd.to_datetime(df["SETTLEMENTDATE"])  # type:ignore
        df = df.resample("1h", on="SETTLEMENTDATE").mean()
        df = df.reset_index(drop=False)
        df = df.rename(columns={"TOTALDEMAND": "demand", "RRP": "price", "SETTLEMENTDATE": "time"})
        # Remove outlier (> $100)
        df = df[df["price"] <= 100]
        print(f"Data size: {df.shape}")
        return df

    def reset(self):
        # initial energy (MWh)
        self.energy_level = self.STARTING_ENERGY
        # Initial step, start from 0+hist_horizon, a random t-horizon
        self.index = np.random.randint(0 + self.HIST_PRICE_HORIZON, self.price_length - self.MAX_STEPS_PER_EPISODE)

        # Reward ($): price diff ($/MWh) * discharge energy (MWh) + fixed cost
        self.reward = 0.0
        # Cost ($/MWh), same unit as price
        self.cost = 40.0
        self.counter = 1

        historical_price: List = (
            self.df_price["price"].iloc[self.index - self.HIST_PRICE_HORIZON : self.index][::-1].to_list()
        )
        state: List = [
            self.energy_level,
            self.cost,
            self.df_price["price"].iloc[self.index],
        ]
        state = state + historical_price

        # logging.info("Initial setting:")
        # logging.info(
        #     f"Energy level:{self.energy_level}, start index:{self.index}, max steps: {self.MAX_STEPS_PER_EPISODE}"
        # )
        self.initialized = True

        return state

    def step(self, action: int):
        assert self.initialized, "Environmet is not initialized"
        # Sell
        if action == self.DISCHARGE:
            discharge_pwr = min(self.MAX_DISCHARGE_PWR, (self.energy_level - self.ENERGY_MIN) / self.DURATION)

            # Update enery level
            self.energy_level = self.energy_level - discharge_pwr * self.DURATION

            # fix cost = rate ($/MW) * power (MW)
            discharge_cost = self.BETA * discharge_pwr
            # Dependant on current price in market ($/MWh * MWh)
            reward = (
                (self.df_price["price"].iloc[self.index] * self.EFF - self.cost) * (discharge_pwr * self.DURATION)
            ) - discharge_cost

        # Buy
        elif action == self.CHARGE:
            charge_pwr = min(self.MAX_CHARGE_PWR, (self.ENERGY_MAX - self.energy_level) / self.DURATION)
            # Cost only change during charging ($/MWh) = total cost (current+new) / total energy (current+new)
            total_energy_cost = (self.cost * self.energy_level) + (
                self.df_price["price"].iloc[self.index] * charge_pwr * self.DURATION / self.EFF
            )
            total_energy = self.energy_level + charge_pwr * self.DURATION
            self.cost = total_energy_cost / total_energy

            # Update energy level
            self.energy_level = self.energy_level + charge_pwr * self.DURATION

            # fix cost = rate ($/MW) * power (MW)
            charge_cost = self.BETA * charge_pwr
            reward = -1 * charge_cost

        # Hold
        elif action == self.HOLD:
            # No change in energy level
            reward = 0
        else:
            assert False, "Invalid action"

        # Include historical price in state
        historical_price: List = (
            self.df_price["price"].iloc[self.index - self.HIST_PRICE_HORIZON : self.index][::-1].to_list()
        )
        state: List = [
            self.energy_level,
            self.cost,
            self.df_price["price"].iloc[self.index],
        ]
        state = state + historical_price

        # One trajectories or episode has MAX_T hours
        if self.counter >= self.MAX_STEPS_PER_EPISODE:
            done = True
        else:
            done = False

        info = {}

        self.index += 1
        self.counter += 1

        return state, reward, done, info


if __name__ == "__main__":
    env_config = {"MAX_STEPS_PER_EPISODE": 5, "LOCAL": True}
    env = SimpleBattery(env_config)
    np.random.seed(1)

    for i in range(2):
        state = env.reset()
        done = False
        step = 1
        while not done:
            action = np.random.choice([SimpleBattery.CHARGE, SimpleBattery.DISCHARGE, SimpleBattery.HOLD])
            state, reward, done, info = env.step(action)
            print(f"Episode {i+1} ({step}): {state}, {reward}, {done}, {info}")
            step += 1
