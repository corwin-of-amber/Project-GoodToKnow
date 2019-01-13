#!/usr/bin/python
# -*- coding: utf-8 -*-
from lxml import etree
from lxml.builder import ElementMaker,E
import xml.etree.ElementTree as ET
import sys
import os
import glob
import urlparse
import urllib
import zipfile
import copy
import shutil
import re
import string

def removeHTMLPrefix(filename, php_name) :
	out_file = open(php_name, 'wb')
	f = open(filename, 'rb')
	for line in f :
		pattern = re.compile('(\s*)xmlns:html="http://www.w3.org/1999/xhtml"(\s*)')
		new_line = pattern.sub('\\1\\2', line)
		pattern = re.compile('(\s*)html:(\s*)')
		new_line = pattern.sub('\\1\\2', new_line)
		out_file.write(str(new_line))
	f.close()
	out_file.close()
	os.remove(filename)

def parseChapters(files) :

	chapters = []
	is_first = True
	found_first = False
	filename = ""
	title = ""
	i = 0
	#length added for empty chapters, headers that are line after line
	length = -1
	chapters_size = 0
	if len(files) <= 2 :
		context = ET.iterparse("../../" + urllib.unquote(files[1]).decode('utf8'), events=('end', ))

		# find class name
		for event, elem in context:
			if "class" in elem.attrib and elem.attrib["class"] == u"כותרת":
				chapters_size = chapters_size + 1
		if chapters_size <= 2 and booklet != "intro_to_logic":
			class_name = u"כותרת-קטנה"
		elif booklet == "intro_to_logic" :
			class_name = u"כותרת _idGenParaOverride-2"
		else :
			class_name = u"כותרת"
		# parsing chapters
		context = ET.iterparse("../../" + urllib.unquote(files[1]).decode('utf8'), events=('end', ))
		for event, elem in context:
			if "class" in elem.attrib and elem.attrib["class"] == class_name :
				found_first = True
				if not is_first and length > 0 :
					removeHTMLPrefix(filename, 'content_' + title + '.php')
				is_first = False
				if length == 0 :
					i = i - 1
				title = "chapter " + str(i)
				filename = format(title + ".xml")
				with open(filename, 'wb') as f:
						if length == 0 :
							elem.text = chapters[len(chapters) - 1] + elem.text
							chapters[len(chapters) - 1] = elem.text
						else :
							chapters.append(elem.text)
						f.write(ET.tostring(elem, encoding="us-ascii", method="html"))
						length = 0
				i = i + 1
			else :
				if found_first and elem.tag == '{http://www.w3.org/1999/xhtml}p':
					length = length + 1
					with open(filename, 'ab') as f:
						f.write(ET.tostring(elem, encoding="us-ascii", method="html"))

		removeHTMLPrefix(filename, 'content_' + title + '.php')

	else :

		remove = []
		for file in files :
			found = False
			is_first = True
			found_first = False
			filename = ""
			title = ""
			i = 0
			context = ET.iterparse("../../" + urllib.unquote(file).decode('utf8'), events=('end', ))
			for event, elem in context:
				if "class" in elem.attrib and elem.attrib["class"] == "Header-copy" :
					found = True
					found_first = True
					if not is_first and length > 0 :
						removeHTMLPrefix(filename, 'content_' + title + '.php')
					is_first = False
					if length == 0 :
						i = i - 1
					title = "chapter " + str(len(chapters))
					filename = format(title + ".xml")
					with open(filename, 'wb') as f:
							if length == 0 :
								elem.text = chapters[len(chapters) - 1] + elem.text
								chapters[len(chapters) - 1] = elem.text
							elif elem.text is None:
								chapters.append(u"פרק " + str(len(chapters) - 1))
							else :
								chapters.append(elem.text)

							f.write(ET.tostring(elem, encoding="us-ascii", method="html"))
							length = 0
					i = i + 1
				else :
					if found_first and elem.tag == '{http://www.w3.org/1999/xhtml}p':
						length = length + 1
						with open(filename, 'ab') as f:
							f.write(ET.tostring(elem, encoding="us-ascii", method="html"))
			if found_first:
				removeHTMLPrefix(filename, 'content_' + title + '.php')

			if not found :
				remove.append(file)

		for f in remove :
			files.remove(f)
	return chapters

def getBooklet(all_booklets) :
	booklet = ""
	for line in all_booklets :
		breaked = re.split('=', line)
		if len(breaked) > 1 :
			pattern = re.compile('booklets\[')
			if 	re.findall(pattern, line) :
				pattern = re.compile('\".*\"')
				for str in re.findall(pattern, line):
					booklet = re.sub('\"', '', str)

	return booklet

def getHebrewName(all_booklets) :
	hebrew_name = ""
	for line in all_booklets :
		breaked = re.split('=', line)
		if len(breaked) > 1 :
			pattern = re.compile('booklet_description\[')
			if 	re.findall(pattern, line) :
				pattern = re.compile('\".*\"')
				for str in re.findall(pattern, line):
					#print str
					hebrew_name = string.replace(str.decode('utf-8'), '"', "")
	return hebrew_name

def getImage(all_booklets) :
	image_name = ""
	for line in all_booklets :
		breaked = re.split('=', line)
		if len(breaked) > 1 :
			pattern = re.compile('images\[')
			if 	re.findall(pattern, line) :
				pattern = re.compile('\".*\"')
				for str in re.findall(pattern, line):
					image_name = re.sub('\"', '', str)
	return image_name


