# Energy Arbitrage using Amazon SageMaker RL

Energy storage system (ESS) can benefit the grid in many ways such as to balance and maintain the grid, or to store electricity for later use during peak demand, outage or emergency period. In order to meet demand, utilities must be prepared to distribute electricity instantaneously, through a constant balance of supply and demand. Energy storage can complement energy supply when demand is larger than current supply, if there are any disruptions in traditional forms of generation, and when renewable resources are not generating electricity which is subjected to weather condition.

Energy storage has created new opportunity for energy storage owner to generate profit via arbitrage, the difference between revenue received from energy sale (discharge) and the charging cost

## Objective

The objective of this post is to demonstrate the use of RL agent in energy arbitrage use case.

In this example, the simulated battery environment take reference to the paper [Arbitrage of Energy Storage in Electricity Markets with Deep Reinforcement Learning](https://arxiv.org/abs/1904.12232) by Hanchen Xu et al., you can get more information by reading the paper.

## Dataset

The battery simulation environment contains publicly available electric price dataset from Australian Energy Market Operator (AEOM), which you can download from [here](https://aemo.com.au/en/energy-systems/electricity/national-electricity-market-nem/data-nem/aggregated-data) as well.

## What will you learn

- Training a DQN agent using Amazon SageMaker RL
- Evaluate agent performance against other baseline fixed rules agents

## Setup

Make sure your python virtual environment has necessary python packages installed.

`pip install -r requirements.txt`

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
