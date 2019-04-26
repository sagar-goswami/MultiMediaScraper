import tkinter as tk
import requests
import os
import speech_recognition as sr
from tkinter import *
from bs4 import BeautifulSoup
from tkinter.scrolledtext import ScrolledText


pp = ''

def scrape_function():
	if search_term != '':
		search_term_keywords = search_term.get()
	
	url = "https://www.google.co.in/search?q=" + 'wikipedia+' + search_term_keywords ##generating search url

	google_search = requests.get(url)	##fetching url
	soup_google_search = BeautifulSoup(google_search.text,"lxml") 	##parsing response using lxml parser
	links = []	##array for links

	for item in soup_google_search.select(".r a"):
		links.append(item.get('href')) 	##array for google link results

	first_google_result_url = links[0]	##storing first link 
	if first_google_result_url[:31] == '/url?q=https://en.wikipedia.org': 
		first_google_result_url = first_google_result_url[7:]
		exact_first_url = first_google_result_url.partition('&')[0]	##generating exact link
		wiki_page = requests.get(exact_first_url) ##fetching wikipage for the search query
		soup_wiki_page = BeautifulSoup(wiki_page.text, "lxml") 	##parsing
			
		print(soup_wiki_page.title.text[:-12])	##printing title 
		
		for paragraph in soup_wiki_page.find_all('p'):	##printing all p elements
			global  pp
			pp = pp + paragraph.text
			print(pp)

		file = open("testfile.txt","w") 
		file.write(pp)
		file.close()
		os.rename('testfile.txt',soup_wiki_page.title.text[:-12] + '.txt') 
		print("File Saved Successfully")

		exit()
		
		text = Text(height = "1500", width = "1500") 
		text.pack()
		text.insert(END, pp)
		mainloop()

screen = Tk()
screen.geometry("600x200")
screen.title("Text Scraper")

heading = Label(text = "Simple Text Scraper", bg = "black", fg = "white", height = "3", width = "700", font='hack 15 bold')
heading.pack()

search_term_text = Label(text = "Search term*", font='hack 10 bold')
search_term_text.place(x = 20, y = 100)

search_term = StringVar()

search_term_entry = Entry(textvariable = search_term)
search_term_entry.place(x = 135, y = 100, width = '300')

button_submit = Button(text = "Scrape", width = '10', command = scrape_function, fg = 'white', bg = 'black')
button_submit.place(x = 450, y = 95)

# button_save_as_text = Button(text = "Save as text", width = '10', fg = 'white', bg = 'black', command = save_as_text)
# button_save_as_text.place(x = 30, y = 130)

screen.mainloop()
