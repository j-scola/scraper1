from bs4 import BeautifulSoup
import requests
import time
import os

done = False
unfamiliar_skills = []

print('If there are any skills you would like remove from results, type them below. Leave blank to skip.')
while not done:
  unfamiliar_skill = input('>')
  if unfamiliar_skill == '':
    done = True
  else:
    unfamiliar_skills.append(unfamiliar_skill)
    
print(f'Getting jobs...')
if len(unfamiliar_skills):
  print('Results with skills you entered will be removed:')
  for skill in unfamiliar_skills:
    print(skill)

def find_jobs():
  html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=').text
  soup = BeautifulSoup(html_text, 'lxml')
  # parse out the details of the job listing
  joblist = soup.find('ul', class_='new-joblist')
  job_cards = joblist('li', class_='job-bx')
  for index, job_card in enumerate(job_cards):
    posted_on = job_card.find('span', class_='sim-posted').span.text
    if posted_on.find('few days ago') >= 0:
      url = str(job_card.header.h2.a['href'])
      job_id = url[url.find('jobid-'):]
      job_id = job_id[job_id.find('-') + 1:job_id.find('_')]
      details = job_card.find('ul', class_='top-jd-dtl').findAll('li')
      job_title_tuple = job_card.find('h2').text,
      for title in job_title_tuple:
        job_title = title.replace('\n', '').replace(' ','')
      company_name = job_card.find('h3', class_='joblist-comp-name').text.replace(' ', '')
      skills = job_card.find('span', class_='srp-skills').text.replace('\n', '').replace(' ', '')
      location = details[-1].text.split('\n')[2]
      # experience level
      experience = details[0].text

      should_save = True
      for skill in unfamiliar_skills:
        if skill not in skills:
          should_save = False
      if should_save:
        try: 
          with open(f'data/{job_id}.txt', 'x') as f:
            line2 = f'Job Title: {job_title.strip()}\n'
            line1 = f'Company Name: {company_name.strip()}\n'
            line5 = f'Location'
            line3 = f'Skills: {skills.strip()}\n'
            line4 = f'Link to job listing: {url}\n'
            f.write(line1)
            f.write(line2)
            f.write(line3)
            f.write(line4)
            print(f'Job data saved in to data/{job_id}.txt')
            f.close()
          # except FileExistsError as err:
          #   print(f'Already saved job with id {job_id}')
        except FileExistsError as err:
          print('found previously saved job')
           

if __name__ == '__main__':
  run_count = 100000
  while run_count > 0:
    run_count -= 1
    find_jobs()
    time_wait = .5
    print(f'Waiting {time_wait} minutes... ({run_count} runs remaining)')
    time.sleep(time_wait * 60)

  
