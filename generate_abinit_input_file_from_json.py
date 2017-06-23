#!/usr/bin/env python
# -*- coding=UTF-8 -*-
"""
Parses an json file of input settings for Abinit, and outputs an Abinit input file to stdout.

This input format is indicated by the .abinit.json format.

The format supported is as follows:

{
	"direct": // an array of attributes to put directly into Abinit
	[
		<attributes>
	],

	"meta": // an array of attributes describing the input, that may be used to create input but are not input directly
	[
		<attributes>
	]
}

Each attribute has the following format:

{
	"name": <string>,
	"value": <input value>,
	"comment": <string, optional>
}

Additional properties are ignored.

Input values may be the following types:

literal (string or number): placed as-is
array of literals: placed in-line, separated by 2 spaces
matrix of literals: placed on each line after the label,
    indented with values separated by 2 spaces

This file ignores all "meta" attributes and naively places all "direct" attributes,
with comments for each input preceding each input.
"""

__version__ = "0.0.0"

__author__ = "JJ Brown"
__copyright__ = "Copyright 2017, JJ Brown"
__credits__ = ["JJ Brown"]
__license__ = "MIT"
__maintainer__ = "JJ Brown"
__status__ = "development"

import json
import handle_command_line_IO

LABEL_WIDTH = 8

class SimpleAttribute:
	def __init__(self, name, value, comment=None):
		self.name = name
		self.value = value
		self.comment = comment

	def __str__(self):
		"""Represent this attribute in Abinit"""
		if(self.comment is None):
			formatted_comment_lines = []
		else:
			formatted_comment_lines = ["#"+x for x in self.comment.splitlines()]

		if(type(self.value) is list and len(self.value) > 0):
			if(type(self.value[0]) is list): #then the value is a matrix
				input_lines = [self.name] + [' '*LABEL_WIDTH+"  ".join([unicode(xy) for xy in x]) for x in self.value]
			else: #then the value is a 1-D array
				input_lines = [self.name.ljust(LABEL_WIDTH) + "  ".join([unicode(x) for x in self.value])]
		else:
			input_lines = [self.name.ljust(LABEL_WIDTH) + unicode(self.value)]

		return "\n".join(formatted_comment_lines+input_lines)

	def __repr__(self):
		"""Represent this attribute as JSON"""
		return self.__dict__.__repr__()

class SimpleAttributeJSONDecoder(json.JSONDecoder):
	def __init__(self, *args, **kwargs):
		json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

	def object_hook(self, element):
		"""
		Parse the name, value, and optional comment inside an attribute,
		and return it as a SimpleAttribute.

		Assumes all element properties are unicode u'strings'.
		"""
		handle_command_line_IO.errprint(element)
		if('comment' in element or 'name' in element or 'value' in element): #if it's a Simple Attribute
			if(u'comment' in element): 
				return SimpleAttribute(name=(element[u'name'] or element['name']), value=element[u'value'], comment=element[u'comment'])
			else:
				return SimpleAttribute(name=element[u'name'], value=element[u'value'])
		else: #some other element
			return element

def display_help_message():
	"""Prints a help message with usage instructions to stderr"""
	handle_command_line_IO.errprint("Usage: python generate_abinit_input_file_from_json.py [filename.abinit.json] > outputfile.in")

input_file,_ = handle_command_line_IO.get_input_file(display_help_message) # get from stdin or first argument's file
input_data = json.load(input_file, cls=SimpleAttributeJSONDecoder)
print("\n\n".join([attribute.__str__() for attribute in input_data[u'direct']])) # send to stdout for redirection