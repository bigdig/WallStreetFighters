# -*- coding: utf-8 -*-
__author__ = "Xai"
__date__ = "$2012-03-02 19:32:01$"

import numpy as np
import re
import csv
import datetime
import urllib2
import cStringIO
import cPickle
import threading

'''一个简单的SINA数据客户端，主要使用requests开发'''
import requests
import execjs

#ZMIENNE GLOBALNE
REMEMBER_COUNT = 15

DATABASE_LAST_UPDATE = datetime.date(2012,3,3)
INDEX_LIST = []
STOCK_LIST = []
FOREX_LIST = []
RESOURCE_LIST = []
BOND_LIST = []
FUTURES_LIST = []
HISTORY_LIST = []
AMEX_HIST = []
NYSE_HIST = []
NASDAQ_HIST = []
UPDATE_FLAG = False


class FinancialObject (object):
	"""A class defining a financial object (index, company, raw material, bond, etc.) that stores historical quotes and possibly the indexes. """

	def __init__ (self, name, abbreviation, financialType, dataSource, detail = None, lastUpdate = datetime.date (1971,1,1)):
		self.name = name
		self.abbreviation = abbreviation
		self.financialType = financialType
		#self.dataSource = dataSource
		self.dataSource = "Yahoo"
		self.detail = detail # detailed information -> index - country / index - index
		self.lastUpdate = lastUpdate #information when last updated data from archive.
		self.currentValue = [] #para value and date of download
		self.previousValues = [] #list in values ​​from same day but previously retrieved form: [datetime, value]
		self.valuesDaily = [] #list for yahoo characters [[date, open, high, low, close, volume, adj close], [date, ...]
		# for Stooq without adj close.
		self.valuesWeekly = [] # as above only for weekly data
		self.valuesMonthly = [] # as above only for monthly data
		self.dailyUpdate = datetime.date (1971,1,1)
		self.monthlyUpdate = datetime.date (1971,1,1)
		self.weeklyUpdate = datetime.date (1971,1,1)

	def updateArchive(self, timePeriod):
		"""Method of updating data of an existing object. Creates a new temporary object and copies its contents to a 'self' object. """
		day = datetime.timedelta(days=1)
		lastUpdate = self.lastUpdate + day		

		global UPDATE_FLAG
		try:
		
			if self.dataSource == "Yahoo":
				if timePeriod == 'daily' and self.dailyUpdate != datetime.date.today():
					UPDATE_FLAG = True
					self.dailyUpdate = datetime.date.today()
					if self.valuesDaily == []: 
						tmpObj = createWithArchivesFromYahoo(self.name, self.abbreviation, self.financialType, self.detail, timePeriod)	
					elif self.valuesDaily[0][0] == datetime.date.today():
						return
					else:
						date = self.valuesDaily[0][0]+day
						tmpObj = createWithArchivesFromYahoo(self.name, self.abbreviation, self.financialType, self.detail, timePeriod, date)		
					self.valuesDaily = self.valuesDaily + tmpObj.valuesDaily
					self.dailyUpdate = tmpObj.dailyUpdate
				elif timePeriod == 'weekly' and self.weeklyUpdate != datetime.date.today():
					UPDATE_FLAG = True
					self.weeklyUpdate = datetime.date.today()	
					if self.valuesWeekly == []: 
						tmpObj = createWithArchivesFromYahoo(self.name, self.abbreviation, self.financialType, self.detail, timePeriod)	
					elif self.valuesWeekly[0][0] == datetime.date.today():
						return
					else:
						date = self.valuesWeekly[0][0]+day
						tmpObj = createWithArchivesFromYahoo(self.name, self.abbreviation, self.financialType, self.detail, timePeriod, date)		
					self.valuesWeekly = self.valuesWeekly + tmpObj.valuesWeekly
					self.weeklyUpdate = tmpObj.weeklyUpdate
				elif timePeriod == 'monthly' and self.monthlyUpdate != datetime.date.today():
					UPDATE_FLAG = True
					self.monthlyUpdate = datetime.date.today()
					if self.valuesMonthly == []: 
						tmpObj = createWithArchivesFromYahoo(self.name, self.abbreviation, self.financialType, self.detail, timePeriod)	
					elif self.valuesMonthly[0][0] == datetime.date.today():
						return
					else:
						date = self.valuesMonthly[0][0]+day
						tmpObj = createWithArchivesFromYahoo(self.name, self.abbreviation, self.financialType, self.detail, timePeriod, date)		
					self.valuesMonthly= self.valuesMonthly + tmpObj.valuesMonthly
					self.monthlyUpdate = tmpObj.monthlyUpdate
		except DataAPIException:
			UPDATE_FLAG = True
			return

	def getArray(self, time):
		"""Funkcja zwracająca rekordowaną tablicę (numpy.recarray) dla informacji w odstępie czasu przekazanym jako parametr funkcji. Pozwala to dostać się do poszczególnych tablic używając odpowiednich rekordów: 'date' 'open' etc."""
		if self.financialType == 'forex' or self.financialType == 'bond' or self.financialType == 'resource' or self.financialType == 'future':
			tmplist = []
			if time == 'daily':
				for x in self.valuesDaily:
					tmplist.append((str(x[0]),x[1],x[2],x[3],x[4],0))
			if time == 'weekly':
				for x in self.valuesWeekly:
					tmplist.append((str(x[0]),x[1],x[2],x[3],x[4],0))
			if time == 'monthly':
				for x in self.valuesMonthly:
					tmplist.append((str(x[0]),x[1],x[2],x[3],x[4],0))
			return np.array(tmplist,dtype = [('date','S10'),('open',float),('high',float),('low',float),('close',float),('volume',float)])
		else:
			tmplist = []
			if time == 'daily':
				for x in self.valuesDaily:
					tmplist.append((str(x[0]),x[1],x[2],x[3],x[4],x[5]))
			if time == 'weekly':
				for x in self.valuesWeekly:
					tmplist.append((str(x[0]),x[1],x[2],x[3],x[4],x[5]))
			if time == 'monthly':
				for x in self.valuesMonthly:
					tmplist.append((str(x[0]),x[1],x[2],x[3],x[4],x[5]))
			return np.array(tmplist,dtype = [('date','S10'),('open',float),('high',float),('low',float),('close',float),('volume',float)])
			
	def getIndex(self, begin, end, time = 'daily'):
		"""Funkcja zwracająca indeksy tablicy dla danego przedziału czasu"""
		if begin > end:
			return
		if time == 'daily':
			if end < self.valuesDaily[0][0]:
				raise DataAPIException('Stock was not noted yet ')
			size = len(self.valuesDaily)
			
			if begin < self.valuesDaily[0][0]:
				start = 1
			else:
				start = 0
				while (begin > self.valuesDaily[start][0]):
					start += 1
			
			if end > self.valuesDaily[size-1][0]:
				finish = size-2
			else:
				finish = start
				while (end > self.valuesDaily[finish][0]):
					finish += 1
			return [start-1,finish+1]
		if time == 'weekly':
			size = len(self.valuesWeekly)
			if end < self.valuesWeekly[0][0]:
				raise DataAPIException('Stock was not noted yet ')
			if begin < self.valuesWeekly[0][0]:
				start = 1
			else:
				start = 0
				while (begin > self.valuesWeekly[start][0]):
					start += 1
		
			if end > self.valuesWeekly[size-1][0]:
				finish = size-2
			else:
				finish = start
				while (end > self.valuesWeekly[finish][0]):
					finish += 1
			return [start-1,finish+1]
		if time == 'monthly':
			size = len(self.valuesMonthly)
			if end < self.valuesMonthly[0][0]:
				raise DataAPIException('Stock was not noted yet ')
			if begin < self.valuesMonthly[0][0]:
				start = 1
			else:
				start = 0
				while (begin > self.valuesMonthly[start][0]):
					start += 1
			
			if end > self.valuesMonthly[size-1][0]:
				finish = size-2
			else:
				finish = start
				while (end > self.valuesMonthly[finish][0]):
					finish += 1
			return [start-1,finish+1]
