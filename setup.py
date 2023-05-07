from setuptools import setup

setup(
    name='cuboxGPT',
    version='0.1.0',
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
)
