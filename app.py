# Libraries
import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

# Variables
page_num = 0

# Lists
job_titles_list = []
company_names_list = []
location_names_list = []
job_skills_list = []
links = []
posted_list = []

while True:
    # Fetch the url
    result = requests.get(f'https://wuzzuf.net/search/jobs/?a=hpb&q=front-end&start={page_num}')

    # Get content
    content = result.content

    # Fetch content with BeautifulSoup
    soup = BeautifulSoup(content, "lxml")

    # Find the elements containing info we need.
    job_titles = soup.find_all('a', { "class": "css-o171kl", "rel": "noreferrer" })
    first_job = soup.find('a', { "class": "css-o171kl", "rel": "noreferrer" })
    company_names = soup.find_all('a', { "class": "css-17s97q8" })
    location_names = soup.find_all('span', { "class": "css-5wys0k" })
    job_skills = soup.find_all("div", { "class": "css-y4udm8" })
    job_etc = soup.find_all("a", { "class": "css-n2jc4m" })
    posted_new = soup.find_all("div", { "class": "css-4c4ojb" })
    posted_old = soup.find_all("div", { "class": "css-do6t5g"})
    posted = [*posted_new, *posted_old]

    number_of_jobs = soup.find("strong").text
    number_of_pages = int(number_of_jobs) // 15

    if (page_num > number_of_pages):
        print("Ends")
        break

    # Iterate over elements to get text
    for i in range(len(job_titles)):
        job_titles_list.append(job_titles[i].text)
        links.append(job_titles[i].attrs['href'])
        company_names_list.append(company_names[i].text)
        location_names_list.append(location_names[i].text)
        job_skills_list.append(job_skills[i].text)
        posted_list.append(posted[i].text.strip())

    print(page_num)

    # Increment
    page_num = page_num + 1

    # print(job_titles_list)
    # print(company_names_list)
    # print(location_names_list)
    # print(job_skills_list)
    # print(links)
    # print(posted_list)

# create csv file and fill it with values

full_list = [job_titles_list, company_names_list, location_names_list, job_skills_list, links, posted_list]
exported = zip_longest(*full_list)
with open("file.csv", "w") as myfile:
    wr = csv.writer(myfile)
    wr.writerow(["Job Title", "Company Name", "Location", "Skills", "Links", "Posted At"])
    wr.writerows(exported)