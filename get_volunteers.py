from bs4 import BeautifulSoup

import requests
import pickle

# run time - virtual - 15 min [only 20 results - bug?]
# run time - oakland - 6 min - get 2K job ids - 23 min total - pickle jobs
# run time - los angeles - 20 min



def print_job_ids(url):
	r = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data, 'html.parser')

	for item in soup.find_all(class_="searchitem PUBLIC"):
		print(item.get('id'))

def get_job_ids(url, id_set):
	#print(url)
	#print(len(id_set))
	r = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data, 'html.parser')

	for item in soup.find_all(class_="searchitem PUBLIC"):
		next_id = item.get('id')
		#print(next_id)
		id_set.add(next_id)

	#print(len(id_set))
	return id_set

def run_print_function(base_url):
	result_number = 11
	result_string = '11'
	url = base_url + result_string

	while(result_number < 1266):
		print("results: %d" % result_number)
		print_job_ids(url)
		result_number += 10
		result_string = str(result_number)
		url = base_url + result_string

	print('all results printed')


def from_volunteer_match(input_url, location, savefile):

	base_url = 'https://www.volunteermatch.org/search/'
	#end_virtual_url = ''

	# generate correct search url based on location
	if (location == 'Chicago'):
		print('searching for volunteer jobs in Chicago')
		base_url = input_url + 'Chicago%2C+ILA&o=recency&s='
	elif (location == 'Brooklyn'):
		print('searching for volunteer jobs in Brooklyn')
		base_url = input_url + 'Brooklyn%2C+NY&o=recency&s='
	elif (location == 'Los Angeles'):
		print('searching for volunteer jobs in Los Angeles')
		base_url = input_url + 'Los+Angeles%2C+CA&o=recency&s='
	elif (location == 'Oakland'):
		print('searching for volunteer jobs in Oakland')
		base_url = input_url + 'Oakland%2C+CA&o=recency&s='
	elif (location == 'Virtual'):
		print('searching for Virtual volunteer jobs')
		base_url = 'https://www.volunteermatch.org/search/?aff=&includeOnGoing=true&v=true&o=distanceBand&s='
		#end_virtual_url = '1&o=distanceBand&l=San+Francisco%2C+CA%2C+USA&r=20&sk=&specialGroupsData.groupSize=&na=&partner=&usafc='


	result_number = 1
	result_string = str(result_number)
	#url = base_url + end_virtual_url

	id_set = set()
	#id_set = get_job_ids(url, id_set)
	#print_job_ids(url)

	#actual number for all virutal results: 6832 1/31/18
	#while result_number < 6832:
	#actual number for all oakland results: 2032 1/31/18
	#actual number for all la results: 2200 1/31/18
	#actual number for all chicago results: 1317 2/1/18
	#actual number for all brooklyn results: 2345 2/1/18
	while result_number < 2400:
		full_url = base_url + result_string
		#full_url = base_url + result_string + end_virtual_url
		#print(full_url)
		#print_job_ids(full_url)
		id_set = get_job_ids(full_url, id_set)
		# for local locations
		result_number += 10
		# for virtual locations
		#result_number += 1
		result_string = str(result_number)

	print("there are %d volunteer jobs in %s" % (len(id_set), location))
	opportunity_list = []

	for opportunity in id_set:
		url = 'https://www.volunteermatch.org/search/' + opportunity + '.jsp'
		r = requests.get(url)
		data = r.text
		soup = BeautifulSoup(data, 'html.parser')
		title = str(soup.find(class_='opp_title_heading'))
		organization = str(soup.find(class_='opp_detail_org_name'))
		summary = str(soup.find(class_="opp_summary"))
		headings = soup.find_all(class_='opp_lower_container_section')

		opportunity_string = ""
		opportunity_string += title
		opportunity_string += organization
		opportunity_string += summary
	
		for item in headings:
			item_string = str(item)
			opportunity_string += item_string
			#pass

		opportunity_list.append(opportunity_string)

	pickle.dump( opportunity_list, open(savefile, "wb" ) )
	print('opportunity_list pickled.')

