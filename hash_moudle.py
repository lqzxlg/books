# -*- coding: UTF-8 -*-
# [Hash Calculation] part of books project
# Author : Cngmg，2021, Zhejiang
# Version : 1.0.0

import hashlib

class hash_Tool():
	def __init__(self, raw):
		pass

	def __str__(self):
		return "This is Hash Calculation Class."

	def CalcMD5(raw):
		md5obj = hashlib.md5()
		md5obj.update(raw)
		hash = md5obj.hexdigest()
		return hash

	def CalcSHA1(raw):
		sha1obj = hashlib.sha1()
		sha1obj.update(raw)
		hash = sha1obj.hexdigest()
		return hash

	def CalcSHA256(raw):
		sha256obj = hashlib.sha256()
		sha256obj.update(raw)
		hash = sha256obj.hexdigest()
		return hash

	def CalcSHA512(raw):
		sha512obj = hashlib.sha512()
		sha512obj.update(raw)
		hash = sha512obj.hexdigest()
		return hash