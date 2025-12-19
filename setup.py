"""Setup script para PyRUT."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyrut",
    version="1.0.0",
    author="PyRUT Team",
    author_email="",
    description="Librería Python para validación de RUTs chilenos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pyrut/pyrut",
    packages=find_packages(exclude=["tests", "examples"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Natural Language :: Spanish",
    ],
    keywords="rut chile validacion verificador chileno cedula documento",
    python_requires=">=3.8",
    install_requires=[],  # Sin dependencias externas
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/pyrut/pyrut/issues",
        "Source": "https://github.com/pyrut/pyrut",
    },
)
