from setuptools import setup

extras = {"test": ["pytest", "pytest-watch", "tox"]}

setup(name="pydnd",
    description="""Py-DnD is a Python module for simple character 
    generation for the fifth edition of Dungeons and Dragons.""",
    version=0.1,
    author="Nicholas Hunt-Walker",
    author_email="nhuntwalker@gmail.com",
    extras_require=extras,
    package_dir={'': "src"},
    license="MIT",
    py_modules=["main"]
)