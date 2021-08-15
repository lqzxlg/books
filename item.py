# -*- coding: UTF-8 -*-
# [item] part of books project
# Author : Cngmg，2021, Zhejiang
# Version : 1.0.0
# Env : python3.6

from aes import AESTool as AT
from hash_moudle import hash_Tool as HT
import json, os, random, time

save_dir = "archive\\"

class WithEntry():
	def __init__(self, jsonfile, hashid, pwd):
		if len(jsonfile) == 0:
			self.jsonfile = []
		else:
			self.jsonfile = json.loads(jsonfile)
		self.hashid = hashid
		self.pwd = pwd
		
	def getendid(self):
		index = len(self.jsonfile)
		return index

	def getid(self, index):
		return self.jsonfile[index]["id"]

	def writefile(self):
		data = json.dumps(self.jsonfile)
		open(save_dir + self.hashid, "wb").write(AT.Encryption(data, self.pwd))

	def readItem(self, index, item):
		return self.jsonfile[index]["data"][item]

	def appendItem(self, types, value, log):
		self.jsonfile.append(
			{
				"id":self.getendid(),
				"data":{
					"type":types,
					"time":str(time.asctime(time.localtime(time.time()))),
					"value":str(float(value)),
					"log":log
					}
				}
			)

	def changeItem(self, index, types, value, log):
		self.jsonfile[index] = {
				"id":index,
				"data":{
					"type":types,
					"time":str(time.asctime(time.localtime(time.time()))),
					"value":str(value),
					"log":log
					}
				}

	def delItem(self, index):
		del self.jsonfile[index]

	def readall(self):
		return self.jsonfile

	def readline(self, index):
		return self.jsonfile[index]

	def clearbooks(self):
		self.jsonfile.clear()

	def getItemNumber(self):
		return len(self.jsonfile)

class booksItem():
	def __init__(self, usr, pwd):
		self.usr = usr
		self.pwd = pwd
		tmpstr = "usr:%s|pwd:%s"%(usr, pwd)
		self.hashid = HT.CalcSHA1(tmpstr.encode("utf-8"))
		
	def get_books(self):
		if not os.path.exists(save_dir + self.hashid):
			open(save_dir + self.hashid, 'wb')
			byte = b""
		else:
			byte = AT.Decryption(open(save_dir + self.hashid, 'rb').read(), self.pwd)
		return WithEntry(byte, self.hashid, self.pwd)

	def get_hash(self):
		return self.hashid

def initenv():
	if not os.path.exists("archive"):
		os.mkdir("archive")
	return None

def sample():
	initenv()
	usrbooks = booksItem("name","password")
	usrhash = usrbooks.get_hash()
	booksEntry = usrbooks.get_books()
	# type:in 收入 out 支出 base 基础
	booksEntry.appendItem("in",100,"Unknown")
	booksEntry.appendItem("out",100,"Unknown")
	#booksEntry.clearbooks()
	booksEntry.writefile()
	#print(booksEntry.getItemNumber())
	print(booksEntry.readall())

if __name__ == '__main__':
	sample()
