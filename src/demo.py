#
# Filename: legit_issues.py
# Date: 2023-06-27
# Updated: 2023-09-06
# Author: Alan Bitterman
# Description: Sample Legit Issues API Report
#
# Linux/Mac Requirements:
#   python3
#   jq  	https://stedolan.github.io/jq/
#   export TOKEN environment variable for the Legit tenant API token specified
#
# Usage:
#   1.  Set TOKEN environment variable for the Legit tenant specified prior to running script
#       $ export TOKEN="lgt_##############################"
#
#   2.  Set Script Variables as required; minimum change the TENANT variable.
#        x. Set the tenant name value in base_url variable later in code ...
#	base_url="https://[tenant_name].legitsecurity.co/api/v1.0/"
#
#   3.  Run script ...
#       $ chmod +x legit_issues.py
#       $ python3 legit_issues.py			# All Issues ...
#
#       Command Line Arguements
#       $ python3 legit_issues.py [TYPE] [Product-Unit(s)]
#       $ python3 legit_issues.py Secret
#       $ python3 legit_issues.py Secret Active_Repos
#       $ python3 legit_issues.py "Secret" "Active_Repos Mine"       # Multiple Product Unit Values ...
# 	$ python3 legit_issues.py "" "Active_Repos"		     # All Issue Types per Product Unit(s) ...
#       $ python3 legit_issues.py "" "Active_Repos Mine"             # All Issue Types per Product Unit(s) ...
#
# Future Todos:
#   x.  Add sortable column headers
#   x.  Add column data filters ???
#   x.  As always, add more variables, modules and checks :)
#
# Code disclaimer information ...
# This document contains programming examples.
#
# Legit Security grants you a nonexclusive copyright license to use all programming code examples
# from which you can generate similar function tailored to your own specific needs.
#
# All sample code is provided by Legit Security for illustrative purposes only. These examples have
# not been thoroughly tested under all conditions. Legit Security, therefore, cannot guarantee or
# imply reliability, serviceability, or function of these programs.
#
# All programs contained herein are provided to you "AS IS" without any warranties of any kind.
# The implied warranties of non-infringement, merchantability and fitness for a particular purpose
# are expressly disclaimed.
#
##########################################################

import json
import requests
import os.path

import webbrowser
import time
from datetime import datetime

import sys

#
# App Variables - Update tenant name ...
#
token=""		# uses TOKEN environment variable value ...
token="lgt_11e33e1d96e54572998abdf757ff77f6813dadf65008d154"
base_url="https://alan.legitsecurity.co/api/v1.0/"	# replace tenant name with respective one for your org
#base_url="https://demo5.legitsecurity.net/api/v1.0/"
params=""		
pnum=1			# Starting pageNumber value ...
psize=100		# Max pageSize value hard coded in the Tenant, contact Legit Engineering for override ...
err=""
issue_types=["Misconfiguration","Secret","IaC","Incident","Controls","Pipeline","Dependencies","Sast","VulnerableAssets","Other"]		# Valid List of Legit Issue Types ...

#
# Get TOKEN from Environment Variable for Legit API Authentication Header ...
#
#try:
#        token=os.environ['TOKEN']
#except KeyError:
#        print("Error: Missing TOKEN envionment variable value for Legit API token ...")
#        sys.exit()
headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer '+token}

#
# Files ...
#
source_json_file="api.json" 		# Issues JSON generated source file 
json_file="api2.json"			# Issues JSON file formated for reporting 
html_file="api.html"			# Report HTML file
csv_file="api.csv"			# Download CSV file

#
# Query Variables ...
#
type=""					# Issue Type ...
#type="IaC"   				# Hard Coded Value ...
pus=""					# Product Unit(s), for multiple values, use space delimiter ..
pus_list=[]				# Product Units URL Query string built by code ...
product_list=[]				# Result from Product Units API ...

# 
# Command Line Arguements Override ...
#

#
# Issue Type ...
#
try:
	type=sys.argv[1]
except:
	err="Missing argv[1]"
print("Issue Type: "+type)

#
# Validate Issue Type ...
#
if type:
	if type not in issue_types:
		print ("Error: "+type+" is not a valid issue type, valid types are: \n"+str(issue_types))
		sys.exit()

# 
# Product Unit(s) ...
#
try:
        pus=sys.argv[2]
except IndexError:
        err="Missing argv[2]"   # print("Missing Product Unit")
print("Product Unit(s): "+pus)

