from gym.envs.registration import register

from ._core import TrainResult, evaluate_episode, train

register(
    id="SimpleBattery-v1",
    entry_point="energy_storage_system.envs:SimpleBattery",
)
