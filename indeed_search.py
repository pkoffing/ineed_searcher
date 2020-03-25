# -*- coding: utf-8 -*-
"""
Indeed Job Web Scraper
"""
from urllib import request
import re, pickle #TODO
from bs4 import BeautifulSoup


#loads pickle file  into job list and is_searched #TODO
# Empty Lists for storing jobs and Job objects

job_list = []
is_searched = []

if job_list:
    for job in job_list:
        is_searched.append(job.url)

## Regular Expressions

## Searches Indeed Search Result Page Source, pulls out job information
##relating to job and returns as a tuple (url, company name, job location
##job title) in that order

job_pattern = re.compile(r"""
jobmap\[\d+\]\=\s\{                             #Raw Job header
jk:\\\'([\w \: \' \, \\ \/ \-]+?)\\\'           #Url String
[\w \: \' \, \\ \/ \-]+?[\w\s\:\'\,\\\/\-]+?    #Unwanted Extraneous Text
cmp:\\\'([\w \: \' \, \\ \/ \-]+?)\\\'          #Company Name  
[\w \: \' \, \\ \/ \-]+?                        #Unwanted Extraneous Text          
loc:\\\'([\w \: \' \, \\ \/ \-]+?)\\\'          #Job Location
[\w \: \' \, \\ \/ \-]+?                        #Unwanted Extraneous Text
title:\\\'([\w \: \' \, \\ \/ \-]+?)\\\'        #Job Title
[\w \: \' \, \\ \/ \-]+?                        ##Unwanted Extraneous Text
\'\};                                           #Raw Job Ending
""", re.VERBOSE)


#Object representing a given job

class Job:
    def __init__(self, job_tuple):
        
        self.company = job_tuple[1]
        self.location = job_tuple[2]
        self.title = job_tuple[3]
        self.url = 'http://www.indeed.co.uk/viewjob?jk='+job_tuple[0]
    
        self.description = self.pull_decription() 
        self.status = 'UNREAD'
        
    def __str__(self): #TODO
        return '<%s, %s, %s> \n %s' % (self.title, self.company, self.location, self.description)
    
    def change_status(self):
        """
        Changes interest to bool of parameter. Toggles bool by default with no 
        parameters
        """ 
        
        user = input("""Would you like to change this job\'s status?
                     The current status is """+self.status+' Y or N.')
        if user != 'Y' or user != 'N':
            print ('Input needs to be \'Y\' or \'N\'. Please try again')
            break
        

    
    def pull_decription(self):
        '''Extracts job descriptions from indeed url. Return job description as
        a string
        '''
        page = str(request.urlopen(self.url).read())
        soup_page = BeautifulSoup(page, 'lxml')
        description = soup_page.find('div', class_ = 'jobsearch-jobDescriptionText').text
        return description
## URL Search Generator


SearchTerms = {
    'OneWordA' : ['Reseach', 'Lab', 'Laboratory'],
    'OneWordB' : ['Assistant', 'Technician','Technologist', 'Scientist'],
    'FullSearch': ['Biotech', ['Junior', 'Biotech'], ['Cell', 'Culture'],['Tissue','Culture'],['Synthetic','Biology']]}

def gen_url_list():
    '''Returns a list of indeed job search urls based on search terms.
    '''
    
    url_list = []
    
    #General method for putting a url together from search terms
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

#URL Scraping Functions

def page_scrape(url):
    '''
    Takes an indeed search url as an argument - url.
    Returns a list of raw job info strings
    '''
    page = str(request.urlopen(url).read())
    
    for tup in job_pattern.findall(page):
        if tup[0] in is_searched:
            pass
        else:
            is_searched.append(tup[0])
            exec('job'+str(len(is_searched))+'=Job(tup)')
            exec('job_list.append(job'+str(len(is_searched))+')')
            
        
for url in gen_url_list():
     page_scrape(url)
     
for job in job_list:
    print (job)
     

