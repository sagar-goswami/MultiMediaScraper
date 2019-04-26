import re
import os
import json
import urllib
import os.path
import requests
import http.cookiejar
import urllib.request
import speech_recognition as sr
from os import path
from pytube import YouTube
from bs4 import BeautifulSoup


def wiki_scrape(search_item):
	os.chdir(current_dir)
	url = "https://www.google.co.in/search?q=" + 'wikipedia+' + search_item ##generating search url

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
		print('\nScraping Started\n')
		
		if not os.path.exists('Text'):
			os.mkdir('Text')
			os.chdir('Text')
		if os.path.exists('Text'):
			os.chdir('Text')

		print('Title: ' + soup_wiki_page.title.text[:-12])	##printing title 
		
		pp = ''
		imgs = []

		for paragraph in soup_wiki_page.find_all('p'):	##printing all p elements
				pp = pp + paragraph.text

		print('\nSummary: ' + pp)
		
		if not os.path.exists(soup_wiki_page.title.text[:-12]):
			os.mkdir(soup_wiki_page.title.text[:-12])
			os.chdir(soup_wiki_page.title.text[:-12])
		if os.path.exists(soup_wiki_page.title.text[:-12]):
			os.chdir(soup_wiki_page.title.text[:-12])

		file = open(soup_wiki_page.title.text[:-12] + '.txt',"w") 
		file.write(pp)
		file.close()
		print("Text file saved Successfully\n")
	else:
		print("An error occured")

def gimage_scrape(query):
	def get_soup(url,header):
	    return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url,headers=header)),'html.parser')

	error_count = 0

	image_type="ActiOn"
	query = query.split()
	query = '+'.join(query)
	url = "https://www.google.co.in/search?q="+ query +"&source=lnms&tbm=isch"
	#add the directory for your image here
	DIR="Image"
	header={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"}
	soup = get_soup(url,header)


	ActualImages=[]# contains the link for Large original images, type of  image
	for a in soup.find_all("div",{"class":"rg_meta"}):
	    link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
	    ActualImages.append((link,Type))

	print("Currently downloading" ,len(ActualImages),"Images")
	print("\nTo skip at any time press `ctrl + Z`\n")

	if not os.path.exists(DIR):
	            os.mkdir(DIR)
	
	DIR = os.path.join(DIR, query.split()[0])

	if not os.path.exists(DIR):
	            os.mkdir(DIR)
	###print images
	for i , (img , Type) in enumerate( ActualImages):
	    try:
	        req = urllib.request.Request(img, headers={'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"})
	        raw_img = urllib.request.urlopen(req).read()   

	        cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
	        print('Saving image no. ' + str(cntr))
	        if len(Type)==0:
	            f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+".jpg"), 'wb')
	        else :
	            f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+"."+Type), 'wb')


	        f.write(raw_img)
	        f.close()
	    except Exception as e:
	        print("Error downloading a image")
	        error_count = error_count + 1
	        continue

	print("Unable to download " + str(error_count) +  " Images")


