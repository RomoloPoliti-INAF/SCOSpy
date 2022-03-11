import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SCOSpy", # Replace with your own username
    version="0.4.4",
    author="Romolo Politi",
    author_email="Romolo.Politi@inaf.it",
    description="Python library to read the SCOS-2000 header",
    license="General Public License v3 (GPLv3)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.ict.inaf.it/gitlab/romolo.politi/scospy",
    packages=setuptools.find_packages(),
    install_requires=[
        'bitstring',
    ],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
