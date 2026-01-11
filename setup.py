"""
Setup script for BEAST Framework
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ""

setup(
    name="beast",
    version="0.1.0",
    description="Dynamic Framework for Techni Beer Sheva Military School",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Techni Beer Sheva",
    packages=find_packages(),
    install_requires=[
        "python-dotenv>=1.0.0",
        "SQLAlchemy>=2.0.0",
        "PyYAML>=6.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
