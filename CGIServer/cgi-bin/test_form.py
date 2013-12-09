#!/usr/bin/env python
import cgi

form = cgi.FieldStorage()
name = form.getfirst('name', 'empty')

print "Content-type: text/html"
print
print "<title>Test CGI</title>"
print "<p>Hello    "
print name
print "     World!</p>"
