from setuptools import setup, find_packages

setup(
    name='django-model-explorer',
    version='0.0.1',
    description='Extensions to the Django admin interface for presenting aggregate and statistical model information.',
    long_description=open('README.rst').read(),
    # Get more strings from http://www.python.org/pypi?:action=list_classifiers
    author='Roger Barnes`',
    author_email='roger@mindsocket.com.au',
    url='https://github.com/mindsocket/django-model-explorer',
    download_url='https://github.com/mindsocket/django-model-explorer/downloads',
    license='BSD',
    packages=find_packages(exclude=('tests', 'example')),
    tests_require=[
        'django>=1.3,<1.5',
    ],
#    test_suite='runtests.runtests',
#    include_package_data=True,
#    zip_safe=False,  # because we're including media that Django needs
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
