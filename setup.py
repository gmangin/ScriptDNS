from setuptools import setup

setup(name='dnsScript',
      version='0.0.0',
      description='Dns script',
      author='Gaelle MANGIN',
      maintainer='Gaelle MANGIN',
      url='https://http://monwiki.tk/doku.php?id=projets:rush:rush10',
      packages=['dnsScript'],
      license='MIT License',
      package_data={'': ['LICENSE', 'README.md']},
      classifiers=[
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.2',
          'Topic :: Internet',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: System :: Networking'],
                    zip_safe=True)
