"""
Create multiple IGV session files using items in a Dataset Collection.
"""

import bioblend.galaxy
import requests
from six.moves import urllib

from BeautifulSoup import BeautifulSoup

class GiInteractor(object):
    """Interacts with Galaxy to ultimately retrieve URLs required to build a session."""

    def __init__(self, galaxy_url, api_key, hids, hdcas):
        self.gi = bioblend.galaxy.GalaxyInstance(galaxy_url, api_key)
        self.hids = hids
        self.hdcas = hdcas

    @property
    def collection_elements(self):
        for hid, hdca in zip(self.hids, self.hdcas):
            collection = self.gi.histories.show_dataset_collection(dataset_collection_id=hdca, history_id=hid)
            yield hid, collection['name'], collection['elements']

    @property
    def display_application_links(self):
        for hid, collection_name, elements in self.collection_elements:
            for element in elements:
                element_identifier = element['element_identifier']
                hda_id = element['object']['id']
                dataset_details = self.gi.histories.show_dataset(dataset_id=hda_id, history_id=hid)
                for display_app in dataset_details['display_apps']:
                    if display_app['label'] == 'display with IGV':
                        for link in display_app['links']:
                            yield collection_name, element_identifier, urllib.parse.urljoin(self.gi.url, link['href'])

    @property
    def igv_links(self):
        for (collection_name, element_identifier, display_link) in self.display_application_links:
            display_name = "%s: %s" % (collection_name, element_identifier)
            display_html = requests.get(display_link, params={'displayname': display_name}).history[0].text
            display_html = urllib.parse.unquote_plus(display_html)
            link = self.parse_links(display_html).split('load?file=')[1]
            yield link

    @staticmethod
    def parse_links(gx_response):
        """Return link embedded in galaxy response for display_application url get request."""
        soup = BeautifulSoup(gx_response)
        for link in soup.findAll('a'):
            if link:
                return link.get('href')

