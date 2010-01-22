from distutils.core import setup
import os
from glob import glob

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way. Taken from Django's install script.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

def search_for_packages():
	"""
	Walk through the source directory and get the list of Snappy packages.
	"""
	packages = []
	root_dir = os.path.dirname(__file__)
	if root_dir != '':
		os.chdir(root_dir)
	snappy_dir = 'snappy'

	for dirpath, dirnames, filenames in os.walk(snappy_dir):
		# Ignore dirnames that start with '.'
		for i, dirname in enumerate(dirnames):
			if dirname.startswith('.'): del dirnames[i]
		if '__init__.py' in filenames:
			packages.append('.'.join(fullsplit(dirpath)))
	return packages

packages = search_for_packages()
data = {
	'name': 'snappy',
	'fullname': 'Snappy Screen Capture',
	'version': '0.1b',
	'author': 'Donald Harvey',
	'author_email': 'donald@donaldharvey.co.uk',
	'description': 'A quick, customisable and easy-to-use screen capture app for Linux.',
	'url': 'http://launchpad.net/snappy-screen-capture',
	'packages': packages,
	'scripts': ['bin/snappy'],
	'data_files': [
		('share/applications', ['resources/snappy.desktop']),
		('share/pixmaps', ['resources/snappy.png']),
		('share/icons/hicolor/16x16/apps', ['resources/16/snappy.png']),
		('share/icons/hicolor/24x24/apps', ['resources/24/snappy.png']),
		('share/icons/hicolor/48x48/apps', ['resources/snappy.png']),
		('share/icons/hicolor/32x32/apps', ['resources/32/snappy.png']),
		('share/icons/hicolor/64x64/apps', ['resources/64/snappy.png']),
		('share/icons/hicolor/scalable/apps', ['resources/snappy.svg']),
		('share/snappy/pixmaps', glob('resources/*.png')),
		('share/snappy', ['resources/finished.wav', 'resources/uploaded.svg']),
		('share/snappy/glade/preferences', glob('resources/glade/preferences/*.glade')),
		('share/snappy/glade/preferences/sharing', glob('resources/glade/preferences/sharing/*.glade')),
	],
}
if __name__ == '__main__':
	setup(**data)
