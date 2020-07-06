from setuptools import setup, find_packages

with open('requirements.txt') as fp:
    install_requires = [f for f in fp.readlines() if not f.startswith("-") and not f.startswith("#")]

setup(
    name='crypto_com',
    packages=find_packages(),
    version='0.1',
    description='Crypto.com websocket api client',
    author='Álvaro García Gómez',
    author_email='maxpowel@gmail.com',
    url='https://github.com/maxpowel/crypto_com_client',
    download_url='https://github.com/maxpowel/crypto_com_clientarchive/master.zip',
    classifiers=['Topic :: Adaptive Technologies', 'Topic :: Software Development', 'Topic :: System', 'Topic :: Utilities'],
    install_requires=install_requires,
    keywords=['websocket', 'client', 'crypto']
)
