from setuptools import setup

setup(
    name='cuboxGPT',
    version='0.1.0',
    py_modules=['webParser', 'db', 'chatFromDB'],
    install_requires=[
        'Click',
        'requests',
        'bs4',
        'rich',
        'langchain',
        'openai'
    ],
    entry_points={
        'console_scripts': [
            'webParser = webParser:loadWebContentFromCuboxExport',
            'db = db:setDatabase',
            'chatFromDB = chatFromDB:search'
        ],
    },
)
