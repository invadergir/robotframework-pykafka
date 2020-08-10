from setuptools import setup

setup(
    name='robotframework_pykafka',
    packages=['robotframework_pykafka'],  # this must be the same as the name above
    version='0.12',
    python_requires='>=3.5',
    install_requires=[
        'robotframework >= 3.2.1',
        'pykafka >= 2.8.0'
    ],
    description='This is a robot framework wrapper around pykafka, the best python kafka library out there as of this writing, and the only one that supports kafka 1.0 through and 2.3.',
    author='Michael Sesterhenn',
    author_email='invadergir@users.noreply.github.com',
    url='https://github.com/invadergir/robotframework-pykafka',
    download_url='https://github.com/invadergir/robotframework_pykafka/tarball/0.11',
    keywords=['robotframework', 'kafka','testing'],
    classifiers=["Programming Language :: Python :: 3",
                 "Topic :: Software Development :: Libraries :: Python Modules"]
)
