from setuptools import setup

setup(
    name="alfred",
    version="1.0.0",
    description="CLI Bot assistant. Package for adding data to address book, read/update/delete it, adding notes etc.",
    url="https://github.com/adrkarpl",
    author="'Gotham Devs': Katarzyna Drajok, Katarzyna Czempiel, Rafał Pietras, Dawid Radzimski, Adrian Karwat",
    author_email="katarzyna.drajok@gmail.com; katarzyna.czempiel@gmail.com; rafal.radx@gmail.com; dawid.radzimski@gmail.com; adr.karwat@gmail.com",
    readme="README.md",
    license="MIT",
    packages=["alfred"],
    requires=["thefuzz"],
    entry_points={"console_scripts": ["alfred-run=alfred.run_alfred:main"]},
)
