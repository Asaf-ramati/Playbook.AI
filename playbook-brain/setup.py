from setuptools import setup, find_packages

setup(
    name="playbook-brain",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langgraph>=0.2.59",
        "langchain-openai>=0.3.14",
        "langchain-core>=0.3.28",
        "pandas>=2.0.0",
    ],
)