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

# DEFINE MAIN FUNCTIONS
#%%

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
    
def update_tables():
    # get non-reduntant lists of types and functions
    types = list(set(all_parts['Type']))
    functions = list(set(all_parts['Function']))
    
    for idx in range(len(types)):
        part_type_ori = types[idx] # keep the original name 
        print('Updating json files for:', part_type_ori)
        
        # change the name to fit file name standards
        types[idx] = types[idx].lower()
        types[idx] = types[idx].replace(' ', '_')
        
        part_type = types[idx]
        json = '../database/scripts/'+ 'type_' + part_type + '.json' #set file path
        
        table_data = all_parts.loc[all_parts['Type']==part_type_ori] # create new table for new types
            
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
        print('Updating json files for:', part_func_ori)
        functions[idx] = functions[idx].lower()
        functions[idx] = functions[idx].replace(' ', '_')
        
        part_func = functions[idx]
        json = '../database/scripts/'+ 'func_' + part_func + '.json'
        
        table_data = all_parts.loc[all_parts['Function']==part_func_ori]
            
        table_data.to_json(json, orient = 'records')
        file = open(json, 'r+')
        contents=file.read()
        file.seek(0, 0)
        file.write('var tabledata='+contents+';')
        file.close()

def create_part(part_info, description):
        
    # get template to be filled with the different data
    template = open('../database/templates/part_template.html', 'r').read()
    
    empty_data = True
    
    temp_template = BeautifulSoup(template, 'html.parser') # make the soup object out of the template html
    # fill header elements
    temp_template.find('h2',{'id':'name'}).string=part_info["Name"]
    temp_template.find('h4',{'id':'code'}).string=part_info["Code"].replace('_s', '*')
    temp_template.find('img', {'id':'icon'})['src']="../images/"+part_info["Type"]+".png"
    
    ptype = temp_template.new_tag('a')
    ptype.string = part_info["Type"]
    ptype.attrs['href'] = "../tables/type_"+part_info["Type"].replace(" ","_")+".html"
    ptype.attrs['id'] = "type"
    temp_template.find('a',{'id':'type'}).replaceWith(ptype)
    
    
    function = temp_template.new_tag('a')
    function.string = part_info["Function"]
    function.attrs['href'] = "../tables/func_"+part_info["Function"]+".html"
    function.attrs['id'] = "function"
    temp_template.find('a',{'id':'function'}).replaceWith(function)

    
    ref=part_info["Publication"]
    first_author=ref.split('.')[0].replace(" ", "")
    if re.search(r'\(\d{4}\)', ref):
        year=re.search(r'\(\d{4}\)', ref).group()[1:-1]
    else:
        year = 2021
    file_name = 'pub_'+first_author+str(year)
    
    pub = temp_template.new_tag('a')
    pub.string = file_name.replace("pub_","")
    pub.attrs['href'] = "../tables/"+file_name+".html"
    pub.attrs['id'] = "publication"
    temp_template.find('a',{'id':'publication'}).replaceWith(pub)
    
    
    # fill data elements. If variables are "-", their corresponding table row will be deleted
    if part_info["DR"] == '-':
        temp_template.find('tr', {'id':'dr'}).decompose()
    else:
        temp_template.find('tr',{'id':'dr'}).findChildren()[1].string=str(part_info["DR"])
        empty_data = False
        
    if part_info["n"] == '-':
        temp_template.find('tr', {'id':'hill'}).decompose()
    else:
        temp_template.find('tr',{'id':'hill'}).findChildren()[1].string=str(part_info["n"])
    
    
    if (part_info["High"] == '-'):
        temp_template.find('tr', {'id':'max'}).decompose()
    else:
        temp_template.find('tr',{'id':'max'}).findChildren()[0].string=measures[part_info["Type"]]
        temp_template.find('tr',{'id':'max'}).findChildren()[1].string=str(part_info["High"])
        temp_template.find('tr',{'id':'max'}).findChildren()[2].string=part_info["Unit"]
        empty_data = False
        
    if (part_info["Low"] == '-'):
        temp_template.find('tr', {'id':'min'}).decompose()
    else:
        temp_template.find('tr',{'id':'min'}).findChildren()[1].string=str(part_info["Low"])
        temp_template.find('tr',{'id':'min'}).findChildren()[2].string=part_info["Unit"]
    
    if part_info["Km"] == '-':
        temp_template.find('tr', {'id':'k'}).decompose()
    else:
        temp_template.find('tr',{'id':'k'}).findChildren()[1].string=str(part_info["Km"])
        temp_template.find('tr',{'id':'k'}).findChildren()[2].string=part_info["Km Unit"]
        empty_data = False
        
    if part_info["Strain"] == '-':
        temp_template.find('tr', {'id':'strain'}).decompose()
    else:
        temp_template.find('tr',{'id':'strain'}).findChildren()[1].string=part_info["Strain"]
        
    if part_info["Plasmid"] == '-':
        temp_template.find('tr', {'id':'plasmid'}).decompose()
    else:
        temp_template.find('tr',{'id':'plasmid'}).findChildren()[1].string=part_info["Plasmid"]
        
    if part_info["ori"] == '-':
        temp_template.find('tr', {'id':'origin'}).decompose()
    else:
        temp_template.find('tr',{'id':'origin'}).findChildren()[1].string=part_info["ori"]
        
    if part_info["Resistance"] == '-':
        temp_template.find('tr', {'id':'resistance'}).decompose()
    else:
        temp_template.find('tr',{'id':'resistance'}).findChildren()[1].string=part_info["Resistance"]
    
    # fill the reference section at the end of the page
    temp_template.find('div',{'id':'referencing'}).p.string=part_info["Publication"]
    doi=temp_template.new_tag('a')
    doi.string = part_info["doi"]
    doi.attrs['href']=part_info["doi"]
    temp_template.find('div',{'id':'referencing'}).append(doi)
    
    # recover the previous description of the page if there was one
    temp_template.find('div', {'id':'description'}).replaceWith(description)
    
    # fill sequences (variable number) 
    for seq in part_info[22:]: # get all at the end of the table 
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
    create_sbol(part_info["Construct"], part_info["Code"])
    
    # create the link for the generated image
    temp_template.find('div',{'id':'circuit'}).findChild('img').attrs['src']='../images/part_'+part_info["Code"]+'.png'
    temp_template.find('div',{'id':'circuit'}).findChild('a').attrs['href']='../images/part_'+part_info["Code"]+'.png'
    
    #save all changes to the html file
    html = '../database/parts/'+line["Code"]+'.html'
    new_part = open(html, 'w', encoding='utf-8')
    new_part.write(str(temp_template))
    
    new_part.close()

