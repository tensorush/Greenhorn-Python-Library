from setuptools import setup


setup(
    name='greenhorn',
    version='0.0.1',
    license='MIT License',
    author='Georgy Trush',
    author_email='tensorush@gmail.com',
    description='Python library meant for personal studies of Python basics',
    long_description=open('./README.md', 'r').read(),
    long_description_content_type='text/markdown',
    packages=['greenhorn'],
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
    ],
)
