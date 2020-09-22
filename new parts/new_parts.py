# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 22:03:37 2020

@author: Felipe

script still in progress. Major sections of code still need to be made into functions and error traps should be included.
"""

# IMPORT LIBRARIES

from bs4 import BeautifulSoup #for HTML parsing
import os #for file reading, renaming, and moving
import pandas as pd #to read/write csv and json files
import regex as re #for string parsing
import matplotlib.pyplot as plt #for dnaplotlib to function
import dnaplotlib as dpl #to plot circuit images in part pages

# FUNCTION FOR PART PAGE CIRCUIT IMAGES
def create_sbol(construct, name):
    
    # get the circuit string and transform it into an iterable list
    # structure: <part 1 type>:<part 1 name>,<part 2 type>:<part 2 name>
    plasmids = construct.split('//') # // separates different plasmids
    
    for idx in range(len(plasmids)):
        plasmids[idx] = plasmids[idx].split(',') # , separates different parts in the same plasmid
    
    designs = []
    
    sp = {'type':'EmptySpace', 'name':'S1', 'fwd':True} # dnaplotlib tag for empty spaces
    
    max_length = len(max(plasmids, key=len)) # get the length (in parts) of the biggest plasmid
    
    # set font size and line width based on how much the image will be shrinked
    font_size = 20/max([len(plasmids), max_length/4]) 
    line_size = 2/len(plasmids)
    
    d = 0
    for plasmid in plasmids:
        designs.append([])
        for part in plasmid: #set offset for parts names
            if plasmid.index(part) % 2 == 0:
                y_offset = 20
            else:
                y_offset = -15
            part = part.replace(' ','') # handle spaces in circuit string
            designs[d].append(sp)
            designs[d].append({'type':part.split(':')[0], 'name':part.split(':')[1], 'fwd':True, 'opts':{'label':part.split(':')[1], 'label_size':font_size, 'label_y_offset':y_offset}})
        d += 1
    
    dr = dpl.DNARenderer(linewidth=line_size) # dnaplotlib renderer object
    
    if len(designs) > 1: # making subplots only makes sense if there are multiple plasmids   
        fig, axs = plt.subplots(len(designs))
        
        for idx in range(len(designs)): # use dnapltlib's standard drawing commands (got from their github)
            start, end = dr.renderDNA(axs[idx], designs[idx], dr.SBOL_part_renderers())
            axs[idx].set_xlim([start, end])
            axs[idx].set_ylim([-25,25])
            axs[idx].set_aspect('equal')
            axs[idx].set_xticks([])
            axs[idx].set_yticks([])
            axs[idx].axis('off')
        fig.set_figwidth(0.75*max_length)
    else:
        fig = plt.figure()
        ax = plt.axes()
        start, end = dr.renderDNA(ax, designs[0], dr.SBOL_part_renderers())
        ax.set_xlim([start, end])
        ax.set_ylim([-25,25])
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.axis('off')
        
    # save figure with appropriate name and close everything
    fig.savefig('../database/images/part_'+name+'.png')
    plt.close('all')
        
# INITIALIZATION VARIABLES
#%%

# Dictionary sets the alternative names for the "High" value (for parts that lack dynamic behaviour).
measures = {'Regulated Promoters':'High',
            'Constitutive Promoters':'Strength',
            'RBS':'Strength',
            'Reporters':'None',
            'Terminators': 'Strength',
            'Insulators':'None',
            'Riboregulators':'High',
            'CRISPR':'None',
            'Degradation Tags':'Strength',
            'Post-Translational':'Efficiency',
            'Recombinases':'None',
            'Origins of Replication':'Copy Number'}

# import parts tables
new_parts = pd.read_csv('new_parts.csv', delimiter=';', encoding='utf-8')
all_parts = pd.read_csv('all_parts.csv', delimiter=";", encoding='utf-8')


#FIND TRULY NEW PARTS
#%% 
print()
redundant = new_parts["Code"].isin(all_parts["Code"])
new_parts = new_parts.drop(new_parts.index[redundant[redundant].index.values])


# UPDATE TABLES JSON FILES
#%%

# get non-reduntant lists of types and functions
types = list(set(new_parts['Type']))
functions = list(set(new_parts['Function']))

for idx in range(len(types)):
    part_type_ori = types[idx] # keep the original name 
    print('Creating json files for:', part_type_ori)
    
    # change the name to fit file name standards
    types[idx] = types[idx].lower()
    types[idx] = types[idx].replace(' ', '_')
    
    part_type = types[idx]
    json = '../database/scripts/'+ 'type_' + part_type + '.json' #set file path
    if os.path.exists(json):
        json_literal = open(json, 'r').read()
        json_good = json_literal[14:-1] # remove the "var tabledata=" part from the json files (they are not really json files)
        table_data = pd.read_json(json_good, orient='records')
        table_data = table_data.rename(columns={measures[part_type_ori]:'High'}) # rename columns to fit the general name
        table_data = table_data[new_parts.columns] # organize the columns
        table_data = table_data.append(new_parts.loc[new_parts['Type']==part_type_ori], sort=False) # append new data
    else:
        table_data = new_parts.loc[new_parts['Type']==part_type_ori] # create new table for new types
        
    table_data = table_data.rename(columns={'High':measures[part_type_ori]}) # reset the "High" column name
    
    # save table to json and generate the script file 
    table_data.to_json(json, orient = 'records')
    file = open(json, 'r+')
    contents=file.read()
    file.seek(0, 0)
    file.write('var tabledata='+contents+';')
    file.close()

# do the same thing as before, but for part functions
for idx in range(len(functions)):
    part_func_ori = functions[idx]
    print('Creating json files for:', part_func_ori)
    functions[idx] = functions[idx].lower()
    functions[idx] = functions[idx].replace(' ', '_')
    
    part_func = functions[idx]
    json = '../database/scripts/'+ 'func_' + part_func + '.json'
    if os.path.exists(json):
        json_literal = open(json, 'r').read()
        json_good = json_literal[14:-1]
        table_data = pd.read_json(json_good, orient='records')
        table_data = table_data[new_parts.columns]
        table_data = table_data.append(new_parts.loc[new_parts['Function']==part_func_ori], sort=False)
    else:
        table_data = new_parts.loc[new_parts['Function']==part_func_ori]
        
    table_data.to_json(json, orient = 'records')
    file = open(json, 'r+')
    contents=file.read()
    file.seek(0, 0)
    file.write('var tabledata='+contents+';')
    file.close()
    


# CREATE PART PAGES
#%%

# get template to be filled with the different data
template = open('../database/templates/part_template.html', 'r').read()

for index, line in new_parts.iterrows():
    
    temp_template = BeautifulSoup(template, 'html.parser') # make the soup object out of the template html
    
    html = '../database/parts/'+line["Code"]+'.html'
    
    # check if the part already exists to avoid duplicates (if something has a page but is not on the "all_parts" csv).
    if os.path.exists(html):
        print('Overwriting part page for:', line["Name"])
        # Save the description if page already exists
        previous = open(html, 'r', encoding='utf-8').read()
        previous_soup = BeautifulSoup(previous, 'html.parser')
        prev_description = previous_soup.find('div', {'id':'description'})
    else:
        print('Creating part page for:', line["Name"])
        
    
    empty_data = True
    
    # fill header elements
    temp_template.find('h2',{'id':'name'}).string=line["Name"]
    temp_template.find('h4',{'id':'code'}).string=line["Code"].replace('_s', '*')
    temp_template.find('img', {'id':'icon'})['src']="../images/"+line["Type"]+".png"
    
    ptype = temp_template.new_tag('a')
    ptype.string = line["Type"]
    ptype.attrs['href'] = "../tables/type_"+line["Type"].replace(" ","_")+".html"
    ptype.attrs['id'] = "type"
    temp_template.find('a',{'id':'type'}).replaceWith(ptype) 
    
    function = temp_template.new_tag('a')
    function.string = line["Function"]
    function.attrs['href'] = "../tables/func_"+line["Function"]+".html"
    function.attrs['id'] = "function"
    temp_template.find('a',{'id':'function'}).replaceWith(function)
    
    ref=line["Publication"]
    first_author=ref.split('.')[0].replace(" ", "")
    if re.search(r'\d{4}', ref):
        year=re.search(r'\d{4}', ref).group()
    file_name = 'pub_'+first_author+year
    
    pub = temp_template.new_tag('a')
    pub.string = file_name.replace("pub_","")
    pub.attrs['href'] = "../tables/"+file_name+".html"
    pub.attrs['id'] = "publication"
    temp_template.find('a',{'id':'publication'}).replaceWith(pub)
    
    # fill data elements. If variables are "-", their corresponding table row will be deleted
    if line["DR"] == '-':
        temp_template.find('tr', {'id':'dr'}).decompose()
    else:
        temp_template.find('tr',{'id':'dr'}).findChildren()[1].string=line["DR"]
        empty_data = False
        
    if line["n"] == '-':
        temp_template.find('tr', {'id':'hill'}).decompose()
    else:
        temp_template.find('tr',{'id':'hill'}).findChildren()[1].string=line["n"]
        
    if (line["High"] == '-'):
        temp_template.find('tr', {'id':'max'}).decompose()
    else:
        temp_template.find('tr',{'id':'max'}).findChildren()[0].string=measures[line["Type"]]
        temp_template.find('tr',{'id':'max'}).findChildren()[1].string=line["High"]
        temp_template.find('tr',{'id':'max'}).findChildren()[2].string=line["Unit"]
        empty_data = False
        
    if (line["Low"] == '-'):
        temp_template.find('tr', {'id':'min'}).decompose()
    else:
        temp_template.find('tr',{'id':'min'}).findChildren()[1].string=line["Low"]
        temp_template.find('tr',{'id':'min'}).findChildren()[2].string=line["Unit"]
    
    if line["Km"] == '-':
        temp_template.find('tr', {'id':'k'}).decompose()
    else:
        temp_template.find('tr',{'id':'k'}).findChildren()[1].string=line["Km"]
        temp_template.find('tr',{'id':'k'}).findChildren()[2].string=line["Km Unit"]
        empty_data = False
        
    if line["Strain"] == '-':
        temp_template.find('tr', {'id':'strain'}).decompose()
    else:
        temp_template.find('tr',{'id':'strain'}).findChildren()[1].string=line["Strain"]
        
    if line["Plasmid"] == '-':
        temp_template.find('tr', {'id':'plasmid'}).decompose()
    else:
        temp_template.find('tr',{'id':'plasmid'}).findChildren()[1].string=line["Plasmid"]
        
    if line["ori"] == '-':
        temp_template.find('tr', {'id':'origin'}).decompose()
    else:
        temp_template.find('tr',{'id':'origin'}).findChildren()[1].string=line["ori"]
        
    if line["Resistance"] == '-':
        temp_template.find('tr', {'id':'resistance'}).decompose()
    else:
        temp_template.find('tr',{'id':'resistance'}).findChildren()[1].string=line["Resistance"]
    
    # fill the reference section at the end of the page
    temp_template.find('div',{'id':'referencing'}).p.string=line["Publication"]
    doi=temp_template.new_tag('a')
    doi.string = line["doi"]
    doi.attrs['href']=line["doi"]
    temp_template.find('div',{'id':'referencing'}).append(doi)
    
    # recover the previous description of the page if there was one
    if prev_description:
        temp_template.find('div', {'id':'description'}).replaceWith(prev_description)
    
    # fill sequences (variable number) 
    for seq in line[22:]: # get all at the end of the table 
        if seq == seq:
            seq_data = seq.split(':')
            if seq_data[0] != '':
                name_tag = temp_template.new_tag('h4')
                name_tag.string = seq_data[0]
                letters_tag = temp_template.new_tag('p')
                letters_tag.string = seq_data[1].replace('_^', '<sup>').replace('^_', '</sup>')
                temp_template.find('div',{'id':'sequence'}).append(name_tag)    
                temp_template.find('div',{'id':'sequence'}).append(letters_tag)
    
    # drop the entire table if no data is present
    if empty_data == True:
        temp_template.find('div',{'id':'data'}).findChildren('table')[0].decompose()
    
    # create the circuit image
    create_sbol(line["Construct"], line["Code"])
    
    # create the link for the generated image
    temp_template.find('div',{'id':'circuit'}).findChild('img').attrs['src']='../images/part_'+line["Code"]+'.png'
    temp_template.find('div',{'id':'circuit'}).findChild('a').attrs['href']='../images/part_'+line["Code"]+'.png'
    
    #save all changes to the html file
    new_part = open(html, 'w', encoding='utf-8')
    new_part.write(str(temp_template))
    
    new_part.close()


# UPDATE PUBLICATIONS TABLES
#%%
#get a non-redundant list of references
references=list(set(new_parts['Publication'].to_list()))

for ref in references:
    
    # get the first author name and the publication year for file naming
    first_author=ref.split('.')[0].replace(" ", "")
    if re.search(r'\d{4}', ref):
        year=re.search(r'\d{4}', ref).group()

    file_name = 'pub_'+first_author+year
    print('Creating table for:',file_name)
    
    # set file paths for table data and table page
    json='../database/scripts/'+file_name+'.json'
    html='../database/tables/'+file_name+'.html'
    
    if ref in set(all_parts["Publication"]): # just update the table if the publication is already in the database
        json_literal = open(json, 'r').read()
        json_good = json_literal[14:-1] # remove "var tabledata=" 
        table_data = pd.read_json(json_good, orient='records')
        table_data = table_data[new_parts.columns] # organize data columns
        table_data = table_data.append(new_parts.loc[new_parts['Publication']==ref], sort=False) # append new data
    else:
        table_data = new_parts.loc[new_parts['Publication']==ref]
        tries = 0
        if os.path.exists(json): # handle publications with the same author name and year
            print(json, 'already exists')
            tries += 1
            file_name = file_name+'_'+str(tries)
            json='../database/scripts/'+file_name+'.json'
            while os.path.exists(json):
                print(json, 'already exists')
                tries += 1
                file_name = file_name[:-2]+'_'+str(tries)
                json= '../database/scripts/'+file_name+'.json'
            
    
    # update links to new file name
    json='../database/scripts/'+file_name+'.json'
    html='../database/tables/'+file_name+'.html'
    
    # create/update table data
    table_data.to_json(json, orient = 'records')
    file = open(json, 'r+')
    contents=file.read()
    file.seek(0, 0)
    file.write('var tabledata='+contents+';')
    file.close()
    
    # get the template for table page
    template = open('../database/templates/publications_template.html', 'r').read()
    temp_template = BeautifulSoup(template, 'html.parser')
    
    # fill page title and link to table
    temp_template.find('h2', {'id':'pub_title'}).string = ref
    temp_template.find('script', {'id':'table'})['src']='../scripts/'+file_name+'.json'
    
    if not os.path.exists(html):
        new_part= open(html, 'w', encoding='utf-8')
        new_part.write(str(temp_template))
        new_part.close()
        
# UPDATE "ALL PARTS" TABLE AND SEARCH BASE
#%%

# update and save all_parts.csv
all_parts = all_parts.append(new_parts, sort=False).reset_index(drop=True)
all_parts.to_csv('all_parts.csv', index=False, sep=';', encoding='utf-8-sig')

# set columns that go to search table
search = all_parts[["Name", "Code", "Type", "Regulator", "Lab", "Publication", "Keywords"]]

# Mini Search needs an id column to work
search.insert(0, column='id', value=search.index.values)

# write "json file for search bar"
search.to_json('../database/scripts/search.json', orient='records')
file = open('../database/scripts/search.json', 'r+')
contents=file.read()
file.seek(0, 0)
file.write('var parts='+contents+';')
file.close()