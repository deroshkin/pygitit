from setuptools import setup, find_packages

VERSION = "0.1.0"

setup(
    name="pygitit",
    version=VERSION,
    description="A port of gitit to python.",
    author="Dmytro Yeroshkin",
    author_email="dmytro.yeroshkin@gmail.com",
    url="https://github.com/deroshkin/pygitit",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Bottle",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: MIT License",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Wiki",
        "Topic :: Text Processing :: Markup :: Markdown",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Software Development :: Version Control :: Mercurial",
    ],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "pygitit = pygitit.main:main",
        ]
    },
    install_requires=("bottle", "gitpython", "mercurial"),
    include_package_data=True,
    python_requires=">=3.7.0",
)
