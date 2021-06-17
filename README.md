# Energy Arbitrage using Amazon SageMaker RL

Energy storage system (ESS) can benefit the grid in many ways such as to balance and maintain the grid, or to store electricity for later use during peak demand, outage or emergency period. In order to meet demand, utilities must be prepared to distribute electricity instantaneously, through a constant balance of supply and demand. Energy storage can complement energy supply when demand is larger than current supply, if there are any disruptions in traditional forms of generation, and when renewable resources are not generating electricity which is subjected to weather condition.

Energy storage has created new opportunity for energy storage owner to generate profit via arbitrage, the difference between revenue received from energy sale (discharge) and the charging cost

## Objective

The objective of this post is to demonstrate the use of RL agent in energy arbitrage use case.

In this example, the simulated battery environment take reference to the paper [Arbitrage of Energy Storage in Electricity Markets with Deep Reinforcement Learning](https://arxiv.org/abs/1904.12232) by Hanchen Xu et al., you can get more information by reading the paper.

## Dataset

The battery simulation environment contains publicly available electric price dataset from Australian Energy Market Operator (AEOM), which you can download from [here](https://aemo.com.au/en/energy-systems/electricity/national-electricity-market-nem/data-nem/aggregated-data) as well.

Alternatively, you can run the notebook in sequence as data will be downloaded via a `bin/download_data.sh` in notebook `notebooks/00_battery_sim_notebook.ipynb`.

## What will you learn

- Training a DQN agent using Amazon SageMaker RL
- Evaluate agent performance against other baseline fixed rules agents

## Setup

It is recommended to install the `energy_storage_system` Python package to a virtual environment.

```bash
git clone https://github.com/aws-samples/sagemaker-rl-energy-storage-system.git
cd sagemaker-rl-energy-storage-system

# Activate the virtual environment where you want to install this repo.
# ...

pip install -e '.[all]'
```

## How this repository is organized

```text
.
|-- bin                          # Script to prep SageMaker notebook instance for local mode
|-- notebooks                    # Sample notebooks
|   |-- *.ipynb
|   `-- ipython_config.py        # IPython magic to let *.ipynb treat src/ as PYTHONPATH
|-- setup.py                     # To install energy_storage_system as a Python module
|-- src
|   |-- demo                     # Streamlit app
|   |-- energy_storage_system    # Module energy_storage_system
|   |-- sagemaker_rl             # Module sagemaker_rl used by SageMaker training job
|   |-- smnb_utils               # Helper functions used by sample notebooks
|   `-- source_dir               # SageMaker training job's source_dir and entrypoint script
`-- tests                        # Unit tests for SageMaker's ray launcher
```

## How to use this repository

As a quick start, run the Jupyter notebooks under `notebooks/` in sequence. These notebooks include
the end-to-end workflow, from downloading the sample data, training the agents, evaluating the
agents, generating reports (both static and interactive), and generating the Streamlit visualization
data.

Once all the notebooks have completed, you should see directory `data/` that contains the agents
output, reports, and Streamlit data. Please note that this `data/` directory is **NOT** versioned.

To run the Streamlit demo, follow these commands:

```bash
# Make sure to activate the virtual environment where you've pip install this repo
# ...

# Make sure current directory is at GITROOT, e.g., sagemaker-rl-energy-storage-system/

# Run the Streamlit app with default settings:
# - INPUT_DIR = ./data/streamlit_input
# - refresh rate at every 1 second
streamlit run src/demo/streamlit_main.py
```

Note that you can also run Streamlit demo app with custom input directory and refresh rate (see
the sample commands below).

```bash
# Show supported CLI args
streamlit run src/demo/streamlit_main.py -- --help

# Run with custom input directory and refresh rate
streamlit run src/demo/streamlit_main.py -- /tmp/my-streamlit-data --update-seconds 0.5
```

> Upcoming: steps to run the Streamlit app on a SageMaker notebook instance.

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
