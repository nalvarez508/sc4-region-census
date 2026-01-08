from distutils.core import setup
import py2exe
import sys, os

opts = {
  'py2exe': {
    'compressed': True,
    'optimize': 2,
    'bundle_files': 3,
    'includes': [
      'encodings.*',
      'PIL._imaging', 'PIL._imagingft',
      '_tkinter', 'Tkinter',
      'wx'
    ],
    'excludes': [
      'Tkconstants', 'tcl8.5', 'tcl8.6',
      'matplotlib.tests', 'numpy.random_examples'
    ],
    'dll_excludes': [
      'w9xpopen.exe'
    ]
  }
}

windows_entry = [{'script': 'app.py'}]

setup(
  name='Region Census',
  version='0.8.1',
  description='Region and city information viewer for SimCity 4.',
  options=opts,
  zipfile='library.zip',
  windows=windows_entry
)