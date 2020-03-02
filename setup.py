import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='schedule-dnovichkov',
    version='0.0.1',
    author='Dmitriy Novickov',
    author_email='dmitriy.novichkov@gmail.com',
    description='Range-based schedule',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dnovichkov/schedule',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
