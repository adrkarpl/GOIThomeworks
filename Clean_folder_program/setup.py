from setuptools import setup, find_packages

setup(
    name='Clean_folder_program',
    version='1.00',
    description='Program for sorting files by their type (extensions).',
    url='https://github.com/adrkarpl',
    author='Adrian Karwat',
    author_email='adr.karwat@gmail.com',
    license='MIT',
    packages=find_packages(),
    entry_points={'console_scripts': ['clean-folder = clean_folder.clean:clean_and_organize_folder']}
)