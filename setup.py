import os
from typing import List

from setuptools import find_packages, setup

_repo: str = "sagemaker-rl-energy-storage-system"
_pkg: str = "energy_storage_system"
_version = "0.0.1"


def read(fname) -> str:
    """Read the content of a file.

    You may use this to get the content of, for e.g., requirements.txt, VERSION, etc.
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


# Declare minimal set for installation
required_packages: List[str] = [
    "boto3",
    "gym",
    "matplotlib",
    "pandas",
    "pandas_bokeh>=0.5.5",
    "ray[rllib]==0.8.5",  # python 3.5 to 3.8
    "sagemaker",
    "seaborn",
    "tensorflow==2.1.0",  # python 3.5 to 3.7
    "tqdm",
    "streamlit==0.82.0",
    "bokeh>=2.2.0",
]

setup(
    name=_pkg,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    version=_version,
    description="to give description",
    long_description=read("README.md"),
    author="ProServe, AWS",
    url=f"https://github.com/aws-samples/{_repo}/",
    project_urls={
        "Bug Tracker": f"https://github.com/aws-samples/{_repo}/issues/",
        "Documentation": f"https://{_repo}.readthedocs.io/en/stable/",
        "Source Code": f"https://github.com/aws-samples/{_repo}/",
    },
    license="MIT License",
    keywords="reinforcement learning sagemaker energy storage optimization",
    platforms=["any"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires=">=3.6.0,<3.8.0",
    install_requires=required_packages,
)
