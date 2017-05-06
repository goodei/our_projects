from bs4 import BeautifulSoup
from req import get_html

# html = """
# <html>
# 	<head>
# 		<title></title>
# 	</head>
# 	<body>
# 		<h1></h1>
# 		<p></p>
# 		<p></p>
# 		<p></p>
# 	</body>
# </html>
# """

html = get_html('https://yandex.ru/search/?lr=213&msid=1492258299.59905.22879.9839&text=python')

if html:
	bs = BeautifulSoup(html, 'html.parser')

	data = []

	for item in bs.find_all('li', class_='serp-item'):
		block_title = item.find('a',class_='organic__url')
		href = item.find(a, class_='path__item')
		data.append({
			'title': block_title.text,
			'link': href.get('href')
		})

print(data)

#for para in bs.find_all('p'):
#	print(para.text)