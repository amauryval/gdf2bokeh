from setuptools import setup, find_packages

#used by meta.yaml, do not forget space
requirements = [
    "geopandas >=0.8.0",
    "bokeh >=2.0.1"
]

setup_requirements = []

test_requirements = []

setup(
    author="amauryval",
    author_email='amauryval@gmail.com',
    url="https://github.com/amauryval/gdf2bokeh",
    version='2.1.0',
    description="An easy way to map geodataframes on bokeh",
    entry_points={},
    install_requires=requirements,
    license="BSD",
    long_description="",
    include_package_data=True,
    keywords='mapping geodataframe bokeh',
    name='gdf2bokeh',
    packages=find_packages(include=["gdf2bokeh", "gdf2bokeh.*"]),
    # setup_requires=setup_requirements,
    test_suite='tests',
    # tests_require=test_requirements,
    zip_safe=False,
    python_requires=">=3.8",
)