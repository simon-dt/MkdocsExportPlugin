from setuptools import setup, find_packages
import os

def read_file(fname):
    "Read a local file"
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='mkdocexport',
    version='0.0.1',
    description="export docs to json",
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    keywords='mkdocs python markdown export',
    url='',
    author='Simon de Turck',
    author_email='simon.de.turck@philips.com',
    license='MIT',
    python_requires='>=3.6',
    install_requires=[
        'mkdocs>=1.1',
        'jinja2',
    ],
    packages=['mkdocexport'],
    package_data={'export': ['templates/*.json.template']},
    entry_points={
        'mkdocs.plugins': [
            'mkdocexport = mkdocexport.plugin:ExportPlugin'
        ]
    }
)