def updateCssFile(booklet) :
	os.chdir("../booklets/" + booklet + "/OEBPS/css/")
	path = "../booklets/" + booklet + "/OEBPS/css/" + glob.glob("*.css")[0].encode('us-ascii')
	os.chdir(starting_dir)
	out_file = open(path + '.tmp', 'wb')
	css_file = open(path, 'rb')
	for line in css_file :
		pattern = re.compile('\\tcolor:#ffffff;')
		new_line = pattern.sub('\\tcolor:#000000;', line)
		out_file.write(str(new_line))
	out_file.close()
	css_file.close()
	os.rename(path, path + '.old')
	shutil.move(path + '.tmp', path)


def copyDirs(src_dir, subdir_names, dest_dir):
	if sys.platform == 'win32':
		src_dir_win = src_dir.replace("/", "\\")
		dest_dir_win = src_dir.replace("/", "\\")

		for d in subdir_names:
			dest_subdir = dest_dir + '/' + d
			if not os.path.isdir(dest_subdir): os.mkdir(dest_subdir)
			cmd = 'xcopy ' + dest_dir_win + '\\' + d + ' ' + dest_dir_win + '\\' + booklet + '\\' + d + '\\' ' /e /s'
			os.system(cmd)

	else:
		for d in subdir_names:
			src_subdir = os.path.join(src_dir, d)
			dest_subdir = os.path.join(dest_dir, d)
			if os.path.isdir(dest_subdir): shutil.rmtree(dest_subdir)
			shutil.copytree(src_subdir, dest_subdir)



starting_dir = os.path.dirname(os.path.abspath(__file__))


if __name__ == "__main__" :
	cwd = os.getcwd()
	os.chdir(starting_dir)

	shutil.copy('all_booklets_list.php', '../index/')
	all_booklets = open('../index/all_booklets_list.php', 'rb')
	booklet = getBooklet(all_booklets)
	all_booklets.close()
	all_booklets = open('../index/all_booklets_list.php', 'rb')
	hebrew_name = getHebrewName(all_booklets)
	all_booklets.close()
	all_booklets = open('../index/all_booklets_list.php', 'rb')
	image_name = getImage(all_booklets)
	all_booklets.close()
	print( "Current directory we are working on: " +
	       os.path.relpath(os.path.join(starting_dir, "../booklets/", booklet), cwd) )

	shutil.copy('../booklets/' + booklet + '/' + image_name, '../index/image/')

	#unzip epub file
	os.chdir("../booklets/" + booklet)
	zip_name = glob.glob(u"*.epub")[0]
	print "Unzipping Ebup file"
	f = open(zip_name, 'rb')
	zip_file = zipfile.ZipFile(f)
	zip_file.extractall()
	os.chdir(starting_dir)

	tree = ET.parse("../booklets/" + booklet + '/OEBPS/content.opf')
	root = tree.getroot()

	print "Parsing content.opf in order to find relevant chapters files"
	#parse chapters name
	chapters = []
	for element in root.iter('{http://www.idpf.org/2007/opf}itemref') :
		if element.attrib.get('idref') != None :
			chapters.append(element.attrib.get('idref'))

	#chapter name --> link
	links = []
	for chapter in chapters:
		for element in root.iter('{http://www.idpf.org/2007/opf}item') :
			if element.attrib.get('id') == chapter :
				#links are paths from the main directory (from project)
				links.append( "booklets/" + booklet + "/OEBPS/" + element.attrib.get('href'))

	out_path = 	'../index/' + booklet
	if not os.path.isdir(out_path):
		os.mkdir(out_path)

	os.chdir(out_path)

	print "Parsing chapters and create php files for each chapter"
	chapters = parseChapters(links)

	os.chdir(starting_dir)

	os.chdir("../booklets/" + booklet)
	pdf_path = "../booklets/" + booklet + "/" + glob.glob("*.pdf")[0].encode('us-ascii')
	pdf_name = glob.glob("*.pdf")[0].encode('us-ascii')
	os.chdir(starting_dir)
	shutil.copy(pdf_path, "../index/" + booklet + "/")

	print "Update php chapters' files"

	shutil.copy('booklet_index.php', '../index/' + booklet + '/')
	chapter_c = open('../index/' + booklet + '/chapters_c.php','ab')
	chapter_c.write("<?php\n$title = \"" + hebrew_name.encode('utf-8') + "\";\n")
	chapter_c.write("$pdf_file = \"" + pdf_name + "\";\n")


	for i in range(len(chapters)) :
		template = open('template_chapter.php', 'rb')
		php_file = open('../index/' + booklet + '/chapter_' + str(i) + '.php','ab')
		for line in template :
			if line.find("replace_name") >= 0:
				php_file.write(line.replace("replace_name", chapters[i].encode('utf8').replace('"', '\\"')))
			elif line.find("replace_num") >= 0:
				php_file.write(line.replace("replace_num", str(i) + ';'))
			elif line.find("replace_total") >= 0:
				php_file.write(line.replace("replace_total", str(len(chapters) - 1) + ';'))
			else :
				php_file.write(line)
		php_file.close()
		chapter_c.write("$chapters[" + str(i) + "] = \"" + chapters[i].encode('utf8').replace('"', '\\"') + "\";\n")
	chapter_c.write("?>")

	updateCssFile(booklet)

	print( "Copy css, font and image for booklet from unzipped Ebub" )

	src_dir = '../booklets/' + booklet + '/OEBPS'
	dest_dir = '../index/' + booklet
	dirs = ["css", "font", "image"]

	copyDirs(src_dir, dirs, dest_dir)

	print( "Delete unzipped files..." )

	shutil.rmtree('../booklets/' + booklet + '/OEBPS')
	shutil.rmtree('../booklets/' + booklet + '/META-INF')
	os.remove("../booklets/" + booklet + "/mimetype")

	print( "The booklet in directory " + booklet + " added to \"Good To Know\" website" )
	print( "  at " + os.path.relpath(os.path.join(starting_dir, "../index/", booklet), cwd) )
