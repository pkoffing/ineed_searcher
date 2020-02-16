# -*- coding: utf-8 -*-
"""
Indeed Job Web Scraper
"""
from urllib import request
import re
job_count = 0
job_list = []


class Job:
    def _init_(self, company = None, location = None, title = None, salary = None):
        self.company = company
        self.location = location
        self.title = title
        self.salary = salary

SearchTerms = {
'OneWordA' : ['Reseach', 'Lab', 'Laboratory'],
'OneWordB' : ['Assistant', 'Technician','Technologist', 'Scientist'],
'FullSearch': ['Biotech', ['Junior', 'Biotech'], ['Cell', 'Culture'],['Tissue','Culture'],['Synthetic','Biology']]}

def url_gen(adj1, loc, adj2 = None):
    '''
    Takes in 1 or 2 search term adjectives as string and one locatation.
    Returns an indeed search url as a string.
    '''
    if adj2 == None:
        return 'https://www.indeed.co.uk/jobs?q='+adj1+'&sort=date&l='+loc+'&radius=5&limit=100'
    else:
        return 'https://www.indeed.co.uk/jobs?q='+adj1+'+'+adj2+'&sort=date&l='+loc+'&radius=5&limit=100'

def gen_url_list():
    url_list = []
    for name1 in SearchTerms['OneWordA']:
        for name2 in SearchTerms['OneWordB']:
            url_list.append(url_gen(name1, 'N15+3HB', name2))
            url_list.append(url_gen(name1, 'Stevenage', name2))
    for name3 in SearchTerms['FullSearch']:
        if type(name3) == type(list):
            url_list.append(url_gen(name3[0], 'N15+3HB', name3[1]))
            url_list.append(url_gen(name3[0], 'Stevenage', name3[1]))
        elif type(name3) == type(str):
            url_list.append(url_gen(name3[0], 'N15+3HB'))
            url_list.append(url_gen(name3[0], 'Stevenage'))
    return url_list

def is_unique(job): #TODO
    '''
    Checks is a job is unique somehow????
    '''
    for jobs in job_list:
        if jobs.description == job.description:
            return True
    return False


def page_scrape(url):
    '''
    Takes an indeed search url as an arguement - url.
    Returns a list of raw job info strings
    '''
    page = request.urlopen(url)
    page = str(page.read())
    return str(re.findall(r'(jobmap\[(.+)\})', page))

def job_construct(raw_job):
    '''
    Takes a links of raw job info strings.
    Adds 'Job' class objects to a list of jobs.
    Returns None.
    '''
    job_list = []
    for raw_job in raw_job:
        company = re.findall(r'cmp:\'(.+)\'?', raw_job)
        location = re.findall(r'loc:\'(.+)\'?', raw_job)
        title = re.findall(r'title:\'(.+)\'?', raw_job)
        exec('job'+str(job_count)+'=Job(company,location,title)')
        exec('job_list.append(job%'+str(job_count))
        job_count+=1
    return job_list
        
def bain():
    url_list = gen_url_list()
    for url in url_list:
        raw_data = page_scrape(url)
        data = job_construct(raw_data)
        for job in data:
            job_list.append(job)
        
    
    