def a_scrape(query):
	base = "https://www.youtube.com/results?search_query="
	qstring = query
	r = requests.get(base+qstring)

	page = r.text
	soup=BeautifulSoup(page,'html.parser')

	vids = soup.findAll('a',{'class':'yt-uix-tile-link'})

	audio_list = []
	for v in vids:
		tmp = 'https://www.youtube.com' + v['href']
		audio_list.append(tmp)

	download_option = input("\nEnter 1 to bulk download, 2 to selectively download: ")
	download_option = int(download_option)
	if download_option == 1:
		print("\nBulk download mode active")
		count=0
		aud_quality = input("Select audio quality:\n0 - 160kbps\n1 - 128kbps\n2 - 70kbps\n3 - 50kbps\nEnter:")
		aud_quality = int(aud_quality)
		print("\nDownloading Audio")
		print("\nTo skip at any time press `ctrl + Z`\n")
		os.chdir(current_dir)
		if not os.path.exists('Audio'):
			os.mkdir('Audio')
			os.chdir('Audio')
			if not os.path.isdir(qstring):
				os.mkdir(qstring)
				os.chdir(qstring)
			else:
				os.chdir(qstring)
		if os.path.exists('Audio'):
			os.chdir('Audio')
			if not os.path.isdir(qstring):
				os.mkdir(qstring)
				os.chdir(qstring)
			else:
				os.chdir(qstring)
		for item in audio_list:
			count+=1
			yt = YouTube(item)
			print("Audio. no " + str(count))
			if aud_quality == 0:
				for res in yt.streams.filter(only_audio=True).filter(abr='160kbps').all():
					print(res)
					res.download()
			if aud_quality == 1:
				for res in yt.streams.filter(only_audio=True).filter(abr='128kbps').all():
					print(res)
					res.download()
			if aud_quality == 2:
				for res in yt.streams.filter(only_audio=True).filter(abr='70kbps').all():
					print(res)
					res.download()
			if aud_quality == 3:
				for res in yt.streams.filter(only_audio=True).filter(abr='50kbps').all():
					print(res)
					res.download()

		print("Download Finished")
	elif download_option == 2:
		print("\nSelective download mode active")
		count=0
		print("\nDownloading Audio Information")
		print("\nTo skip at any time press `ctrl + Z`\n")
		for item in audio_list:
			count+=1
			yt = YouTube(item)
			print("\nShowing audio " + str(count) + " details:\n")
			os.chdir(current_dir)
			if not os.path.exists('Audio'):
				os.mkdir('Audio')
				os.chdir('Audio')
				if not os.path.isdir(qstring):
					os.mkdir(qstring)
					os.chdir(qstring)
				else:
					os.chdir(qstring)
			if os.path.exists('Audio'):
				os.chdir('Audio')
				if not os.path.isdir(qstring):
					os.mkdir(qstring)
					os.chdir(qstring)
				else:
					os.chdir(qstring)
			for res in yt.streams.filter(only_audio=True).all():
				print(res)
			itag_no = input("\nInput <itag> number from above for interested item: ")
			itag_no = int(itag_no)
			final_select = input("If you want to skip this item press '0', else press '1' to download: ")
			final_select = int(final_select)
			if final_select == 0:
				continue
			elif final_select == 1:
				print('Downloading audio with <tag> ' + str(itag_no))
				yt.streams.get_by_itag(itag_no).download()

		print("Download Finished")

def v_scrape(query):
	base = "https://www.youtube.com/results?search_query="
	qstring = query
	r = requests.get(base+qstring)

	page = r.text
	soup=BeautifulSoup(page,'html.parser')

	vids = soup.findAll('a',{'class':'yt-uix-tile-link'})

	video_list = []
	for v in vids:
		tmp = 'https://www.youtube.com' + v['href']
		video_list.append(tmp)

	download_option = input("\nEnter 1 to bulk download, 2 to selectively download: ")
	download_option = int(download_option)
	if download_option == 1:
		print("\nBulk download mode active")
		count=0
		vid_res = input("Select video resolution:\n0 - 720p\n1 - 360p\nEnter:")
		vid_res = int(vid_res)
		print("\nDownloading Videos\n")
		print("\nTo skip at any time press `ctrl + Z`\n")
		os.chdir(current_dir)
		if not os.path.exists('Video'):
			os.mkdir('Video')
			os.chdir('Video')
			if not os.path.isdir(qstring):
				os.mkdir(qstring)
				os.chdir(qstring)
			else:
				os.chdir(qstring)
		if os.path.exists('Video'):
			os.chdir('Video')
			if not os.path.isdir(qstring):
				os.mkdir(qstring)
				os.chdir(qstring)
			else:
				os.chdir(qstring)		
		for item in video_list:
			count+=1
			yt = YouTube(item)
			print("Video. no " + str(count))
			if vid_res == 0:
					for res in yt.streams.filter(subtype='mp4').filter(res='720p').all():
						print(res)
						res.download()				
			elif vid_res == 1:
					for res in yt.streams.filter(subtype='mp4').filter(res='360p').all():
						print(res)
						res.download()

		print("Download Finished")
	elif download_option == 2:
		print("\nSelective download mode active")
		print("\nDownloading Video Information")
		print("\nTo skip at any time press `ctrl + Z`\n")
		count=0
		os.chdir(current_dir)
		if not os.path.exists('Video'):
			os.mkdir('Video')
			os.chdir('Video')
			if not os.path.isdir(qstring):
				os.mkdir(qstring)
				os.chdir(qstring)
			else:
				os.chdir(qstring)
		if os.path.exists('Video'):
			os.chdir('Video')
			if not os.path.isdir(qstring):
				os.mkdir(qstring)
				os.chdir(qstring)
			else:
				os.chdir(qstring)
		for item in video_list:
			count+=1
			yt = YouTube(item)
			print("\nShowing video " + str(count) + " details:")
			for res in yt.streams.filter(subtype='mp4').all():
				print(res)
			itag_no = input("\nInput <itag> number from above for interested item: ")
			itag_no = int(itag_no)
			final_select = input("If you want to skip this item press '0', else press '1' to download: ")
			final_select = int(final_select)
			if final_select == 0:
				continue
			elif final_select == 1:
				print('Downloading video with <tag> ' + str(itag_no))
				yt.streams.get_by_itag(itag_no).download()
				print('Download completed')

		print("Download Finished")

