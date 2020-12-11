from setuptools import setup, find_packages


# with open('README.md') as f:
#     readme = f.read()

# with open('LICENSE') as f:
#     license = f.read()

license = ''

setup(
    name='ModelDevelop',
    version='0.1.0',
    description='ModelDevelop data pre processing and models ingestion',
    #long_description=readme,
    license=license,
    classifiers=['Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: spark  :: 2.3.1',
                 'Development Status   :: Initial'],
    install_requires=[
        # 'boto>=2.42.0',
        # 'boto3>=1.5.28',
        # 'pymysql>=0.8.0',
        # 'python-dateutil>=2.7.2',
        # 'enum34>=1.1.6',
        # 'sqlalchemy'
    ],
    packages=find_packages(exclude=['']),
    test_suite="nose.collector"
)