#koniec definicji klasy

class DataAPIException(Exception):
	def __init__(self,value):
		self.value = value
	def __str__(self):
		return repr(self.value)


def getDayBarsFromSina(name, abbreviation, financialType, detail, timePeriod, sinceDate = datetime.date(1971,1,1)):
	"""# 从sina加载最新的Day数据"""
	global HISTORY_LIST
	global UPDATE_FLAG
	if UPDATE_FLAG == False:
		print isInHistory(abbreviation)
		finObj = isInHistory(abbreviation)
		if finObj != None:
			finObj.updateArchive(timePeriod)
			return finObj

	currentDate = datetime.date.today()

	finObj = FinancialObject(name,abbreviation, financialType, "Yahoo", detail, currentDate)
	print "Pobieram: " + abbreviation

	requests.adapters.DEFAULT_RETRIES = 5
	session = requests.session()
	session.keep_alive = False

	try:

		symbol = "rb1801"
		url = u'http://stock.finance.sina.com.cn/futures/api/json.php/InnerFuturesService.getInnerFuturesDailyKLine?symbol={0}'.format(symbol)
		
		print(u'从sina下载{0}的日K数据 {1}'.format(symbol, url))

		responses = execjs.eval(session.get(url).content.decode('gbk'))
		dayVolume = 0

		finObj.dailyUpdate = datetime.date.today()

		for row in responses:
			dataRow = [[parserStringToDate(row["date"]),float(row["open"]),float(row["high"]),float(row["low"]),float(row["close"]),int(row["volume"])]]
			finObj.valuesDaily = finObj.valuesDaily + dataRow

		if len(finObj.valuesDaily)>0:
    			print(u'从sina读取了{0}条日线K数据'.format(len(finObj.valuesDaily)))
		else:
			print(u'从sina读取日线K数据失败')

	except Exception as e:
		print(u'加载Sina历史日线数据失败：'+str(e))

	if UPDATE_FLAG == False:
    		if len(HISTORY_LIST) == REMEMBER_COUNT:
			HISTORY_LIST[1:REMEMBER_COUNT:1]=HISTORY_LIST[0:REMEMBER_COUNT-1:1]
			HISTORY_LIST[0] = finObj
		else:
			HISTORY_LIST += [finObj]
	UPDATE_FLAG = False	
	return finObj 
	