def voice_search():
	print("Voice Search:")
	search_item = ''
	while True:
		if not search_item:	
			r = sr.Recognizer()
			with sr.Microphone() as source:
			    print ('Say Something!')
			    audio = r.listen(source, timeout = None)
			    print ('Done!')
			search_item = r.recognize_google(audio)
			print("\nYou said " + str(search_item))
			return search_item
		break

def text_search():
	search_item = input("\nEnter the search keyword:")   ##search query input
	return search_item

while True:
	current_dir = os.getcwd()
	print('Cuurent Directory is: ' + str(current_dir))
	scrape_method = input("Enter \n1 - scrape `Text`\n2 - scrape `Images`\n3 - scrape `Videos`\n4 - scrape `Audios`\n5 - Exit\n\nYour option: ")
	scrape_method = int(scrape_method)
	if scrape_method == 1:
		print("\n##Text Scraper selected##")
		while True:
			input_means = input("Enter \n3 - `Text search`\n4 - `Voice search`\n\nText scraping using option:") 
			input_means = int(input_means)
			if input_means == 3:
				search_item = text_search()
				wiki_scrape(search_item)
				break
			elif input_means == 4:
				search_item = voice_search()
				wiki_scrape(search_item)
				break
			else:
				print("\nPlease enter a valid option")
	elif scrape_method == 2:
		print("\n##Images Scraper selected##")
		while True:
			input_means = input("Enter \n3 - `Text search`\n4 - `Voice search`\n\nImage scraping using option:")
			input_means = int(input_means) 
			if input_means == 3:
				search_item = text_search()
				gimage_scrape(search_item)
				break
			elif input_means == 4:
				search_item = voice_search()
				gimage_scrape(search_item)
				break
			else:
				print("Please enter a valid option")
	elif scrape_method == 3:
		print("\n##Videos Scraper selected##")
		while True:
			input_means = input("Enter \n3 - `Text search`\n4 - `Voice search`\n\nVideo scraping using option:")
			input_means = int(input_means) 
			if input_means == 3:
				search_item = text_search()
				v_scrape(search_item)
				break
			elif input_means == 4:
				search_item = voice_search()
				v_scrape(search_item)
				break
			else:
				print("Please enter a valid option")
	elif scrape_method == 4:
		print("\n##Audios Scraper selected##")
		while True:
			input_means = input("Enter \n3 - `Text search`\n4 - `Voice search`\n\nAudio scraping using option:")
			input_means = int(input_means) 
			if input_means == 3:
				search_item = text_search()
				a_scrape(search_item)
				break
			elif input_means == 4:
				search_item = voice_search()
				a_scrape(search_item)
				break
			else:
				print("Please enter a valid option")
	elif scrape_method == 5:
		exit()
	else:
		print("Please enter a valid option")
