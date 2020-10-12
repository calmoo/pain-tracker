from setuptools import find_packages, setup

setup(
    name="pain_tracker",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "Flask==1.1.2",
        "Flask-JWT-Extended==3.24.1"
        "pymongo==3.11.0",
        "pymodm==0.4.3",
        "argon2-cffi==20.1.0",
    ],
)
