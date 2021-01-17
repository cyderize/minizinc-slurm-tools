import setuptools

with open("README.md", "r") as fp:
    long_description = fp.read()

setuptools.setup(
    name="minzinc_slurm_tools",
    version="0.0.1",
    author="Jason Nguyen",
    author_email="jason.nguyen@monash.edu",
    description="MiniZinc SLURM analysis tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cyderize/minizinc-slurm-tools",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "mznst=mznst.cli:main",
        ],
    },
    install_requires=[
        "pytest>=6,<7",
        "click>=7,<8",
        "minizinc>=0.4.2,<0.5",
        "pandas>=1.1,<2",
        "seaborn>=0.11",
        "ruamel.yaml>=0.16",
        "bokeh>=2.2.3"
    ],
)
