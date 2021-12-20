from bs4 import BeautifulSoup
import requests

# request the html file based on search parameters
html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=').text

# apply soup lxml parsing
soup = BeautifulSoup(html_text, 'lxml')

# create list of job cards
joblist = soup.find('ul', class_='new-joblist')

# create a list to store objects
jobs_data = []
try:
  job_cards = joblist('li', class_='job-bx')
  for job_card in job_cards:
    
    posted_on = job_card.find('span', class_='sim-posted').span.text
    if posted_on.find('few days ago') >= 0:
    
      details = job_card.find('ul', class_='top-jd-dtl').findAll('li')
      
      job_title_tuple = job_card.find('h2').text,
      for title in job_title_tuple:
        job_title = title.replace('\n', '').replace(' ','')

      company_name = job_card.find('h3', class_='joblist-comp-name').text.replace(' ', '')
      
      skills = job_card.find('span', class_='srp-skills').text.replace('\n', '').replace(' ', '')
    
      location = details[-1].text.split('\n')[2]
      experience = details[0].text
      
      # Job_data = {
      #   'company_name': company_name,
      #   'job_title': job_title,
      #   'location': location,
      #   'experience': experience,
      # }
      
      jobs_data.append(f'''

Company Name: {company_name}
Job Title:
{job_title}


Skills:
{skills}

__________________________________
''')
except:
  print('an error occurred durring html file parsing')
    
if len(jobs_data) > 0:
  file = open('scrape_results.txt', 'w')
  file.writelines(jobs_data)
  file.close()


    
  
  