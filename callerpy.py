#!/usr/bin/env python

# CallerPy V 2.0 - Truecaller Name Retriever
# Copyright (C) <2013>  mad_dev(A'mmer Almadani)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the <organization> nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Report any issues with this script to <mad_dev@linuxmail.org>


import mechanize
from bs4 import BeautifulSoup
import re
import datetime
import argparse


#####CREDS_twitter#####
user = ''
pwd = ''

class CallerPy():

	def authenticate(self):
		url = 'http://www.truecaller.com/authenticate/'
		return url

	def twitter(self, user, pwd):
		
		param = 'twitter'
		url = self.authenticate()
		B.open(url+param)
		B.form = list(B.forms())[0]
		B['session[username_or_email]'] = user
		B['session[password]'] = pwd
		return B.submit()

	#def googlePlus():

	#def facebook():
	

	def truecaller(self, country, number):
		B.form = list(B.forms())
		B.follow_link(nr=1)
		q = B.open('http://www.truecaller.com/search/%s/%s' %(country, number))
		a = q.read()
		bs = BeautifulSoup(a)
		if '<h2 id="profile-name">' in a:
			for name in bs.find_all('h2',{"id":"profile-name"}):
				nm = re.split(r'<.*?>', str(name))
				for i in nm:
					print i
			self.save(nm[1], country, number)


	def save(self, name, country, number):
		template = '''
			<entry>
				<name>%s</name>
				<number>%s</number>
				<country>%s</country>
			</entry>
		''' %(name, number, country)
		xml = open('log.xml', 'a')
		xml.write(template)
		xml.close()

	def country_by_code(self, code):
		a = open('countries', 'r')
		b = a.read()
		p = re.findall('[a-z]{1,}', b)
		o = re.findall('[0-9]{1,}', b)
		for i, e in zip(p, o):
			if str(code) in e:
				return i

if __name__ == '__main__':
	par = argparse.ArgumentParser(prog=__file__, formatter_class=argparse.ArgumentDefaultsHelpFormatter, 
		epilog="Do not forget to hardcode your credentials", description='TrueCaller Name Retriever')
	par.add_argument('-n', '--number', required=True, help="Phone Number Without Country Code", metavar='number')
	par.add_argument('-c', '--country',required=False,  help="Country | String", metavar='country')
	par.add_argument('-cc', '--countrycode',required=False,  help="Country | Int", metavar='country code', type=int)
	par.add_argument('-l', '--login', required=True, default='twitter', help="Login Method | twitter, g+, fb", metavar='login')

	argvs = par.parse_args()

	current_date = datetime.datetime.now()
	
	B = mechanize.Browser()
	B.set_handle_robots(False)
	x = CallerPy()
	
	'''TODO:Define function to handle arguments'''
	if argvs.country is None:
		if argvs.login == 'twitter':
			print 'Using Twitter'
			try:
				if '54' in str(argvs.countrycode):
					country = 'argentina-buenosaires'
					x.twitter(user, pwd), x.truecaller(country, argvs.number)
				if '245' in str(argvs.countrycode):
					country = 'guinea-bissau'
					x.twitter(user, pwd), x.truecaller(country, argvs.number)
				if '91' in str(argvs.countrycode):
					country = 'india-other'
					x.twitter(user, pwd), x.truecaller(country, argvs.number)
				else:
					x.twitter(user, pwd), x.truecaller(x.country_by_code(argvs.countrycode), argvs.number)
			except:
				print 'Could Not Find a Name for %s' %argvs.number
				
		else:
			print 'This version only supports twitter'
	if argvs.countrycode is None:
		if argvs.login == 'twitter':
			print 'Using Twitter'
			x.twitter(user, pwd), x.truecaller(argvs.country, argvs.number)
		else:
			print 'This version only supports twitter'


