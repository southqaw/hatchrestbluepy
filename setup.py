import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hatchrestbluepy",
    version="1.0.1",
    author="Klint Youngmeyer",
    author_email="kkyoungmeyer@gmail.com",
    description="A Python library to control the Hatch Rest sound machine, using bluepy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/southqaw/hatchrestbluepy",
    project_urls={
        "Bug Tracker": "https://github.com/southqaw/hatchrestbluepy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Home Automation",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        'bluepy',
    ],
)
