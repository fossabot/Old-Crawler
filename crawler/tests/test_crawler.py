#!/usr/bin/python3

from package.module import *
from package.searches import SiteInformations
from package.inverted_index import InvertedIndex

class TestCrawlerBase(object):
    """Base class for all crawler test classes."""
    def setup_method(self, _):
        """Configure the app."""
        self.url = 'http://www.example.fr'
        self.language = 'fr'
        self.STOPWORDS = {'fr':('mot', 'pour')}
        self.inverted_index = {'t': "'train'{1:2}"}
        self.alphabet = ALPHABET

class TestCrawlerBasic(TestCrawlerBase):
    def test_clean_text(self):
        text = ('Sample text with non-desired \r whitespaces \t chars \n')
        text = clean_text(text)
        assert not '\n' in text and not '\r' in text and not '\t' in text

    def test_get_base_url(self):
        assert get_base_url(self.url + '/page1.php') == self.url

    def test_clean_links(self):
        links = ['page.php', 'http://www.example.fr/', 'mailto:test@test.fr']
        links = SiteInformations.clean_links(self, links)

        assert links == ['http://www.example.fr/page.php', 'http://www.example.fr']

    def test_clean_keywords(self):
        keywords = ['le', 'mot', '2015', 'bureau', 'word\'s', 'l\'example', 'l’oiseau']
        keywords = SiteInformations.clean_keywords(self, keywords)
        assert keywords == ['bureau', 'word', 'example', 'oiseau']

    def test_remove_duplicates(self):
        assert remove_duplicates(['mot', 'mot']) == ['mot']

    def test_detect_language(self):
        keywords = 'un texte d\'exemple pour tester la fonction'.split()
        language = SiteInformations.detect_language(self, keywords)
        assert language == 'fr'

    def test_clean_favicon(self):
        favicon = '/icon.ico'
        favicon = SiteInformations.clean_favicon(self, favicon)
        assert favicon == 'http://www.example.fr/icon.ico'

    def test_append_doc(self):
        inverted_index = InvertedIndex.append_doc(self, ['voiture', 'mot', 'tobogan'], '2')
        assert inverted_index == {'m': "'mot'{2:1}", 'v': "'voiture'{2:1}", 't': "'train'{1:2}'tobogan'{2:1}"}

        inverted_index = InvertedIndex.append_doc(self, ['voiture', 'mot', 'mot', 'mot', 'chanteur', 'avion'], '3')
        assert inverted_index == {'a': "'avion'{3:1}", 'c': "'chanteur'{3:1}", 'm': "'mot'{2:1,3:3}", 'v': "'voiture'{2:1,3:1}"}

        inverted_index = InvertedIndex.append_doc(self, ['avion', 'avion'], '3')
        assert inverted_index == {'a': "'avion'{3:2}"}

        inverted_index = InvertedIndex.append_doc(self, ['avion', 'avion'], '20')
        assert inverted_index == {'a': "'avion'{3:2,20:2}"}

        inverted_index = InvertedIndex.append_doc(self, ['avion', 'avion', 'avion', 'avion', 'avion', 'avion', 'avion', 'avion', 'avion', 'avion', 'avion', 'avion', 'avion', 'avion'], '455')
        assert inverted_index == {'a': "'avion'{3:2,20:2,455:14}"}

        