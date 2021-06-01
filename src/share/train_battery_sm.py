from ray.tune.registry import register_env
from sagemaker_rl.ray_launcher import SageMakerRayLauncher


class MyLauncher(SageMakerRayLauncher):

    def register_env_creator(self):
        from battery_env_sm import SimpleBattery
        register_env("SimpleBattery-v1",
                     lambda env_config: SimpleBattery(env_config))

    def get_experiment_config(self):
        multi = 1
        return {
            "training": {
                "env": "SimpleBattery-v1",
                "run": "DQN",
                "config": {
                    "use_pytorch": True,
                    "env_config": {
                        'MAX_STEPS_PER_EPISODE': 168,
                    },
                },
                "stop": {
                    "training_iteration": 5,
                },
            }
        }

if __name__ == "__main__":
#     import ray
#     import torch
#     print("Ray version:", ray.__version__)
#     print("Torch version:", torch.__version__)
    MyLauncher().train_main()
