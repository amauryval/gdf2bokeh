from setuptools import setup, find_packages

#used by meta.yaml, do not forget space
requirements = [
    "geopandas",
    "bokeh >=2.0.1"
]

setup_requirements = []

test_requirements = []

setup(
    author="amauryval",
    author_email='amauryval@gmail.com',
    description="An helper to map geodataframe on bokeh",
    entry_points={},
    install_requires=requirements,
    license="MIT license",
    long_description="",
    include_package_data=True,
    keywords='geo bokeh',
    name='geo_bokeh',
    packages=find_packages(include=["geo_bokeh", "geo_bokeh.*"]),
    # setup_requires=setup_requirements,
    test_suite='tests',
    # tests_require=test_requirements,
    url='https://github.com/amauryval/geo_bokeh',
    version='0.5.4',
    zip_safe=False,
    python_requires=">=3.6",
)