from setuptools import setup

setup(
    name = 'komachi',
    version = '0.0.1',
    description = 'Scraper for Hatsugen Komachi',
    author = 'Tetsuya Shioda',
    author_email = 'ysk501sw@gmail.com',
    url = 'https://github.com/jubatus/hackason.git',
    install_requires = ['beautifulsoup4', 'lxml'],
    packages = ['komachi']
)
