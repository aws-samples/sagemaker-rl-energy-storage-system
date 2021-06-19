from abc import ABC, abstractmethod

import numpy as np

from .envs import SimpleBattery


class Agent(ABC):
    @abstractmethod
    def compute_action(self, state) -> int:
        pass


class RandomAgent(Agent):
    """Random agent."""

    actions = (SimpleBattery.CHARGE, SimpleBattery.DISCHARGE, SimpleBattery.HOLD)

    def compute_action(self, state) -> int:
        return np.random.choice(self.actions)


class PriceVsCostAgent(Agent):
    """What should be the initial initial energy costs?

    Buy: electric price < electric cost
    Sell: electric price > electric cost
    """

    def compute_action(self, state) -> int:
        electric_price = state[2]
        electric_cost = state[1]

        if electric_price > electric_cost:
            action = SimpleBattery.DISCHARGE
        elif electric_price < electric_cost:
            action = SimpleBattery.CHARGE
        else:
            action = SimpleBattery.HOLD

        return action


class MovingAveragePriceAgent(Agent):
    """
    Buy: market price < past last x days average price
    Sell: market price > past last x days average price
    """

    def __init__(self, days: int = 5) -> None:
        if days < 1:
            raise ValueError(f"Days must be > 0, but getting {days}")
        self.days = days

    def compute_action(self, state) -> int:
        market_price = state[2]
        past_average_price = sum(state[-self.days :]) / len(state[-self.days :])

        if market_price > past_average_price:
            action = SimpleBattery.DISCHARGE
        elif market_price < past_average_price:
            action = SimpleBattery.CHARGE
        else:
            action = SimpleBattery.HOLD

        return action
