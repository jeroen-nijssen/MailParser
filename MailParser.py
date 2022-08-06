from alive_progress import alive_bar
import extract_msg
import os
import time
# import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--FolderToSearch', type=str, help="Specify the location where the .msg files are stored")
parser.add_argument('--searchString', type=str, help="The string which will be searched for")
parser.add_argument('--searchInBody', action='store_true',help="enabling the search in body function")
parser.add_argument('--no-searchInBody', dest='searchInBody', action='store_false', help="disableing the search in body function [default state]")
parser.set_defaults(searchInBody=False)
parser.set_defaults(FolderToSearch=os.getcwd())

args = parser.parse_args()

folder_to_search = args.FolderToSearch
search_item = args.searchString
search_in_body = args.searchInBody

# print(folder_to_search)
# print(search_item)
# print(search_in_body)

def search_msg(fullpath,search_in_body,search_item):
    success = 0
    return_message = "none"

    try:
        msg = extract_msg.Message(fullpath)
    except:
        success= 0
        print(f"Unable to extract {fullpath}")
        raise

    if search_in_body and search_item in msg.body:
        success = 1
        return_message = "Found search item in body"
    
    if search_item in msg.subject:
        success = 1
        return_message = "Found search item in subject"

    if success == 1:
        msg_sender = msg.sender
        msg_date = msg.date
        msg_subj = msg.subject
        msg_message = msg.body

        #display findings within console
        print("Search Item found:")
        print(f"File location: {fullpath}")
        print(f"Search message: {return_message}")
        print("\n\n")
        print(f"Sender:\t\t{msg_sender}")
        print(f"Sent On:\t\t{msg_date}")
        print(f"Subject:\t\t{msg_subj}")
        print(f"Body:\n{msg_message}\n")

        input("Press Enter to continue...")


ext = ('.msg')
files = os.listdir(folder_to_search)
with alive_bar(len(files), force_tty=True) as bar:
    time.sleep(.005)
    for file in files:
        if file.endswith(ext):
            fullpath = os.path.join(folder_to_search,file)
            search_msg(fullpath,search_in_body,search_item)
            bar.title(folder_to_search)
            bar()