# passed an html page as beautiful soup
# returns a set of links to next pages
def get_page_links(html):
	page_links = set()

	for item in html.find_all(class_='page-item'):
		for atag in item.find_all('a'):
			link = atag.get('href')
			link_string = str(link)
			if link_string.startswith('?page='):
				page_links.add(link_string)
	return page_links

def get_opportunity_links(html, opportunity_links):
	for item in html.find_all('a'):
		link = item.get('href')
		link_string = str(link)
		if link_string.startswith('/volunteer/'):
			opportunity_links.add(link_string)

	return opportunity_links


def from_catch_a_fire(input_url, savefile):

	r = requests.get(input_url+'/volunteer/')
	data = r.text
	soup = BeautifulSoup(data, 'html.parser')

	opportunities = set()
	opportunities = get_opportunity_links(soup, opportunities)
	pages = get_page_links(soup)

	for page in pages:
		url = input_url + '/volunteer/' + page
		response = requests.get(url)
		data = response.text
		soup = BeautifulSoup(data, 'html.parser')
		opportunities = get_opportunity_links(soup, opportunities)

	opportunity_list = []

	for opportunity in opportunities:
		opportunity_url = input_url + opportunity

		r = requests.get(opportunity_url)
		data = r.text
		soup = BeautifulSoup(data, 'html.parser')

		opportunity_list.append(str(soup))


	pickle.dump( opportunity_list, open(savefile, "wb" ) )
	print('opportunity_list pickled.')



def from_la_works():
	url = 'https://www.laworks.com/opportunity-search'
	r = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data, 'html.parser')
	opportunity_list = []
	opportunity_html = []

	for item in soup.find_all('a'):
		link = item.get('href')
		link_string = str(link)
		if link_string.startswith('/opportunity/'):
			#print(link_string)
			opportunity_list.append(link_string)
	print ('links found')

	for opp in opportunity_list:
		opp_url = 'https://www.laworks.com' + opp
		r = requests.get(opp_url)
		data = r.text
		soup = BeautifulSoup(data, 'html.parser')

		#print('\n\n NEW OPPORTUNITY \n\n')

		# div class_ = opportunity-banner-content
		# div class_ = organization-detail
		# h5: Volunteer Roles & Responsiblities (list items)
		# div class_ = express-interest-block template (for additional dates)
		# data-occ-start-date-time
		# data-occ-end-date-time

		title = str(soup.find(class_='opportunity-banner-content'))
		description = str(soup.find(class_='organization-detail'))

		opportunity_string = title + description
		opportunity_html.append(opportunity_string)

		#for item in soup:
		#	print(item)

	print(len(opportunity_html))

def from_sponsorchange(url, savefile):
	r = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data, 'html.parser')

	links = soup.find_all('a')

	for link in links:
		url = link.get('href')
		print(link.get('href'))




def main():
	volunteermatch_url = 'https://www.volunteermatch.org/search?l='
	catchafire_url = 'https://www.catchafire.org'
	sponsorchange_url = 'http://www.sponsorchange.org/?page_id=144'

	#other options: LA, Oakland, Brooklyn
	#location = 'Chicago'
	#location = 'Los Angeles'
	#location = 'Oakland'
	location = 'Brooklyn'
	#location = 'Virtual'

	#volunteermatch_filename = 'volunteermatch-virtual-jobs.p'
	#volunteermatch_filename = 'volunteermatch-chicago-jobs.p'
	#volunteermatch_filename = 'volunteermatch-la-jobs.p'
	#volunteermatch_filename = 'volunteermatch-oakland-jobs.p'
	volunteermatch_filename = 'volunteermatch-brooklyn-jobs.p'

	catchafire_filename = 'catchafire-jobs.p'
	sponsorchange_filename = 'sponsorchange-jobs.p'

	from_volunteer_match(volunteermatch_url, location, volunteermatch_filename)
	#from_catch_a_fire(catchafire_url, catchafire_filename)
	#from_la_works()
	#from_sponsorchange(sponsorchange_url, sponsorchange_filename)


if __name__ == '__main__':
	main()
