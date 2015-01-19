import re
import time
import urllib
import requests
from requests import *
from bs4 import BeautifulSoup
from pymongo import *


base_url = "http://www.localbanya.com"

#mongodb connection
client = MongoClient()
db = client['banya_scrap']
col = db['banyacoll']

# categories
def make_soup( url, uheaders=None, payload=None ):
	if not uheaders or uheaders is None:
		before_2_min = time.time()-120
		before_2_half_min = time.time()-124
		current_time = time.time()
		cookie_value='Cookie_Supported=1; __lc.visitor_id.4488361=S1419586905.8b4c8bb769; _ga=GA1.2.1395525224.1419586898; ww_Cookie_LB_AT=151071; L_Cookie_Campaign=true; lb_session=a:5:{s:10:"session_id";s:32:"e1fb1e65edb274ffa6eafa4a015cd4f2";s:10:"ip_address";s:15:"122.177.175.100";s:10:"user_agent";s:105:"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36";s:13:"last_activity";i:%d;s:9:"user_data";s:0:"";}a0c1ad5be6c0ff5c9c2b5f2b1c790cba; __utmt=1; __utma=206849294.1395525224.1419586898.1421319303.1421390281.23; __utmb=206849294.1.10.1421390281; __utmc=206849294; __utmz=206849294.1420823804.15.3.utmcsr=9.1.15_banner_2|utmccn=fortune|utmcmd=fortune; WZRK_P=http://www.localbanya.com/; Prod_LB_CartID=1905123; lc_window_state=minimized; WZRK_G=5f480883b49d43ae875449007a1fafe8; WZRK_S_KZR-7R7-49KZ={"p":1,"s":%d,"t":%d}'%(before_2_half_min, before_2_min, current_time)
		headers = {
				"Accept":"application/json, text/javascript, */*; q=0.01",
				"Accept-Encoding":"gzip,deflate,sdch",
				"Accept-Language":"en-US,en;q=0.8",
				"Cache-Control":"max-age=0",
				"Connection":"keep-alive",
				# "Cookie":cookie_value,
				"Host":"www.localbanya.com",
				"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36",
			}
	else:
		headers = uheaders
	try:
		if payload:
			payload_data = payload
		else:
			payload_data = None
		soup = BeautifulSoup(requests.get(url, headers=headers, params=payload_data).text)
	except ConnectionError as e:
		soup = BeautifulSoup(requests.get(url, headers=headers, params=payload_data).text)
	return soup

soup = make_soup(base_url)
"""
# subcategory->shows only 20 list at a time, 
check total quantity of products, if > 20
then make a post request with query string
{
	task:products
	subcat_id:17
	start:20
	total:45
	sort:
	tags:
	brands:
} 
"""

def more_product( **kwargs ):
	before_2_min = time.time()-120
	before_2_half_min = time.time()-124
	current_time = time.time()
	if kwargs['total_items'] > 20:
		# make an request, json result expected
		# filter html with new line feed escape character
		total_pagination_call = kwargs['total_items']/20 
		# for odd number
		if not kwargs['total_items']%20 == 0:
			total_pagination_call += 1
		else:
			pass
		print total_pagination_call
		counter = 0
		increment_counter = 20
		while(counter < total_pagination_call):
			start_num = increment_counter
			payload = {
				"task":"products",
				"subcat_id":kwargs["sub_cat_id"],
				"start":start_num,
				"total":kwargs['total_items'],
				"sort":'',
				"tags":'',
				"brands":''
			}
			encoded_url=urllib.quote_plus(kwargs['url'])
			last_activity = time.time()-60 
			current_time = time.time()
			cookie_value='Cookie_Supported=1; __lc.visitor_id.4488361=S1419586905.8b4c8bb769; _ga=GA1.2.1395525224.1419586898; ww_Cookie_LB_AT=151071; lb_session=a:5:{s:10:"session_id";s:32:"cce1debe4e870b600eb342c7dd67739f";s:10:"ip_address";s:15:"122.177.175.100";s:10:"user_agent";s:105:"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36";s:13:"last_activity";i:%d;s:9:"user_data";s:0:"";}0ffd6920a6f65863364a3852973ac9df; __utmt=1; WZRK_G=5f480883b49d43ae875449007a1fafe8; WZRK_S_KZR-7R7-49KZ={"p":1,"s":%d,"t":%d}; L_Cookie_Campaign=true; __utma=206849294.1395525224.1419586898.1421319303.1421390281.23; __utmb=206849294.4.10.1421390281; __utmc=206849294; __utmz=206849294.1420823804.15.3.utmcsr=9.1.15_banner_2|utmccn=fortune|utmcmd=fortune; WZRK_P=%s; Prod_LB_CartID=1905123; lc_window_state=minimized'%(last_activity, current_time, current_time, encoded_url)
			request_product_headers = {
				"Accept":"application/json, text/javascript, */*; q=0.01",
				"Accept-Encoding":"gzip,deflate,sdch",
				"Accept-Language":"en-US,en;q=0.8",
				"Connection":"keep-alive",
				# "Cookie":"%s"%cookie_value,
				"Host":"www.localbanya.com",
				"Referer":"http://www.localbanya.com/products/Breakfast-&-Health-Food/Cereals/173/3?isCampaign=true",
				"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36",
				"X-Requested-With":"XMLHttpRequest"
			}
			counter += 1
			increment_counter += 20
			print counter, increment_counter
			more_request_url="http://www.localbanya.com/home/next_page"
			more_result_response_html = requests.get( more_request_url, headers=request_product_headers, params = payload )
			html_data = more_result_response_html.json()['response'].encode('utf-8').replace("\n", '').replace("\'", "'")
			print 'more result'
			msoup = BeautifulSoup( html_data )
			for details in msoup.findAll("div", {"class": "product-inner"}):
				data = {
					"category": kwargs['category_title'],
					"product_category": kwargs['sub_cat_title'], 
					"product_details": {
						"image_source": details.find("img", {"class": "prod_img"})['src'].encode('utf-8').strip(),
						"name": details.find("div", {"class": "prName"}).text.encode('utf-8').strip(),
						"quantity": details.find("span", {"class": "sku_weight"}).text.encode('utf-8').strip(),
						"price": details.find("div", {"class": "new-price"}).text.encode('utf-8').strip()
					}	
				}
				print data

	return

