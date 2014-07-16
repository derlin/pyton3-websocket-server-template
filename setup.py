from setuptools import setup, find_packages

setup(
    name = 'ws server template',
    version = '1.0',
    description = 'simple example of a cherrypy server using ws4py websockets',

    author = 'Lucy Linder',
    author_email='lucy.derlin@gmail.com',

    package_dir = {'': 'src/python'},
    packages = [ 'utils', 'wsocket' ],

    install_requires = [
        'requests',
        'cherrypy',
        'ws4py',
        'cherrypy-wsgiserver'
    ],

    url = '',
    license = '',
)
