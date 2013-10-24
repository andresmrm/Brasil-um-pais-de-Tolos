import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, '..', '..', 'README.md')).read()
CHANGES = open(os.path.join(here, '..', '..', 'CHANGES.txt')).read()

requires = [
    'pyramid==1.5a1',
    'repoze.tm2>=1.0b1', # default_commit_veto
    'sqlalchemy',
    'zope.sqlalchemy',
    'WebError',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    'plim',
    'deform',
    'nose',
    ]


setup(name='pyramidapp',
      version='0.0',
      description='pyramidapp',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires = requires,
      tests_require = requires,
      test_suite="pyramidapp",
      entry_points = """\
      [paste.app_factory]
      main = pyramidapp:main
      """,
  #    [console_scripts]
#      initialize_bpt_db = bpt.scripts.initializedb:main
      paster_plugins=['pyramid'],
      )

