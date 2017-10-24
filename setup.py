from setuptools import setup

setup(
    name='cr-py',
    version='1.1.4',
    description='A Python API wrapper for cr-api',
    long_description='A Python API wrapper for cr-api',
    url='https://github.com/kwugfighter/cr.py',
    author='kwugfighter',
    author_email='isaacli430@gmail.com',
    license='MIT',
    keywords=['cr', 'Clash Royale', 'CR API'],
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    packages=['cr_py'],
    install_requires=['requests']
)