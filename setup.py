from pathlib import Path

from setuptools import find_packages, setup

CURRENT_DIR = Path(__file__).parent

with open(f"{CURRENT_DIR}/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Nerd-Storage",
    description="A simple LAN storage.",
    version="0.2.1",
    license="GPLv3",
    author="0xHaru",
    author_email="0xharu.git@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="storage flask webserver homeserver",
    url="https://github.com/0xHaru/Nerd-Storage",
    project_urls={
        "Bug Tracker": "https://github.com/0xHaru/Nerd-Storage/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    python_requires=">=3.6",
    install_requires=["flask", "flask-login", "jinja2"],
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "nerdstorage=nerdstorage.__main__:main",
        ]
    },
)