# 
# Get Product Units List ...
#
product_list=[]
pnum=1
if ( pus ):
	while pnum < 100:
		url = f""+base_url+"products?pageSize="+str(psize)+"&pageNumber="+str(pnum)
		#print(url)

		response = requests.get(url, params=params, headers=headers)
		# print(response.text)
		d = response.json()

		if (d): 
			#print(d)
			for o in d:
				#print(o["name"])
				product_list.append(o["name"])
				continue
		#print(product_list)
		break

	#
	# Validate Product Unit Names ...
	#
	pus_list=list(pus.split(" "))
	for s in pus_list:
		if s not in product_list:
			print("Error: "+s+" is not a valid product unit, valid product units are: \n"+str(product_list))
			sys.exit()

	# 
	# Build Product Units URL Param String ...
	#
	pus="&productUnits=".join(pus_list)
	#print("Product Unit(s) URL Query String: "+pus)

# 
# Output source JSON file ...
#
file1 = open(source_json_file, 'w')

#
# Loop thru pageNumbers/pageSize to get issues ...
#
url = ""
pnum = 1
while pnum < 1000:
	#url = f"https://alan.legitsecurity.co/api/v1.0/issues?pageSize="+str(psize)+"&pageNumber="+str(pnum)+"&issueType="+type
	if ( pus ):
		url = f""+base_url+"issues?pageSize="+str(psize)+"&pageNumber="+str(pnum)+"&status=Open&issueType="+type+"&productUnits="+pus
	else:
		url = f""+base_url+"issues?pageSize="+str(psize)+"&pageNumber="+str(pnum)+"&issueType="+type
	#print(url)

	response = requests.get(url, params=params, headers=headers)     
	# print(response.text)
	d = response.json() 

        # Local Output ...
	#print(d)
	#for o in d:
		#print(o)
        	#print(o["id"])
        	#print(o["policyName"])
        	#print(o["title"])
        	#print(o["description"])
        	#print(o["detectedAt"])
        	#print(o["status"])
        	#print(o["type"])
        	#print(o["severity"])
        	#print("-----------------------------------")

	pnum = pnum + 1		# Increment pageNumber ...

        #
        # Break loop if null response ...
        #
	if ( d ):
		#
		# Output JSON response text ...
		#
		file1.write(response.text)
		file1.write('\n')
		print(url)
		continue
	break

file1.close()

#
# Modify Source JSON file format for Report Processing (One Object per Line) ...
#
sd = os.system('cat '+source_json_file+' | jq ".[]" | jq -s > '+json_file+'')
print('Format JSON for HTML Report ... '+str(sd))

#
# todo: add some verification logic here ...
#
print("Done with Data Generation ...")

#############################################################################################
## Report Variables ...

ts=time.time()			 	#print(ts)
dt=str(datetime.fromtimestamp(ts, tz=None)).replace(' ','T')
#dt=`date "+%Y-%m-%dT%H:%M:%SZ"`	
print(dt)

#
# Report Fields ...
# Nested Key Values are delimited with a period, i.e. origin.originName, payload.occurrencesCount
#
rpt_fields=["id","policyName","title","description","origin.originName","productUnits","detectedAt","status","type","severity","integration.name","assignedUser","comments","lastUpdateTime"]

#
# For the JSON conversion, need to format special columns; nested array values, nested objects, datatype conversions str(), etc.
#
td_fields=["['id']","['policyName']","['title']","['description']","['origin']['originName']","['productUnits']","['detectedAt']","['status']","['type']","['severity']","['integration']['name']","['assignedUser']","['comments']","['lastUpdateTime']"]

#
# Loop Variables ...
#
column_headers=""		# HTML Table Column Header values ...
csv_headers=""			# CSV Column Header values ...
td_str=""			# HTML Table Row and Cell string to be eval() ...
csv_str=""			# CSV Line Columns string to be eval() ...
delim=""			# td_str delimiter ...
delim2=""			# CSV Column Header delimiter ...
delim3=""			# csv_str delimiter ...
list=["id", "title", "description", "status", "type", "severity"]  	# no column/cell modification list ...

