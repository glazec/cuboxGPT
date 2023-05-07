from setuptools import setup
import os
# Read the contents of the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cuboxGPT',
    version='0.1.1',
    author='Glaze',
    description='Use GPT to chat/search your large Cubox datasets',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    readme='README.md',
    keywords=['Cubox', 'search', 'AI', 'GPT', 'langchain'],
    url='https://github.com/glazec/cuboxGPT',
    py_modules=['webParser', 'db', 'chatFromDB', 'cuboxGPT'],
    install_requires=[
        'typer',
        'requests',
        'bs4',
        'rich',
        'langchain',
        'openai',
        'chromadb',
        'tiktoken'
    ],
    entry_points={
        "console_scripts": [
            "cuboxGPT=cuboxGPT:app",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",

    ],
)