def createWithArchivesFromStooq(name, abbreviation, financialType, detail, timePeriod, sinceDate = datetime.date(1971,1,1)):
    return getDayBarsFromSina(name,abbreviation, financialType, detail, timePeriod)

def createWithArchivesFromYahoo(name, abbreviation, financialType, detail, timePeriod, sinceDate = datetime.date(1971,1,1)):
	"""Funkcja tworząca obiekt zawierający archiwalne dane pobrane ze strony finance.yahoo dotyczące obiektu zdefiniowanego w parametrach funkcji"""
	return getDayBarsFromSina(name,abbreviation, financialType, detail, timePeriod)
	global HISTORY_LIST
	global UPDATE_FLAG
	if UPDATE_FLAG == False:
		print isInHistory(abbreviation)
		finObj = isInHistory(abbreviation)
		if finObj != None:
			finObj.updateArchive(timePeriod)
			return finObj

	currentDate = datetime.date.today()

	finObj = FinancialObject(name,abbreviation, financialType, "Yahoo", detail, currentDate)
	print "Pobieram: " + abbreviation
	url = 'http://ichart.finance.yahoo.com/table.csv?s='+abbreviation+'&a='+str(sinceDate.month-1)+'&b='+str(sinceDate.day)	 
        url = url+'&c='+str(sinceDate.year)+'&d='+str(currentDate.month-1)+'&e='
	url = url+str(currentDate.day)+'&f='+str(currentDate.year)+'&g=d&ignore=.csv'
	if timePeriod == 'weekly':
		url = url.replace('&g=d', '&g=w')
	elif timePeriod == 'monthly':
		url = url.replace('&g=d', '&g=m')
	try:
		site = urllib2.urlopen(url)
	except urllib2.URLError, ex:
		print url
		print "Something wrong happend! Check your internet connection!"
		raise DataAPIException('Connection Error!')
	csvString = site.read()
	csvString = cStringIO.StringIO(csvString)
	dataCsv = csv.reader(csvString)
	dataCsv.next()

	if timePeriod == 'daily':
		finObj.dailyUpdate = datetime.date.today()
		for row in dataCsv:
			dataRow = [[parserStringToDate(row[0]),float(row[1]),float(row[2]),float(row[3]),float(row[4]),int(row[5])]]
			finObj.valuesDaily = dataRow + finObj.valuesDaily
	elif timePeriod == 'weekly':
		finObj.weeklyUpdate = datetime.date.today()	
		for row in dataCsv:
			dataRow = [[parserStringToDate(row[0]),float(row[1]),float(row[2]),float(row[3]),float(row[4]),int(row[5])]]
			finObj.valuesWeekly = dataRow + finObj.valuesWeekly 
	elif timePeriod == 'monthly':
		finObj.monthlyUpdate = datetime.date.today()
		for row in dataCsv:
			dataRow = [[parserStringToDate(row[0]),float(row[1]),float(row[2]),float(row[3]),float(row[4]),int(row[5])]]
			finObj.valuesMonthly = dataRow + finObj.valuesMonthly
	if UPDATE_FLAG == False:
		if len(HISTORY_LIST) == REMEMBER_COUNT:
			HISTORY_LIST[1:REMEMBER_COUNT:1]=HISTORY_LIST[0:REMEMBER_COUNT-1:1]
			HISTORY_LIST[0] = finObj
		else:
			HISTORY_LIST += [finObj]
	UPDATE_FLAG = False	
	return finObj 

		 
