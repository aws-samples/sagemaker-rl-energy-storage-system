from ray.tune.registry import register_env
from sagemaker_rl.ray_launcher import SageMakerRayLauncher


class MyLauncher(SageMakerRayLauncher):
    """Battery optimization using Ray-RLLib on SageMaker.

    By default, PyTorch is used. However, TensorFlow can be chosen by setting SageMaker
    estimator's hyperparameter ``"rl.training.config.use_pytorch"`` to ``False``.

    See also: :class:`sagemaker_rl.ray_launcher.SageMakerRayLauncher`.
    """

    def register_env_creator(self):
        """Register a battery gym environment.

        See also: :meth:`~sagemaker_rl.ray_launcher.SageMakerRayLauncher.register_env_creator`.
        """
        from energy_storage_system.envs import SimpleBattery

        register_env("SimpleBattery-v1", lambda env_config: SimpleBattery(env_config))

    def get_experiment_config(self):
        """Get the default configuration, which will be overriden by hyperparameters.

        See also: :meth:`~sagemaker_rl.ray_launcher.SageMakerRayLauncher.get_experiment_config`.
        """
        return {
            "training": {
                "env": "SimpleBattery-v1",
                "run": "DQN",
                "config": {
                    "use_pytorch": True,
                    "env_config": {
                        "MAX_STEPS_PER_EPISODE": 168,
                    },
                },
                "stop": {
                    "training_iteration": 5,
                },
            }
        }


if __name__ == "__main__":
    MyLauncher().train_main()
