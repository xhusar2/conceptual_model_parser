from setuptools import setup, find_packages

setup(
    name='exquiro',
    version='0.2.0',
    keywords='github repositories sieve projects community',
    description='Tool for parsing XMI files and searching in conceptual models from those files.',
    #long_description=long_description,
    author='Richard Husar',
    author_email='husarric@fit.cvut.cz',
    license='MIT',
    url='https://github.com/xhusar2/exquiro',
    zip_safe=False,
    packages=find_packages(),
    package_data={
        'exquiro': [
        ]
    },
    entry_points={
    },
    install_requires=[
        'requests',
        'lxml',
        'neomodel'
    ],
    setup_requires=[
        'pytest-runner',
        'requests',
        'neomodel'
    ],
    tests_require=[
        'betamax',
        'pytest'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Communications',
        'Topic :: Internet',
        'Topic :: Software Development',
        'Topic :: Software Development :: Version Control',
    ],
)
