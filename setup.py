from setuptools import setup, find_packages

requirements = []

setup_requirements = []

test_requirements = []

setup(
    author="amauryval",
    author_email='amauryval@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    description="An helper to map geodataframe on bokeh",
    entry_points={},
    install_requires=requirements,
    license="MIT license",
    long_description="",
    include_package_data=True,
    keywords='bokeh',
    name='geo_bokeh',
    packages=find_packages(include=['geo_bokeh']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/amauryval/geo_bokeh',
    version='0.5.1',
    zip_safe=False,
)