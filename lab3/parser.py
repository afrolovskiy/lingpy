# coding: utf-8
import mwparserfromhell


class WikiContentParser(object):

	def run(self, text):
		res = mwparserfromhell.parse(text)
		import ipdb; ipdb.set_trace()
		return res
