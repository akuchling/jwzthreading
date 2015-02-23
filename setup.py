
from distutils import core

kw = {
    'name': 'jwzthreading',
    'version': '0.92',
    'description': 'Algorithm for threading mail messages.',
    'long_description' : '''Contains an implementation of an algorithm for threading mail
messages, as described at http://www.jwz.org/doc/threading.html.''',
    'author': "A.M. Kuchling",
    'author_email': "amk@amk.ca",
    'url': "http://www.amk.ca/python/code/jwz.html",
    'py_modules': ['jwzthreading'],
    'classifiers': [
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 3',
            'Topic :: Software Development :: Libraries',
            'Topic :: Communications :: Email',
    ]
}

core.setup(**kw)
