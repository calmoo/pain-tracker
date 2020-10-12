from setuptools import find_packages, setup

setup(
    name="pain_tracker",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "Flask==1.1.2",
        "pymongo==3.11.0",
        "pymodm==0.4.3",
    ],
)