def parserStringToDate(string):
	"""Funkcja zmieniająca ciąg znaków postaci "YYYY-MM-DD" na obiekt klasy datatime.date"""
	string = string.split('-')
	x = datetime.date(int(string[0]),int(string[1]),int(string[2]))
	return x

def parserDateToString(date):
	"""Funkcja zmieniająca obiekt datetime.date na string postaci YYYYMMDD"""
	date = str(date)
	date = date.replace('-','')
	return date

def updateDatabase():
	"""Funkcja sprawdzająca czy na rynkach pojawiły się nowe spółki, jeśli tak to dodaje spółki do bazy danych. """
	global DATABASE_LAST_UPDATE	
	current = datetime.datetime.today()
	csvFile  = open('data2.wsf', "ab")
	dmonth = datetime.timedelta(days=30)
	while(DATABASE_LAST_UPDATE.month <= current.month and DATABASE_LAST_UPDATE.month <= current.year):

		smonth = DATABASE_LAST_UPDATE.ctime()[4:7:1]
		syear = DATABASE_LAST_UPDATE.year%100
		url = "http://biz.yahoo.com/ipo/prc_"+smonth.lower()+str(syear)+".html"
		try:
			site = urllib2.urlopen(url)
		except urllib2.URLError, ex:
			print "Something wrong happend! Check your internet connection!"
			raise DataAPIException('Connection Error!')
		pageSource = site.read()
		pattern = '(?s)Prev(.*)Prev'
		pattern = re.compile(pattern)
		m = re.search(pattern,pageSource)
		pageSource = m.group(0)

		pattern = '>([0-9][0-9]*-[A-Z][a-z][a-z]-[0-9][0-9])</td><td>(.*)</td><td.*>([A-Z][A-Z][A-Z]*)<.*>M<'
		for m in re.finditer(pattern,pageSource):
			if isInStock(m.group(3)) == None:
				print m.group(3)+m.group(2)+m.group(1)
				csvFile.write(m.group(3)+','+m.group(2)+',Yahoo,NYSE\n')
		DATABASE_LAST_UPDATE = DATABASE_LAST_UPDATE + dmonth
			

