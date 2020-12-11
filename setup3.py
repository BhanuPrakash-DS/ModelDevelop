from setuptools import setup, find_packages
setup(
    name="ModelDevelop",
    version="0.1",
    packages=find_packages(),
    script_args=['--quiet', 'bdist_egg'],
    classifiers=['Programming Language :: Python :: 3.4',
                 'Programming Language :: Pyspark :: 2.3.1',
                 'Development Status :: Initial'],
    install_requires=[
        'boto>=2.42.0',
        # 'boto3>=1.5.28',
        # 'pymysql>=0.8.0',
        # 'python-dateutil>=2.7.2',
        # 'enum34>=1.1.6',
        # 'sqlalchemy'
    ]
)