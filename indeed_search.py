# -*- coding: utf-8 -*-
"""
Indeed Job Web Scraper
"""
from urllib import request
import re
raw_list = []
job_list = []


class Job:
    def __init__(self, raw_job):
        info = self.pull_raw_job(raw_job)
        
        self.company = info[0]
        self.location = info[1]
        self.title = info[2]
        self.url = 'http://www.indeed.co.uk/viewjob?jk='+info[3]
    
#        self.description = self.pull_decription()
        
        
    def __str__(self): #TODO
        pass
    
    def pull_raw_job(self,raw_job):
        '''Takes in a raw job string. Returns a tuple containing, title, location
        company, salay, and url'''
        company = re.findall(r'cmp:\'(.+?)\'', raw_job)[0]
        location = re.findall(r'loc:\'(.+?)\'', raw_job)[0]
        title = re.findall(r'title:\'(.+?)\'', raw_job)[0]
        url = re.findall(r'jk:\'(.+?)\'', raw_job)[0]
        return (company, location, title, url)
    
    def pull_decription(self):
        '''Extracts job descriptions from indeed url. Return job description as
        a string
        '''
        page = request.urlopen(self.url)
        page = str(page.read())
        search = re.findall(r'jobDescriptionText\"\>.+\</p\>\<p\>*?(.+*?)id=\"mapRoot\"', page)
    def is_unique(self):
        '''Checks if job already exists in job_list. Returns True if it doens't
        '''
        
## 


def gen_url_list():
    '''Returns a list of indeed job search urls based on search terms.
    '''
    
    #List Search Terms
    SearchTerms = {
    'OneWordA' : ['Reseach', 'Lab', 'Laboratory'],
    'OneWordB' : ['Assistant', 'Technician','Technologist', 'Scientist'],
    'FullSearch': ['Biotech', ['Junior', 'Biotech'], ['Cell', 'Culture'],['Tissue','Culture'],['Synthetic','Biology']]}

    url_list = []
    
    #General method for putting a url together form search terms
    def url_gen(adj1, loc, adj2 = None):
    '''
    Takes in 1 or 2 search term adjectives as string and one locatation.
    Returns an indeed search url as a string.
    '''
        if adj2 == None:
            return 'https://www.indeed.co.uk/jobs?q='+adj1+'&sort=date&l='+loc+'&radius=5&limit=100'
        else:
            return 'https://www.indeed.co.uk/jobs?q='+adj1+'+'+adj2+'&sort=date&l='+loc+'&radius=5&limit=100'

    
     #Method for generating combinations of search terms
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



def page_scrape(url):
    '''
    Takes an indeed search url as an argument - url.
    Returns a list of raw job info strings
    '''
    page = request.urlopen(url)
    page = str(page.read())
    jobs = re.findall(r'jobmap\[\d+\]\= \{[\w \:\'\,\/\-\\]+};', page)
    return jobs

def job_constructor(raw_job):
    '''
    Takes a links of raw job info strings.
    Adds 'Job' class objects to a list of jobs.
    Returns None.
    '''
    for raw_job in raw_job:
        exec('job'+str(len(job_list))+'=Job(raw_job)')
        exec('job_list.append(job'+str(len(job_list)))        
