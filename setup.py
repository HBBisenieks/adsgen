from setuptools import setup

setup(
    name='adsgen',
    version='0.4.1',
    description="""Generate usernames and other account info from Blackbaud
                exports""",
    url="https://headroyce.org",
    author='Hilary B. Brenum',
    author_email='hbrenum@headroyce.org',
    license='MIT',
    packages=['adsgen'],
    install_requires=[
        'python-ldap',
        'unidecode',
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'adsgen = adsgen:main',
        ],
    },
    include_package_data=True,
    data_files=[('/etc', ['adsgen.cfg'])],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
