#!/usr/bin/env python
# coding: utf-8

# In[48]:


import pandas as pd
import requests
import json
import time
import urllib.request
import os
import csv
import dropbox


# In[49]:


sinceDate = ""

#os.chdir('ImageFiles1')

userIDs = {'joeyshaw' : 'JoeyShaw', 
           'destes' : 'DwayneEstes', 
           #'themorrislab' : 'AshleyMorris',
           #'ruhfel' : 'BradRuhfel', 
           #'kentuckybotanist': 'TaraLittlefield'
          }

tot_list = open('/users/aidanshaw/python/Files/iNatData/Running_list.csv', 'w')
writer = csv.writer(tot_list)

dbx = dropbox.Dropbox("vxb15liTLwsAAAAAAAATe22NyPLCUpDrrCbkYOsH1GIdLN4tjj-wDVpIc4OtERQQ")



species_list = pd.read_excel('TNKY_list.xlsx')

species_list = list(species_list['TNKY ScientificName'])

species_str = '//'.join(species_list)


file_names = []
file_url = []


# In[50]:


for userID, userName in userIDs.items(): 
    url = f'https://api.inaturalist.org/v1/observations?identified=true&photos=true&user_login={userID}&updated_since={sinceDate}&order=desc&order_by=created_at'
    resp = requests.get(url=url)
    time.sleep(1.1)
    jsonData = resp.json() # Check the JSON Response Content documentation below
    totResults = jsonData['total_results']
    if totResults > 0:
        whole, decimal = str((totResults / 200)).split('.')
        whole = int(whole)
        if int(decimal) > 0:
            whole += 1
            maxPages = whole

        print (userName)
        print (totResults)

        #pages = range(1, (maxPages + 1))
        pages = range(1, 2)
        if maxPages > 1 == True:
            for page in pages[:2]:
                print(f'on page {page} of {len(pages)}')
                url = f'https://api.inaturalist.org/v1/observations?identified=true&photos=true&user_login={userID}&iconic_taxa=Plantae&page={page}&per_page=200&&updated_since={sinceDate}&order=desc&order_by=created_at'
                resp = requests.get(url=url)
                jsonData = resp.json() # Check the JSON Response Content documentation below
                results1 = jsonData['results']

                for obs in results1:
                    
                    if obs['taxon']['name'] in species_str:
                        
                        taxonName = obs['taxon']['name'].replace(' ','_')
                        #obs['observation_photos'] seems syn to obs['photos']
                        # the results from either (photos or obs_photos) is a list
                        obsImages = obs['photos']
                        writer.writerow([userName, f'{taxonName}_{len(obsImages)}'])


                        for i, obsImg in enumerate(obsImages):
                            squareImgUrl = obsImg['url']
                            fullImgURL = squareImgUrl.replace('square','large')
                            fileName = f'{taxonName}_{userName}_{i + 1}.jpg'

                            file = requests.get(fullImgURL)


                            dbx.files_upload(file.content, f'/{fileName}')


                            print(fileName)

                            time.sleep(1.3)
                        else:
                            pass
                

print ('Done')


# In[53]:


for userID, userName in userIDs.items(): 
    url = f'https://api.inaturalist.org/v1/observations?identified=true&photos=true&user_login={userID}&updated_since={sinceDate}&order=desc&order_by=created_at'
    resp = requests.get(url=url)
    time.sleep(1.1)
    jsonData = resp.json() # Check the JSON Response Content documentation below
    totResults = jsonData['total_results']
    if totResults > 0:
        whole, decimal = str((totResults / 200)).split('.')
        whole = int(whole)
        if int(decimal) > 0:
            whole += 2
            maxPages = whole

        print (userName)
        print (totResults)
        with open('/users/aidanshaw/python/Files/iNatData/Running_list.csv', 'r') as used_names:
            used_list = pd.read_csv(used_names)
        print (used_list)
        used_dict = list(zip(used_list['user'], used_list['name']))
        print (used_dict)
        
        
        pages = range(1, (maxPages + 1))
        if maxPages > 1 == True:
            for page in pages[:2]:
                print(f'on page {page} of {len(pages)}')
                url = f'https://api.inaturalist.org/v1/observations?identified=true&photos=true&user_login={userID}&iconic_taxa=Plantae&page={page}&per_page=200&&updated_since={sinceDate}&order=desc&order_by=created_at'
                resp = requests.get(url=url)
                jsonData = resp.json() # Check the JSON Response Content documentation below
                results1 = jsonData['results']

                for obs in results1:
                    taxonName = obs['taxon']['name'].replace(' ','_')
                    #obs['observation_photos'] seems syn to obs['photos']
                    # the results from either (photos or obs_photos) is a list
                    obsImages = obs['photos']
                    lst = []
                    running_num = 0
                    for value in used_dict:
                        if userName in value[0]:
                            lst.append(value[1])

                    try:
                        matching = [s for s in lst if f'{taxonName}' in s]
                        print (matching[0])
                        words= matching[0].split('_')
                        maxNum = words[len(words)-1]
                        running_num = int(maxNum)
                        print (running_num)
                    except:
                        running_num = 0
                        print ('new/unused')
                
                    for i, obsImg in enumerate(obsImages):
                        squareImgUrl = obsImg['url']
                        fullImgURL = squareImgUrl.replace('square','large')
                        
                        fileName = f'{taxonName}_{userName}_{i + running_num + 1}.jpg'


                        
                        
                        #urllib.request.urlretrieve(fullImgURL, fileName)
                        print(fileName)

                        time.sleep(1.1)   
                

print ('Done')


# In[ ]:




