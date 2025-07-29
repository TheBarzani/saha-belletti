"""
Setup script for the saha-belleti package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="saha-belleti",
    version="0.1.0",
    author="Based on SAHA et al. and Belleti et al. research",
    description="Quantum K-Coloring Circuit Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: GNU Lesser General Public License v2.1",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "qiskit>=0.45.0",
        "qiskit-aer>=0.12.0", 
        "qiskit-ibm-runtime>=0.15.0",
        "networkx>=3.0",
        "matplotlib>=3.5.0",
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "alive-progress>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
