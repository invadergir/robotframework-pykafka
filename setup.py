from setuptools import setup

setup(
    name='robotframework_pykafka',
    packages=['robotframework_pykafka'],  # this must be the same as the name above
    version='0.10',
    install_requires=[
        'robotframework >= 3.0.4',
        'pykafka >= 2.7.0'
    ],
    description='This is a robot framework wrapper around pykafka, the best python kafka library out there as of this writing, and the only one that supports kafka 1.0 and 1.1.',
    author='Michael Sesterhenn',
    author_email='invadergir@users.noreply.github.com',
    url='https://github.com/invadergir/robotframework-pykafka',
    download_url='https://github.com/invadergir/robotframework_pykafka/tarball/0.10',
    keywords=['robotframework', 'kafka','testing'],
    classifiers=["Programming Language :: Python :: 2.7",
                 "Topic :: Software Development :: Libraries :: Python Modules"]
)
