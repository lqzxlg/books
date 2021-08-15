# -*- coding: UTF-8 -*-
# [aes class] part of books project
# Author : Cngmg，2021, Zhejiang
# Version : 1.0.0
# Env : pycryptodome

from Crypto.Cipher import AES
import os
from Crypto import Random
 
class AESTool():
	
	def __init__(self):
		# print(self)
		pass
	
	def __str__(self):
		return "这是一个AES操作工具"
		
	def isbytes(args):
		# 判断是否是bytes类型
		if type(args) == type(b"0"):
			return True
		else:
			return False

	def CreatKey(keychain):
		# 创建符合要求的密钥
		if not AESTool.isbytes(keychain):
			keychain = str(keychain).encode("utf-8")
		if len(keychain) < 16:
			while len(keychain) < 16:
				keychain += keychain[::-1]
			keychain = keychain[:16]
		elif len(keychain) < 24:
			while len(keychain) < 24:
				keychain += keychain[::-1]
			keychain = keychain[:24]
		elif len(keychain) < 32:
			while len(keychain) < 32:
				keychain += keychain[::-1]
			keychain = keychain[:32]
		else:
			keychain = keychain[:32]
		return keychain

	def Encryption(raw, key):
		# 加密
		if not AESTool.isbytes(raw):
			raw = str(raw).encode("utf-8")
		key = AESTool.CreatKey(key)
		iv = Random.new().read(AES.block_size)
		cipher = AES.new(key, AES.MODE_CFB, iv)
		data = iv + cipher.encrypt(raw)
		return data # 返回类型bytes

	def Decryption(data, key):
		# 解密
		key = AESTool.CreatKey(key)
		iv = data[:16]
		cipher = AES.new(key, AES.MODE_CFB, iv)
		return cipher.decrypt(data[16:]) # 返回类型bytes
