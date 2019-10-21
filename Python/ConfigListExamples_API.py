import requests, json
from getpass import getpass
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

disable_warnings(category=InsecureRequestWarning)

'''
In these examples, we have a list that contains some numerical values.  The values should always be that "value 2" is
1000 larger than "value 1", "value 3" would be 2000 larger than "value 1", and "value 3" would be 3000 larger than 
"value 1".  Each time need another "thing", you need a new a 4 new values to apply across your devices.

This list includes the columns with the header named as follows:
List Column Name:   API Identifier:
value_1             $value_1
value_2             $value_2
value_3             $value_3
value_4             $value_4

Below will show how to do the following:
1) Get the config list ID using the config_list/index API call.  You don't really need to do this every time because
once you have your list ID, it is just a static field in the other API calls for that list.

2) Get the values, per row, for your list and iterate through them.  In this example, we are finding the next
available value by looking at all the values for the column "value_1" and then just doing the basic arithmetic to get
the other 3 values.

3) Create a new row with the next values you want to add to the config list to use for your your "thing".

4) Shows you how to get the list row ID based on searching all the rows in a list for a specific value.  
This is important if you want to make changes or delete a specific row in a list.  Note that each row from every 
list in NetMRI is unique, meaning the row ID is not list specific.  So if you make a change to a row 
(like the final example of deleting a row), you won't need the config list ID.

5) Show you how to delete the row based on the row ID you obtained via the previous config list row search

'''

##################################################################################################################
# Set up some "global" variables used throughout this script
##################################################################################################################

api_user = "someusername"
password = getpass("Enter your Infoblox password: ")
session = requests.Session()
base_url = "https://netmri.yoursite/api/3.3/"

##################################################################################################################
# Index all of your config lists so that you can get the list ID you want to work with.
##################################################################################################################

index_uri = "config_lists/index"
index_response = session.get(base_url + index_uri, verify=False, auth=(user, password))
index = json.loads(index_response.text)

for item in index['config_lists']:
    print(item['id'], item['name'])

##################################################################################################################
# Iterate through all the rows in the specific list, do something with the data
##################################################################################################################

row_uri = "config_lists/rows"
row_querystring = {"id": "27", "limit": "100"}
row_response = session.get(base_url + row_uri, params=row_querystring, verify=False, auth=(user, password))
rows = json.loads(row_response.text)

value_list = []
for row in rows['rows']: # Looping through each row of config list for dict key 'rows'
    value_list.append(int(row['value_1'])) # Appending value of column named 

value1 = ""
value_list.sort()
print(value_list)
for val in range(value_list[0], value_list[-1] + 1): # Assuming list should be in numerical order, find missing value
    if val not in value_list: # if missing value, fill it in instead of going to end of list for next available
        value1 = val
        value2 = value1 + 1000
        value3 = value1 + 2000
        value4 = value1 + 3000
        print(value1, value2, value3, value4)
        break

if not value1: # if NOT missing value, get next value after last value at to end of list.
    value_list.sort()

    value1 = int(value_list.pop(-1)) + 1
    value2 = value1 + 1000
    value3 = value1 + 2000
    value4 = value1 + 3000

    print(value1, value2, value3, value4)

##################################################################################################################
#  Below will actually create a new row with the next chosen BGP ASN obtained from the above script sequence.
##################################################################################################################

create_row_uri = "config_lists/create_row"
create_row_args = {'id': '10','$value_1': str(value1), '$value_2': str(value2), '$value_3': str(value3), '$value_4': str(value4)}

create_row_response = session.post(base_url + create_row_uri, params=create_row_args , verify=False, auth=(api_user, password))
create_row_json = json.loads(create_row_response.text)
print(json.dumps(create_row_json))


##################################################################################################################
#  Below is for searching rows for a specific string (BGP ASN), in this case represented by "value_search_string"
##################################################################################################################

value_search_string = '1111' # This value could come from user input or another source other than static string.
search_row_uri = "config_lists/search_rows"
search_row_querystring = {'id': '10', '$value_1': value_search_string}

search_row_response = session.get(base_url + search_row_uri, params=search_row_querystring, verify=False, auth=(api_user, password))
search_row_json = json.loads(search_row_response.text)
for i in search_row_json['list_rows']:
    row_id = i['id']

##################################################################################################################
#  Below will delete a row based on "row_id" that it obtained via the above list search.
##################################################################################################################

destroy_row_uri = "config_lists/destroy_rows"
destroy_row_arg = {'list_row_id': row_id} # "row_id" value obtained from previous config list search.

destroy_row_response = session.post(base_url + destroy_row_uri, params=destroy_row_arg, verify=False, auth=(api_user, password))
destroy_row_json = json.loads(destroy_row_response.text)
print(json.dumps(destroy_row_json))
