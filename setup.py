#!/usr/bin/env python
"""
Setup configuration for Play House Management System
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("backend/requirements.txt") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="playhouse-management",
    version="1.0.0",
    author="Play House Team",
    author_email="team@playhouse.local",
    description="Complete management system for PlayStation gaming cafe/playhouse",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/moham9dkhalil/playhouse-management",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Business",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business",
        "Topic :: Software Development :: Business Applications",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4",
            "pytest-cov>=4.1",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
            "isort>=5.12",
        ],
    },
    entry_points={
        "console_scripts": [
            "playhouse=app.main:app",
        ],
    },
)
