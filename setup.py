from setuptools import setup, find_packages

setup(
    name="tkr_unit_tests",
    version="0.1.0",
    packages=find_packages(),
    package_data={
        "tkr_unit_tests": ["data/index.html", "data/tests_skip.txt"],
    },
    include_package_data=True,
    install_requires=[
   "pytest",
   "pytest-cov",
   "allure-pytest",
   "requests_mock",
   "pytest_mock"
    ],
    entry_points={
        "console_scripts": [
            "create_structure=tkr_unit_tests.create_structure:main",
            "create=tkr_unit_tests.create:main",
            "run_tests=tkr_unit_tests.run_tests:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    author="Tucker Harley Brown",
    author_email="spynoh@gmail.com",
    description="A package to create and run tests for an existing repository",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tuckertucker/tkr_unit_tests",
    license="MIT",
)