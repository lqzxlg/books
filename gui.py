# -*- coding: UTF-8 -*-
# [gui] part of books project
# Author : Cngmg，2021, Zhejiang
# Version : 1.0.0
# Env : python3.6, tkinter

import tkinter as tk
import easygui as g
import sys, os, copy
from win32api import GetSystemMetrics

import item, log

Screen_Width, Screen_Height = (GetSystemMetrics(0), GetSystemMetrics(1))
usrWidth, usrHeight = (int(Screen_Width * 0.75), int(Screen_Height * 0.75))
item.initenv()

class NameSpace():
	def __init__(self, windows):
		self.usr = None
		self.pwd = None
		self.usrbooks = None
		self.booksEntry = None
		self.savedata = None
		self.windows = windows

	def new(self):
		self.usr = g.enterbox(msg="请输入您的用户名")
		self.pwd = g.passwordbox(msg="请输入您的密码")
		self.usrbooks = item.booksItem(self.usr, self.pwd)
		hashs = self.usrbooks.get_hash()
		if os.path.exists(item.save_dir + hashs):
			g.msgbox(msg="此用户已经注册！",ok_button="确定")
			self.usr = None
			self.pwd = None
			self.usrbooks = None
			return None
		self.booksEntry = self.usrbooks.get_books()
		self.appendbase()
		self.upgradeBooks()
		self.savedata = copy.deepcopy(self.booksEntry.readall())
		self.booksEntry.writefile()
		
	def open(self):
		self.usr = g.enterbox(msg="请输入您的用户名")
		self.pwd = g.passwordbox(msg="请输入您的密码")
		self.usrbooks = item.booksItem(self.usr, self.pwd)
		hashs = self.usrbooks.get_hash()
		if not os.path.exists(item.save_dir + hashs):
			g.msgbox(msg="此用户不存在！",ok_button="确定")
			self.usr = None
			self.pwd = None
			self.usrbooks = None
			return None
		self.booksEntry = self.usrbooks.get_books()
		self.savedata = copy.deepcopy(self.booksEntry.readall())
		self.upgradeBooks()

	def save(self):
		if self.booksEntry:
			self.booksEntry.writefile()
			self.savedata = copy.deepcopy(self.booksEntry.readall())
		else:
			g.msgbox(msg="无效的登录凭证！",ok_button="确定")

	def exit(self):
		if self.booksEntry:
			if self.savedata != self.booksEntry.readall():
				flag = g.ccbox("文件尚未保存，是否保存？",choices=("是","否"))
				if flag == True:
					self.booksEntry.writefile()
				elif flag == None:
					return None
			self.windows.exit()
		else:
			self.windows.exit()

	def cancellation(self):
		if self.booksEntry:
			if g.ccbox("您保存的数据将会全部全部删除，是否继续？",choices=("是","否")) and g.passwordbox(msg="请再次输入您的密码") == self.pwd:
				hashs = self.usrbooks.get_hash()
				if os.path.exists(item.save_dir + hashs):
					os.remove(item.save_dir + hashs)
					g.msgbox(msg="删除成功！",ok_button="确定")
				self.windows.exit()
		else:
			g.msgbox(msg="无效的登录凭证！",ok_button="确定")

	def append(self):
		if self.booksEntry:
			msg = "请填写条目(+为收入，-为支出)"
			fieldNames = ["收入金额：","备注："]
			fieldValues = []
			while True:
				fieldValues = g.multenterbox(msg,"",fieldNames)
				if fieldValues == None:
					break
				elif fieldValues[0] != "":
					if "+" in fieldValues[0] and not "-" in fieldValues[0]:
						self.booksEntry.appendItem("in",fieldValues[0][1:],fieldValues[1])
					elif "-" in fieldValues[0] and not "+" in fieldValues[0]:
						self.booksEntry.appendItem("out",fieldValues[0][1:],fieldValues[1])
					else:
						g.msgbox(msg="无效的金额输入！",ok_button="确定")
						continue
					break
				g.msgbox(msg="金额项目为必填项！",ok_button="确定")
			self.upgradeBooks()
		else:
			g.msgbox(msg="无效的登录凭证！",ok_button="确定")

	def change(self):
		if self.booksEntry:
			msg = "请填写条目(+为收入，-为支出)"
			fieldNames = ["序号：", "收入金额：","备注："]
			fieldValues = []
			while True:
				fieldValues = g.multenterbox(msg,"",fieldNames)
				if fieldValues == None:
					break
				try:
					int(fieldValues[0])
				except:
					g.msgbox(msg="无效的序号！",ok_button="确定")
					continue
				if fieldValues[1] != "":
					if "+" in fieldValues[1] and not "-" in fieldValues[1]:
						self.booksEntry.changeItem(int(fieldValues[0]),"in",fieldValues[1][1:],fieldValues[2])
					elif "-" in fieldValues[1] and not "+" in fieldValues[1]:
						self.booksEntry.changeItem(int(fieldValues[0]),"out",fieldValues[1][1:],fieldValues[2])
					else:
						g.msgbox(msg="无效的金额输入！",ok_button="确定")
						continue
					break
				g.msgbox(msg="金额项目为必填项！",ok_button="确定")
			self.upgradeBooks()
		else:
			g.msgbox(msg="无效的登录凭证！",ok_button="确定")

	def appendbase(self):
		msg = "请填写条目"
		fieldNames = ["结算金额：","备注："]
		fieldValues = []
		while True:
			fieldValues = g.multenterbox(msg,"",fieldNames)
			if fieldValues == None:
				break
			elif fieldValues[0] != "" and "+" not in fieldValues[0] and "-" not in fieldValues[0]:
				self.booksEntry.appendItem("base",fieldValues[0],fieldValues[1])
				break
			else:
				g.msgbox(msg="无效的金额输入！",ok_button="确定")
		self.upgradeBooks()

	def upgradeBooks(self):
		#print(self.booksEntry.readall())
		for i in range(self.booksEntry.getItemNumber()+1):
			self.windows.lb1.delete(i)
			self.windows.lb2.delete(i)
			self.windows.lb3.delete(i)
			self.windows.lb4.delete(i)
			self.windows.lb5.delete(i)
		for i in range(self.booksEntry.getItemNumber()):
			self.windows.lb1.insert("end",self.booksEntry.getid(i))
			self.windows.lb2.insert("end",self.booksEntry.readItem(i,"type"))
			self.windows.lb3.insert("end",self.booksEntry.readItem(i,"value"))
			self.windows.lb4.insert("end",self.booksEntry.readItem(i,"time"))
			if len(self.booksEntry.readItem(i,"log")) == 0 :
				self.windows.lb5.insert("end", "无备注")
			else:
				self.windows.lb5.insert("end", self.booksEntry.readItem(i,"log"))
		self.windows.et.delete(0,"end")
		tmp = 0.00
		for i in range(self.booksEntry.getItemNumber()):
			if self.booksEntry.readItem(i,"type") == "in":
				tmp += float(self.booksEntry.readItem(i,"value"))
			elif self.booksEntry.readItem(i,"type") == "out":
				tmp -= float(self.booksEntry.readItem(i,"value"))
			else:
				tmp += float(self.booksEntry.readItem(i,"value"))
		self.windows.et.insert("end",str(tmp))

	def delindex(self):
		if self.booksEntry:
			r = g.integerbox(msg="请输入删除条目的序号",lowerbound=0,upperbound=self.booksEntry.getItemNumber()-1)
			if r : self.booksEntry.delItem(r)
			for i in range(r, self.booksEntry.getItemNumber()):
				self.booksEntry.changeItem(i,self.booksEntry.readItem(i,"type"),self.booksEntry.readItem(i,"value"),self.booksEntry.readItem(i,"log"))
			self.upgradeBooks()
		else:
			g.msgbox(msg="无效的登录凭证！",ok_button="确定")

	def clear(self):
		if self.booksEntry:
			self.booksEntry.clearbooks()
			self.upgradeBooks()
		else:
			g.msgbox(msg="无效的登录凭证！",ok_button="确定")

	def logprint_help(self):
		roots = tk.Tk()
		roots.title("About")
		if os.path.exists("main.tex"):
			roots.iconbitmap('main.tex')
		roots.geometry("%dx%d+%d+%d"%(Screen_Width*6//10,Screen_Height*6//10,(Screen_Width-Screen_Width*6//10)//2,(Screen_Height-Screen_Height*6//10)//2))
		t = tk.Text(
			roots,
			font=("Calibri", 20)
			)
		t.insert('end', "\n" + log.helps)
		t.place(
			relheight=1,
			relwidth=1,
			relx=0,
			rely=0
			)
		roots.mainloop()

	def logprint_about(self):
		roots = tk.Tk()
		roots.title("About")
		if os.path.exists("main.tex"):
			roots.iconbitmap('main.tex')
		roots.geometry("%dx%d+%d+%d"%(Screen_Width*6//10,Screen_Height*6//10,(Screen_Width-Screen_Width*6//10)//2,(Screen_Height-Screen_Height*6//10)//2))
		t = tk.Text(
			roots,
			font=("Calibri", 20)
			)
		t.insert('end', "\n" + log.Author + "\n\n" + log.Version)
		t.place(
			relheight=1,
			relwidth=1,
			relx=0,
			rely=0
			)
		roots.mainloop()

	def logprint_gnu(self):
		roots = tk.Tk()
		roots.title("Licence")
		if os.path.exists("main.tex"):
			roots.iconbitmap('main.tex')
		roots.geometry("%dx%d+%d+%d"%(Screen_Width*6//10,Screen_Height*6//10,(Screen_Width-Screen_Width*6//10)//2,(Screen_Height-Screen_Height*6//10)//2))
		t = tk.Text(
			roots,
			font=("Calibri", 20)
			)
		t.insert('end', log.gnu)
		t.place(
			relheight=1,
			relwidth=1,
			relx=0,
			rely=0
			)
		roots.mainloop()

class Windows():
	def __init__(self):
		self.root = None

	def init(self, ns):
		self.ns = ns
		# 创建窗口
		self.root = tk.Tk()
		self.root.title("Private Books")
		self.root.geometry("%dx%d+%d+%d"%(usrWidth,usrHeight,(Screen_Width-usrWidth)//2,(Screen_Height-usrHeight)//2))
		if os.path.exists("main.tex"):
			self.root.iconbitmap('main.tex')
		# self.root.protocol('WM_DELETE_WINDOW', self.ns.exit)
		# 建立菜单栏
		self.menubar = tk.Menu(self.root)
		# 建立下拉文件菜单
		self.filemenu = tk.Menu(self.menubar, tearoff=0)
		self.menubar.add_cascade(label="文件", menu=self.filemenu)
		self.filemenu.add_command(label="新建", command=self.ns.new)
		self.filemenu.add_command(label="打开", command=self.ns.open)
		self.filemenu.add_command(label="保存", command=self.ns.save)
		self.filemenu.add_command(label="注销用户", command=self.ns.cancellation)
		self.filemenu.add_separator()
		self.filemenu.add_command(label="退出", command=self.ns.exit)

		self.menubar.add_separator()
		# 建立下拉编辑菜单
		self.editmenu = tk.Menu(self.menubar, tearoff=0)
		self.menubar.add_cascade(label="编辑", menu=self.editmenu)
		self.editmenu.add_command(label="添加条目", command=self.ns.append)
		self.editmenu.add_command(label="编辑条目", command=self.ns.change)
		self.editmenu.add_command(label="删除条目", command=self.ns.delindex)
		self.editmenu.add_command(label="删除全部", command=self.ns.clear)

		self.menubar.add_separator()
		# 建立下拉关于菜单
		self.aboutmenu = tk.Menu(self.menubar, tearoff=0)
		self.menubar.add_cascade(label="关于", menu=self.aboutmenu)
		self.aboutmenu.add_command(label="关于", command=self.ns.logprint_about)
		self.aboutmenu.add_separator()
		self.aboutmenu.add_command(label="帮助", command=self.ns.logprint_help)
		self.aboutmenu.add_separator()
		self.aboutmenu.add_command(label="协议", command=self.ns.logprint_gnu)

		self.menubar.add_separator()
		self.menubar.add_command(label="强制退出", command=sys.exit)

		# 显示菜单栏
		self.root.config(menu=self.menubar)

		# 创建列表
		self.lb1 = tk.Listbox(self.root, font=("Calibri", 20))
		#self.lb1.insert(0,"0")
		self.lb2 = tk.Listbox(self.root, font=("Calibri", 20))
		#self.lb2.insert(0,"base")
		self.lb3 = tk.Listbox(self.root, font=("Calibri", 20))
		#self.lb3.insert(0,"100.00")
		self.lb4 = tk.Listbox(self.root, font=("Calibri", 20))
		#self.lb4.insert(0,"time")
		self.lb5 = tk.Listbox(self.root, font=("Calibri", 20))
		#self.lb5.insert(0,"Hello World")

		# 显示列表
		self.lb1.place(relx=0,rely=0,relwidth=0.06,relheight=0.9)
		self.lb2.place(relx=0.06,rely=0,relwidth=0.06,relheight=0.9)
		self.lb3.place(relx=0.12,rely=0,relwidth=0.24,relheight=0.9)
		self.lb4.place(relx=0.36,rely=0,relwidth=0.32,relheight=0.9)
		self.lb5.place(relx=0.68,rely=0,relwidth=0.32,relheight=0.9)

		self.lb = tk.Label(
			self.root,
			font=("Calibri", 20),
			text="结余："
			)
		self.lb.place(relx=0.02,rely=0.925,relwidth=0.1,relheight=0.05)

		self.et = tk.Entry(
			self.root,
			font=("Calibri", 20)
			)
		#self.et.insert("end", "Unknown")
		self.et.place(relx=0.12,rely=0.925,relwidth=0.2,relheight=0.05)

	def loop(self):
		# 开启主循环
		if self.root:
			self.root.mainloop()

	def exit(self):
		self.root.quit()

def main():
	windows = Windows()
	ns = NameSpace(windows)
	windows.init(ns)
	windows.loop()
	