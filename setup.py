from setuptools import setup


setup(name='voluum',
      version='0.1',
      description='Python Client for Voluum API',
      author='Ronnie Beltran',
      author_email='rbbeltran.09@gmail.com',
      url='https://github.com/ronbeltran/voluum',
      packages=['voluum'],
      include_package_data=True,
      install_requires=[
          'requests>=2.0',
          'pytz>=2016.10',
      ])