def loadData():
	"""Funkcja wczytująca dane z 'bazy danych' na temat dostępnych do wyszukania obiektów finansowych i zapisuje je do zmiennych globalnych""" 
	global INDEX_LIST
	global STOCK_LIST
	global FOREX_LIST
	global RESOURCE_LIST
	global BOND_LIST
	global FUTURES_LIST
	global DATABASE_LAST_UPDATE
	global HISTORY_LIST
	global AMEX_HIST
	global NASDAQ_HIST
	global NYSE_HIST
	csvFile  = open('data1.wsf', "rb")
	dataCsv = csv.reader(csvFile)
	dataCsv.next()
	for row in dataCsv:
		INDEX_LIST = INDEX_LIST + [[row[0],row[1],row[2],'America']]
	csvFile  = open('data2.wsf', "rb")
	dataCsv = csv.reader(csvFile)
	flag = True
	for row in dataCsv:
		if flag == True:
			DATABASE_LAST_UPDATE = parserStringToDate(row[1])
			flag = False
		else:	
			STOCK_LIST.append([row[0],row[1],row[2],row[3]])
	
	csvFile  = open('data3.wsf', "rb")
	dataCsv = csv.reader(csvFile)
	dataCsv.next()
	for row in dataCsv:
		FOREX_LIST = FOREX_LIST + [[row[0],row[1],row[2],row[3]]]
	csvFile  = open('data4.wsf', "rb")
	dataCsv = csv.reader(csvFile)
	dataCsv.next()
	for row in dataCsv:
		RESOURCE_LIST = RESOURCE_LIST + [[row[0],row[1],row[2],row[3]]]
	csvFile  = open('data5.wsf', "rb")
	dataCsv = csv.reader(csvFile)
	dataCsv.next()
	for row in dataCsv:
		BOND_LIST = BOND_LIST + [[row[0],row[1],row[2],row[3]]]	
	csvFile  = open('data6.wsf', "rb")
	dataCsv = csv.reader(csvFile)
	dataCsv.next()
	for row in dataCsv:
		FUTURES_LIST = FUTURES_LIST + [[row[0],row[1],row[2],row[3]]]	
	csvFile  = open('AMEX.csv', "rb")
	dataCsv = csv.reader(csvFile)
	for row in dataCsv:
		AMEX_HIST += [[parserStringToDate(row[0][0:4:1]+'-'+row[0][4:6:1]+'-'+row[0][6:8:1]),row[1],row[2],row[3],row[4],row[5],row[6]]]
	csvFile  = open('NASDAQ.csv', "rb")
	dataCsv = csv.reader(csvFile)
	for row in dataCsv:
		NASDAQ_HIST += [[parserStringToDate(row[0][0:4:1]+'-'+row[0][4:6:1]+'-'+row[0][6:8:1]),row[1],row[2],row[3],row[4],row[5],row[6]]]
	csvFile  = open('NYSE.csv', "rb")
	dataCsv = csv.reader(csvFile)
	print(dataCsv)
	for row in dataCsv:
		print(row.__dict__)
		NYSE_HIST += [[parserStringToDate(row[0][0:4:1]+'-'+row[0][4:6:1]+'-'+row[0][6:8:1]),row[1],row[2],row[3],row[4],row[5],row[6]]]
	#loadHistory()


def isInHistory(abbreviation):
	"""Funkcja sprawdzająca czy obiekt finansowy o podanym skrócie znajduje się w historii"""
	for x in HISTORY_LIST:
		if x.abbreviation == abbreviation:
			return x	
	return None

def isInStock(abbreviation):
	"""Funkcja sprawdzająca czy obiekt finansowy o podanym skrócie znajduje się w historii"""
	for x in STOCK_LIST:
		if x[0] == abbreviation and x[2] == 'Yahoo':
			return x	
	return None

def saveHistory(file):
	"""Funkcja zapisująca bierzącą historie w pliku"""
	global HISTORY_LIST
	print "zapisalem"
	for x in HISTORY_LIST:
		print x.abbreviation
	cPickle.dump(HISTORY_LIST, file)

class loadHistory(threading.Thread):
	"""Funkcja zapisująca bierzącą historie w pliku"""
    	def __init__(self, File):
        	threading.Thread.__init__(self)
		self.file = File

	def run(self):
		global HISTORY_LIST
		HISTORY_LIST = cPickle.load(self.file)
		self.file.close()

def top5Volume():
	"""Funkcja zwracajaca listę 5 spółek o najwyższym wolumenie"""
	TOP_VOLUME = []
	return TOP_VOLUME

def top5Gainers():
	"""Funkcja zwracajaca listę 5 spółek o najwiekszym wzroscie"""
	TOP_GAINERS = []
	return TOP_GAINERS

def top5Losers():
	"""Funkcja zwracajaca listę 5 spółek o najwiekszym spadku"""
	TOP_LOSERS = []
	return TOP_LOSERS

def getMostPopular():
	"""Funkcja zwracająca aktualne wartości najbardziej popularnych obiektów"""
	mostPopular = []
	return mostPopular


def getDataToLightWeightChart(abbreviation, financialType, source):
	global UPDATE_FLAG
	today = datetime.date.today()
	ddays = datetime.timedelta(days=30)
	since = today - ddays
	UPDATE_FLAG = True
	finObj = createWithArchivesFromYahoo("", abbreviation, financialType, "", "daily", since)
	UPDATE_FLAG = False
	return finObj
	




########################################################################################################