def update_publications():
    #get a non-redundant list of references
    references=list(set(all_parts['Publication'].to_list()))
    file_names = []
    
    for ref in references:
        
        # get the first author name and the publication year for file naming
        first_author=ref.split('.')[0].replace(" ", "")
        if re.search(r'\(\d{4}\)', ref):
            year=re.search(r'\(\d{4}\)', ref).group()[1:-1]
        else:
            year = 2021
    
        file_name = 'pub_'+first_author+str(year)
        repetition_check = file_name
        i = 1
        while repetition_check in file_names:
            repetition_check = file_name + "_" + str(i)
            i += 1
        file_name = repetition_check
        
        print('Creating table for:',file_name)
        
        
        # set file paths for table data and table page
        json='../database/scripts/'+file_name+'.json'
        html='../database/tables/'+file_name+'.html'
        
        table_data = all_parts.loc[all_parts['Publication']==ref]               
        
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


# CREATE AND UPDATE PART PAGES
#%%

if not new_parts.empty: #make sure that the table is not empty (if it is, just update the tables)
    
    redundant = new_parts["Code"].isin(all_parts["Code"])
    redundant_indexes = new_parts.index[redundant[redundant].index.values] #get the redundant indexes
    redundant_parts = new_parts[redundant]
    new_parts = new_parts.drop(redundant_indexes)
    
    for index, line in new_parts.iterrows():
        
        prev_description = ""
        
        print('Creating part page for:', line["Name"], " - " , line["Code"])
        create_part(line, prev_description)
    
    for index, line in redundant_parts.iterrows():
        
        html = '../database/parts/'+line["Code"]+'.html'
        
        previous = open(html, 'r', encoding='utf-8').read()
        previous_soup = BeautifulSoup(previous, 'html.parser')
        prev_description = previous_soup.find('div', {'id':'description'})
        
        print('Overwriting data on part page for:', line["Name"], " - " , line["Code"])
        create_part(line, prev_description)
        

    

# UPDATE "ALL PARTS" TABLE AND SEARCH BASE
#%%

# update and save all_parts.csv

if not new_parts.empty:
    all_parts = all_parts.append(new_parts, sort=False).reset_index(drop=True)
    redundant_indexes = all_parts.index[redundant[redundant].index.values]
    all_parts = all_parts.drop(redundant_indexes)

all_parts = all_parts.sort_values('Publication')

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


# UPDATE TABLES JSON FILES
#%%
update_tables()

# UPDATE PUBLICATIONS TABLES
#%%

#update_publications()