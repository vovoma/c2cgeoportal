from setuptools import setup

readme = open('README.md').read()

setup(
    name="c2cgeoportal_commons",
    version="2.3.0.dev0",
    packages=["c2cgeoportal_commons"],
    description="c2cgeoportal commons",
    long_description=readme,
    include_package_data=True,
    author="Camptocamp",
    author_email="info@camptocamp.com",
    install_requires=[
        "c2cgeoform",
        "papyrus",
        'lingua>=2.4',
        'babel',
        'deform',
        'pyproj',  # sudo apt install python3-dev", why not with c2cgeoform ?
        'ColanderAlchemy>=0.3.2'  # why not with c2cgeoform ?
    ],
    extras_require={
        'testing': [
            'psycopg2',
            'pytest',
            'pytest-cov',
            'flake8==3.4.1',
        ],
    },
    entry_points={
        'console_scripts': [
            'initialize_db_main = c2cgeoportal_commons.scripts.initializedb:main',
        ],
        'paste.app_factory': [
            'test_app = c2cgeoportal_commons.tests:app',
        ],
    },
)