#
# Loop through Report Fields and build header and eval strings ...
# 
for x in range(len(rpt_fields)):
	#print(rpt_fields[x])
        #
        # Build out HTML and CSV column header strings ...
        #
	column_headers=column_headers+"<th>"+rpt_fields[x]+"</th>\n"
	csv_headers=csv_headers+delim2+'"'+rpt_fields[x]+'"'
        #
        # Build out HTML row/cell and CSV column value strings to be eval'd ...
        #
	if (rpt_fields[x] == "policyName"):		# for a decent viewable HTML table, add style to policyName or others ...
		td_str=td_str+delim+"'<td style=\"word-break:break-all;\">'+x"+td_fields[x]+"+'</td>'"
		csv_str=csv_str+delim3+"x"+td_fields[x]
	elif rpt_fields[x] in list:
		td_str=td_str+delim+"'<td>'+x"+td_fields[x]+"+'</td>'"
		csv_str=csv_str+delim3+"x"+td_fields[x]
	else:	 
		td_str=td_str+delim+"'<td>'+str(x"+td_fields[x]+")+'</td>'"
		csv_str=csv_str+delim3+"str(x"+td_fields[x]+").replace('\"','\"\"')"	# For CSV, double up on the inside quotes
	delim="+"
	delim2=","
	delim3='+"\\",\\""+'

#
# Wrap double quotes around string ...
#
csv_str='"\\""+'+csv_str+'+"\\""'

##debug##print(csv_str)#print('\n')
##debug##print(td_str)#print('\n')

#########################################
## No Changes required below this line ##
#########################################

##############################################################################
# 
# Report HTML Output ...
#
print("Building HTML Report w/CSV Download, please wait ...")

#
# Open Files for Output ...
#
file1 = open(html_file, 'w')
file2 = open(csv_file, 'w')

#
# Write HTML Header ...
#
file1.write("""<html>
<head>
<title>Legit Issue Report</title>
<style>
#customers {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 10pt;
  border-collapse: collapse;
  width: 100%;
}
#customers td, #customers th {
  border: 1px solid #ddd;
  padding: 4px;
}
#customers tr:nth-child(even){background-color: #f2f2f2;}
#customers tr:hover {background-color: #ddd;}
#customers th {
  padding-top: 2px;
  padding-bottom: 2px;
  text-align: left;
  background-color: #04AA6D;
  color: white;
}
</style>
</head>
<body>
<center>
<table><tr><td style=\"font-weight: bold;font-size: 16pt;text-align:center;\">
Legit Issues Report - """+dt+"""
</td></tr><tr><td align=center>
Issue Types: """+type+"""  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Product Units: """+pus+""" 
</td></tr><tr><td align=center>
&nbsp;&raquo;&nbsp; <a href="""+csv_file+""" target="_blank">Download CSV</a> &nbsp;&laquo;&nbsp;
</td></tr></table>
<table id=\"customers\"><tr><th>#</th>""")

# 
# Report Table Column Headers ...
#
file1.write(column_headers)
file1.write("</tr>\n")

#
# CSV Header ...
#
file2.write(csv_headers)
file2.write("\n")

#  
# Opening Report Formatted JSON file ...
#
f = open(json_file)
data = json.load(f)  	# returns JSON object as a dictionary
f.close()		# close file

#
# Report Table Line Items ...
#
# Iterating through the json list
i = 1
for x in data:
	# Item Number ...
	file1.write('<tr><td>'+str(i)+'</td>\n')
	# Tests ...
	#print(x['id'])
	#file1.write('<td>'+x['id']+'</td>\n') 
	#file1.write('<td>'+x['origin']['originName']+'</td>\n')  
	#
	# HTML Table Row and Cell string eval ...
	#
	tmp_str=eval(td_str)
	file1.write(tmp_str)
	file1.write('</tr>\n')
	#
	# CSV string eval and CSV clean-up, replaced linefeeds ... 
	#
	tmp2_str=eval(csv_str)
	tmp2_str=tmp2_str.replace('\n', ' ')
	file2.write(tmp2_str)
	file2.write('\n')
	i = i + 1		# Item Number counter ...

file1.write("</table>")

#
# HTML Footer ...
#
file1.write("""&copy; 2023 Legit Security -- All rights reserved
</center>
</body>
</html>""")

file1.close()
file2.close()

#
# Clean-Up ...
#
if os.path.exists(source_json_file):
	os.remove(source_json_file)
if os.path.exists(json_file):
        os.remove(json_file)

#
# Open Report, html_file ...
# 
import webbrowser
# MacOS
chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
# Windows
# chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
# Linux
# chrome_path = '/usr/bin/google-chrome %s'

webbrowser.get(chrome_path).open(html_file)

# 
# The End is Here ...
#
print("HTML File: "+html_file)
print("CSV File: "+csv_file)
print("Done ...")


