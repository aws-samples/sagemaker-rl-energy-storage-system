from gym.envs.registration import register

register(
    id="MyBatt-v1",
    entry_point="energy_storage_system.envs:SimpleBattery",
)
