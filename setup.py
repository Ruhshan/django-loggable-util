from setuptools import setup

with open("README.md", "r") as fh:
  long_description = fh.read()

setup(
  name='django_loggable_util',
  packages=['django_loggable_util'],
  version='0.0.3',
  license='MIT',
  description='Separate logging from class based view business code',
  author='Ruhshan Ahmed Abir',
  author_email='ruhshan.ahmed@gmail.com',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='https://github.com/Ruhshan/django-loggable-util',
  keywords=['Django', 'Loggable', 'Wrapper','Generic view','Class based view'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Django :: Utility',
    'License :: OSI Approved :: MIT License',
    'Framework :: Django',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)