from setuptools import setup, find_packages

try:
    with open("readme.md", "r", encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "A Python library for integrating FileMaker databases with the FileMaker Data API."

setup(
    name="python-fm-dapi-weaver",
    # version="0.1.0",
    use_scm_version={"local_scheme": "no-local-version"},
    setup_requires=[
        "setuptools>=42",
        "setuptools-scm",
    ], 
    author="Mindfire Digital LLP",
    author_email="swathim@mindfiresolutions.com",
    description="A Python wrapper for seamless communication with FileMaker dababases.",    
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mindfiredigital/python-fm-dapi-weaver", 
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "fastapi",
        "uvicorn",
        "requests",
        "python-multipart",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="filemaker data-api python api database client fastapi storage",
)