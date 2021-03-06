#!/usr/bin/python3

"""Define several functions for DatabaseSwiftea."""

def url_is_secure(url):
	"""Check if given url is secure (https).

	:param url: url to check
	:type url: str
	:return: True if url is secure

	"""
	if url.startswith('https'):
		return True
	else:
		return False

def convert_secure(url):
	"""Convert https to http and http to https.

	:param url: url to convert
	:type url: str
	:return: converted url

	"""
	if url_is_secure(url):
		return url[:4] + url [5:]
	else:
		return url[:4] + 's' + url [4:]
