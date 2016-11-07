from setuptools import setup

setup(
    name = "Paved",
    version = "0.5.1",
    url = "https://github.com/eykd/paved",
    download_url = "http://pypi.python.org/pypi/Paved/",
    author = "David Eyk",
    author_email = "eykd@eykd.net",
    license = 'BSD',

    description = 'Common tasks for Paver-based projects.',
    long_description = open('README.rst').read(),

    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Topic :: System :: Software Distribution',
        'Topic :: Utilities',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        ],

    packages=['paved'],
    install_requires = ['Paver'],
    include_package_data = True,
    zip_safe = False,
)
