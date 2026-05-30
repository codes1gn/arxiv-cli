"""Setup configuration for arxiv-cli."""
from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="arxiv-cli",
    version="1.0.0",
    description="Search and download arXiv papers from the terminal — agent-friendly CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="codes1gn",
    url="https://github.com/codes1gn/arxiv-cli",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "arxiv>=2.1.0",
    ],
    extras_require={
        "rich": ["rich>=13.0"],
    },
    entry_points={
        "console_scripts": [
            "arxiv=arxiv_cli.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Utilities",
    ],
    keywords="arxiv papers search cli agent tool academic",
)
