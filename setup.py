from setuptools import setup, find_packages

setup(
    name='my_fastapi_blog',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'fastapi',  # Assuming FastAPI is a dependency
        'uvicorn',  # Assuming Uvicorn is a dependency
        # Add other dependencies here, like SQLAlchemy, databases, Pydantic, etc.
        # Format is 'package_name==version_number' or just 'package_name' for latest version
    ],
    extras_require={
        "dev": [
            "pytest",   # If you use pytest for testing
            # Add other development dependencies like pytest-asyncio, coverage, etc.
        ]
    },
    entry_points={
        'console_scripts': [
            'start=my_fastapi_blog.app.main:run'  # Change this if the path to your app is different
        ],
    },
)
