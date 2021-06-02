#!/usr/bin/env bash

conda create -y --prefix /home/ec2-user/SageMaker/envs/custom_p37 python=3.7 ipykernel
conda activate /home/ec2-user/SageMaker/envs/custom_p37
pip install -r requirements.txt
