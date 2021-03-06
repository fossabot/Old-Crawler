#!/usr/bin/python3

from time import time
import atexit
from os import listdir
from shutil import rmtree
import sys


try:
	import swiftea_bot.private_data as pvdata
except ImportError:
	pass

from index.sftp_swiftea import SFTPSwiftea
from crawling.web_connexion import WebConnexion
from crawling.site_informations import SiteInformations
from database.database_swiftea import DatabaseSwiftea
from swiftea_bot.file_manager import FileManager
from index.inverted_index import InvertedIndex
from swiftea_bot.data import DIR_INDEX
import swiftea_bot.module as module
import index.index as index

class Crawler(object):
	"""Crawler main class."""
	def __init__(self):
		self.infos = list()
		self.sftp_manager = SFTPSwiftea(pvdata.HOST_SSH, pvdata.USER_SSH, pvdata.PASSWORD_SSH)
		self.site_informations = SiteInformations()
		self.file_manager = FileManager()
		stopwords, badwords = self.file_manager.get_lists_words()  # Create dirs if need
		if stopwords == dict() or badwords == dict():
			self.sftp_manager.download_lists_words()  # Download all lists of words (bad and stop)
			stopwords, badwords = self.file_manager.get_lists_words()
		self.site_informations.set_listswords(stopwords, badwords)

		self.index_manager = InvertedIndex()
		self.database = DatabaseSwiftea(pvdata.HOST_DB, pvdata.USER_DB, pvdata.PASSWORD_DB, pvdata.NAME_DB)
		self.web_connexion = WebConnexion()

		self.get_inverted_index()
		self.crawled_websites = 0

	def get_inverted_index(self):
		"""Manage all operations to get inverted-index.

		Check for a save inverted-index file, compare inverted-index in local and
		on server to know if it's necessary to download it.

		"""
		if module.is_index():
			inverted_index = self.file_manager.get_inverted_index()
		else:
			if self.sftp_manager.compare_indexs():
				begining = time()
				inverted_index = self.sftp_manager.get_inverted_index()
				index.stats_dl_index(begining, time())
			else:
				inverted_index = self.file_manager.read_inverted_index()
		self.index_manager.setInvertedIndex(inverted_index)

	def start(self):
		"""Start main loop of crawling.

		Crawl 10 webpages, send documents to database, index them
		and save the configurations (line number in links file, ...).
		Send the inverted-index and check for suggestions each 500 crawled webpages.

		Do it until the user want stop crawling or occured an error.

		"""
		run = True
		while run:
			stats_send_index = time()
			self.suggestions()
			for _ in range(50):
				module.tell('Crawl', severity=2)
				begining = time()
				while len(self.infos) < 10:
					module.tell('File {0}, line {1}'.format(
						str(self.file_manager.reading_file_number),
						str(self.file_manager.reading_line_number+1)), severity=0)
					url = self.file_manager.get_url()  # Get the url of the website
					if url == 'stop':
						self.safe_quit()
					self.crawl_webpage(url)

				# End of crawling loop

				module.tell('{} new documents!'.format(self.crawled_websites), severity=-1)

				self.send_to_db()
				self.indexing()

				module.stats_webpages(begining, time())

				self.infos.clear()  # Reset the list of dict of informations of websites.
				self.file_manager.check_stop_crawling()
				self.file_manager.save_config()
				if self.file_manager.run == 'false':
					module.tell('User wants stop program')
					self.safe_quit()
					run = False
					break

			# End of loop range(n)
			if run:
				self.suggestions()
				self.send_inverted_index()
				self.file_manager.check_size_files()
				module.stats_send_index(stats_send_index, time())

	def crawl_webpage(self, url):
		"""Crawl the given url.

		Get webpage source code, feed it to the parser, manager extracting data,
		manager redirections and can delete some documents to avoid duplicates.

		:param url: url of webpage
		:type url: str

		"""
		module.tell('Crawling ' + url)
		# Get webpage's html code:
		new_url, html_code, nofollow, score, all_urls = self.web_connexion.get_code(url)
		if html_code is None:
			self.delete_if_exists(all_urls)  # Failed to get code, must delete from database.
		elif html_code == 'no connexion':
			sys.exit()
		elif html_code == 'ignore':  # There was something wrong and maybe a redirection.
			self.delete_if_exists(all_urls)
		else:
			module.tell('New url: ' + new_url, severity=0)
			self.delete_if_exists(all_urls)  # Except new url
			webpage_infos, links = self.site_informations.get_infos(new_url, html_code, nofollow, score)
			webpage_infos['url'] = new_url

			if webpage_infos['title'] != '':
				if module.can_add_doc(self.infos, webpage_infos):  # Duplicate only with url
					self.infos.append(webpage_infos)
					self.crawled_websites += 1
					links = self.file_manager.save_links(links)
					self.file_manager.ckeck_size_links(links)
			else:
				self.delete_if_exists(new_url)

	def delete_if_exists(self, urls):
		"""Delete bad doc if exists.

		Check if doc exists in database and delete it from database and inverted-index.

		:param url: url to delete
		:type url: str or list

		"""
		if isinstance(urls, str):
			urls = [urls]
		for url in urls:
			doc_exists = self.database.doc_exists(url)
			if doc_exists:
				doc_id = self.database.get_doc_id(url)
				if doc_id:
					self.database.del_one_doc(url)
					self.index_manager.delete_doc_id(doc_id)
				else:
					self.safe_quit()
			elif doc_exists is None:
				self.safe_quit()
			else:
				module.tell('Ignore: ' + url, severity=-1)

	def send_to_db(self):
		"""Send all informations about crawled webpages to database.

		Can delete some documents to avoid http and https duplicates.

		"""
		module.tell('Send to database', severity=2)
		for webpage_infos in self.infos:
			webpage_infos['url'], url_to_del = self.database.https_duplicate(webpage_infos['url'])
			if url_to_del:
				self.delete_if_exists(url_to_del)
			module.tell('New url (to add): ' + webpage_infos['url'], severity=-1)
			error = self.database.send_doc(webpage_infos)
			if error:
				self.safe_quit()

	def indexing(self):
		"""Index crawled webpages.

		get id of each documents and index them.

		"""
		module.tell('Indexing', severity=2)
		for webpage_infos in self.infos:
			doc_id = self.database.get_doc_id(webpage_infos['url'])
			if doc_id is None:
				self.safe_quit()
			module.tell('Indexing {0} {1}'.format(doc_id, webpage_infos['url']))
			self.index_manager.add_doc(webpage_infos['keywords'], doc_id, webpage_infos['language'])

	def send_inverted_index(self):
		"""Send inverted-index generate by indexing to server."""
		begining = time()
		self.sftp_manager.send_inverted_index(self.index_manager.getInvertedIndex())
		index.stats_ul_index(begining, time())
		for path in listdir(DIR_INDEX):
			rmtree(DIR_INDEX + path)

	def suggestions(self):
		"""Suggestions:

		Get 5 urls from database, delete them, crawl them,
		send all informations about them, index them.

		"""
		suggestions = self.database.suggestions()
		if suggestions is None:
			module.tell('Failed to get suggestions')
		else:
			suggestions = self.site_informations.clean_links(suggestions)
			if len(suggestions) > 0:
				module.tell('Suggestions', severity=2)
				for url in suggestions:
					self.crawl_webpage(url)
				self.send_to_db()
				self.indexing()
				self.infos.clear()  # Reset the list of dict of informations of websites.
			else:
				module.tell('No suggestions')

	def safe_quit(self):
		module.tell('exiting', 0, 2,)


def save(crawler):
	crawler.file_manager.save_inverted_index(crawler.index_manager.getInvertedIndex())

if __name__ == '__main__':
	module.create_dirs()
	module.def_links()
	crawler = Crawler()
	atexit.register(save, crawler)
	crawler.start()
