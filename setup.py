"""Setup script for EasyRedis package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read version from __version__.py
version = {}
with open("easy_redis/__version__.py") as f:
    exec(f.read(), version)

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8")

setup(
    name="easy-redis",
    version=version["__version__"],
    author=version["__author__"],
    description=version["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/easy-redis",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
    python_requires=">=3.8",
    install_requires=[
        "redis>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
        ],
    },
)
