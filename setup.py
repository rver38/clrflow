from distutils.core import setup
setup(
  name = 'clrflow',
  packages = ['clrflow'],
  version = '1.0',
  license='MIT',
  description = 'An improved color module like colorama with additional features and tools.',
  author = 'rver',                   
  author_email = 'rverflow@gmail.com',      
  url = 'https://github.com/rver38/clrflow/',   
  download_url = 'https://github.com/rver38/clrflow/archive/refs/tags/v_1.tar.gz',    
  keywords = ['color', 'gradient', 'text','strings','formatting','ansi'],   
  install_requires=[],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.10'
  ],
)
