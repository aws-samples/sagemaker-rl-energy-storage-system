from gym.envs.registration import register

register(
    id="SimpleBattery-v1",
    entry_point="energy_storage_system.envs:SimpleBattery",
)
