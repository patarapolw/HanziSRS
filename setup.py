from setuptools import setup, find_packages
import sys, os

PROJECT_NAME = 'HanziSRS'
mainscript = '{}/anki_connect.py'.format(PROJECT_NAME)
setup_requires = ['PyQt5', 'google_speech', 'bs4']

if sys.platform == 'darwin':
    setup_requires.append('py2app')
    extra_options = dict(
        app=[mainscript],
        options=dict(py2app=dict(
            argv_emulation=True,
            plist=dict(
                CFBundleName='Hanzi SRS',
            )
        )),
    )
elif sys.platform == 'win32':
    setup_requires.append('py2exe')
    extra_options = dict(
        app=[mainscript],
    )
else:
    extra_options = dict(
        scripts=[mainscript],
    )

setup(
    name=PROJECT_NAME,
    version='0.1.0',
    packages=find_packages(),
    data_files=[
        ('{}/database'.format(PROJECT_NAME),
         [os.path.join('{}/database'.format(PROJECT_NAME), item)
          for item in os.listdir('{}/database'.format(PROJECT_NAME))]),
        ('{}/qml'.format(PROJECT_NAME),
         [os.path.join('{}/qml'.format(PROJECT_NAME), item)
          for item in os.listdir('{}/qml'.format(PROJECT_NAME)) if os.path.splitext(item)[1] == '.qml'])
    ],
    setup_requires=setup_requires,
    install_requires=setup_requires,
    entry_points={
        'gui_scripts': [
            '{0} = {0}.__main__:main'.format(PROJECT_NAME)
        ]
    },
    **extra_options
)
