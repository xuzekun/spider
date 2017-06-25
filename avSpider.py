import requests
from bs4 import BeautifulSoup

URL = ''

def download_page(url):
	html = requests.get(url,headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }).content
	return html

def parseMainPage(data):
	soup = BeautifulSoup(data)
	movie_list_soup = soup.find('div', attrs={'id': 'waterfall'})
	#print movie_list_soup
	detailPagesUrls = []
	list = movie_list_soup.find_all('div',attrs={'class':'item'})
	for movie_li in list: 
		#print movie_li
		movie_box = movie_li.find('a',attrs={'class':'movie-box'})
		href = movie_box.get('href')
		print href
		detailPagesUrls.append(href)
	return detailPagesUrls

def parseDetailPage(html):
	imageInfo = []
	soup = BeautifulSoup(html)
	bigImage = soup.find('a',attrs={'class':'bigImage'})
	bigImageUrl = bigImage.get('href')
	bigImageName = bigImage.get("title")
	imageInfo.append((bigImageUrl, bigImageName))
	sampleList = soup.find_all('a',attrs={'class':'sample-box'})
	for sample in sampleList:
		imageUrl = sample.get('href')
		imageName = sample.get('title')
		imageInfo.append((imageUrl, imageName))
	return imageInfo
		

def downloadImage(imageUrl,imageName):
	print imageUrl
	print imageName
	r = requests.get(imageUrl,stream=True)
	with open(imageName +'.jpg','wb') as f:
		for chunk in r.iter_content():
			f.write(chunk)

def main():
	data = download_page(URL)
	detailPagesUrls = parseMainPage(data)
	for detailPageUrl in detailPagesUrls:
		html = download_page(detailPageUrl)
		imageInfo = parseDetailPage(html)
		for url, name in imageInfo:
			downloadImage(url, name)

if __name__ == '__main__':
	main()