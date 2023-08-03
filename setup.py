
import os
import codecs

from setuptools import setup


def read(*parts):
    return codecs.open(os.path.join(os.path.dirname(__file__), *parts),
                       encoding='utf8').read()

package_data_globs = [
    'templates/conversejs/includes/*.html',
    'static/converse.js/*.js',
    'static/converse.js/*.css',
    'static/converse.js/images/*',
    'static/converse.js/fonticons/*.js',
    'static/converse.js/fonticons/*.css',
    'static/converse.js/fonticons/fonts/*',
]

setup(
    name='django-conversejs',
    description='Adds converse.js (javascript XMPP client) to Django',
    version='0.3.4',
    long_description=read('README.rst'),
    packages=['conversejs',
              'conversejs.migrations',
              'conversejs.templatetags'],
    package_dir={'conversejs': 'conversejs'},
    package_data={'conversejs': package_data_globs},
    author='Sergio Oliveira',
    author_email='sergio@tracy.com.br',
    url='https://github.com/TracyWebTech/django-conversejs',
    license='MPL v2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        ],
    install_requires=[
        'pure-sasl==0.1.5',
        'sleekxmpp==1.3.2',
        'dnspython==1.11.1',
        ],
)