for category in soup.findAll("a", {"class": "cat-name"})[1:2]:
	for sub_cat in soup.findAll("a", {"class": "sub_cat"})[6:7]:
		encoded_url=urllib.quote_plus(sub_cat['href'])
		last_activity = time.time()-60 
		current_time = time.time()
		cookie_value='Cookie_Supported=1; __lc.visitor_id.4488361=S1419586905.8b4c8bb769; _ga=GA1.2.1395525224.1419586898; ww_Cookie_LB_AT=151071; lb_session=a:5:{s:10:"session_id";s:32:"cce1debe4e870b600eb342c7dd67739f";s:10:"ip_address";s:15:"122.177.175.100";s:10:"user_agent";s:105:"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36";s:13:"last_activity";i:%d;s:9:"user_data";s:0:"";}0ffd6920a6f65863364a3852973ac9df; L_Cookie_Campaign=true; __utmt=1; __utma=206849294.1395525224.1419586898.1421319303.1421390281.23; __utmb=206849294.3.10.1421390281; __utmc=206849294; __utmz=206849294.1420823804.15.3.utmcsr=9.1.15_banner_2|utmccn=fortune|utmcmd=fortune; WZRK_P=%s; WZRK_G=5f480883b49d43ae875449007a1fafe8; WZRK_S_KZR-7R7-49KZ={"p":1,"s":%d,"t":%d}; Prod_LB_CartID=1905123; lc_window_state=minimized'%(last_activity, encoded_url, current_time, current_time)
		sub_category_headers = {
			"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
			"Accept-Encoding":"gzip,deflate,sdch",
			"Accept-Language":"en-US,en;q=0.8",
			"Cache-Control":"max-age=0",
			"Connection":"keep-alive",
			# "Cookie":"%s"%cookie_value,
			"Host":"www.localbanya.com",
			"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36"
		}
		sub_cat_details = make_soup(sub_cat['href'], uheaders=sub_category_headers)
		for details in sub_cat_details.findAll("div", {"class":"product-inner"}):
			data = { 
				"category": category.text.encode('utf-8').strip(),
				"product_category": sub_cat.text.encode('utf-8').strip(), 
				"product_details": {
						"image_source": details.find("img", {"class": "prod_img"})['src'].encode('utf-8').strip(),
						"name": details.find("div", {"class": "prName"}).text.encode('utf-8').strip(),
						"quantity": details.find("span", {"class": "sku_weight"}).text.encode('utf-8').strip(),
						"price": details.find("div", {"class": "new-price"}).text.encode('utf-8').strip()
					}
				}

			col.update(
				{"category":category.text.encode('utf-8').strip()},
				{"$push": { "product_details" :{ 
				"image_source" : details.find("img", {"class": "prod_img"})['src'].encode('utf-8').strip(),
				"name": details.find("div", {"class": "prName"}).text.encode('utf-8').strip(),
				"quantity" : details.find("span", {"class": "sku_weight"}).text.encode('utf-8').strip(),
				"price" : details.find("div", {"class": "new-price"}).text.encode('utf-8').strip() } } } )

		total_display_items_per_request = int(re.search( r'\d+', sub_cat_details.find("h2").text.strip().encode("utf-8") ).group())
		print total_display_items_per_request
		if total_display_items_per_request > 20:
			split_url = sub_cat['href'].split("/")
			sub_cat_id = int(split_url[len(split_url)-1].split("?")[0])
			params_data = {	
							"url": sub_cat['href'], 
							"total_items": total_display_items_per_request, 
							"sub_cat_id": sub_cat_id ,
							"category_title": category.text.encode('utf-8').strip(),
							"sub_cat_title": sub_cat.text.encode('utf-8').strip()
						}
			more_product( **params_data )
		else:
			print '< 20 products in %s'%sub_cat.text