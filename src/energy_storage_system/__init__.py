from typing import TypeVar

from gym.envs.registration import register

register(
    id="MyBatt-v1",
    entry_point="energy_storage_system.envs:SimpleBattery",
)

T = TypeVar("T")


def hello_world(s: T) -> T:
    print("Hello world,", s)
    return s
