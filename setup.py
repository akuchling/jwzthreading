
__revision__ = '$Id: setup.py,v 1.2 2003/03/26 17:34:48 akuchling Exp $'

from distutils import core 

kw = {
    'name' : 'jwzthreading',
    'version' : '0.91',
    'description' : 'Algorithm for threading mail messages.',
    'long_description' : '''Contains an implementation of an algorithm for threading mail
messages, as described at http://www.jwz.org/doc/threading.html.''',
    'author' : "A.M. Kuchling",
    'author_email' : "amk@amk.ca",
    'url' : "http://www.amk.ca/python/code/jwzthreading.html",
    'py_modules' : ['jwzthreading'],
    }

# If we're running Python 2.3, add extra information
if hasattr(core, 'setup_keywords'):
    if 'classifiers' in core.setup_keywords:
        kw['classifiers'] = [
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
	    'License :: OSI Approved :: BSD License',
            'Topic :: Software Development :: Libraries',
	    'Topic :: Communications :: Email',
            ]
    if 'download_url' in core.setup_keywords:
        kw['download_url'] = ('http://www.amk.ca/files/python/%s-%s.tar.gz' %
                              (kw['name'], kw['version']))
        
core.setup(**kw)


