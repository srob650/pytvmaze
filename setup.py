from setuptools import setup, find_packages

setup(
    name = 'pytvmaze',
    version = '2.0.4',
    description = 'Python interface to the TV Maze API (www.tvmaze.com)',
    url = 'https://github.com/srob650/pytvmaze',
    author = 'Spencer Roberts',
    author_email = 'pytvmaze@gmail.com',
    license='MIT',

    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5'
    ],

    keywords = 'python tv television tvmaze',
    packages=['pytvmaze'],
    install_requires=['requests']

)
