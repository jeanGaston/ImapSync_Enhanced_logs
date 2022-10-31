import datetime
import os, csv, pandas as pd



def open_logs(path, file):
    """open the logs file and return the statistics part of the file in a list, all the errors encourtered if they exist and the account name"""

    with open(f'{path}/{file}', encoding='utf-8') as f:
        logs = f.read()
    #here we isolate the statistical part
    tmp = logs.split("++++ Statistics" )[1]
    tmp = tmp.split("\n")
    Stats = []
    for a in tmp:
        if ":" in a:
            Stats.append(a.split(":", 1))
    Stats = Stats[:28]
    account = file.split('_')[7]

    #here we isolate the part of the errors if there are any
    Errors = []
    if "errors encountered" in logs :
        tmp = logs.split("++++ Listing" )[2] #index 2 because there is once "listing" for the folders in the logs
        tmp = tmp.split("\n")
        Errors = []
        for a in tmp:
            if ":" in a:
                Errors.append([get_date_and_time(),a])
        save_errors_in_CSV(Errors, account, path)


    return Stats, Errors, account

def save_resume_in_CSV(resume, path):
    """
    Save the condensed log in a csv.
    if the file doesn't exist already, it will be created 
    """
    if not os.path.isfile(f'{path}/resume/resume_logs.csv'):
        with open(f'{path}/resume/resume_logs.csv', 'w', encoding='UTF8', newline='' ) as f :
            writer = csv.writer(f)
            writer.writerow(["Date","Account","Synchronized folder","Synchronized messages","Size","Synchronization errors"])
    with open(f'{path}/resume/resume_logs.csv', 'a+', encoding='UTF8', newline='') as f :
        writer = csv.writer(f)
        writer.writerow(resume)

    
def save_errors_in_CSV(Errors, account, path):
    """
    Create a new file with all the errors found during the transfert of the account
 
    """
    
    with open(f'{path}/resume/errors/{account}_errors.csv', 'w', encoding='UTF8', newline='' ) as f :
            writer = csv.writer(f)
            writer.writerow(['Date', 'Error'])
            writer.writerows(Errors)
    save_in_html(f'{path}/resume/errors/', f'{account}_errors.csv', './css_style/style_css_error.txt',f'html/{account}_errors.html')

    
def save_in_html(path,file_name,style_sheet,out_file_name):
    """
    save the file in html with the specified style sheet applied to it
    """
    a = pd.read_csv(f'{path}/{file_name}')
    #open the css sheet
    with open(style_sheet, 'r') as myfile:
        style = myfile.read()

    html = """<html><head></head>{1}<div>{0}</div></html>""".format(a.to_html(escape=False, justify='center', table_id='tab'),style)
    #save the html file
    with open(f'{path}/{out_file_name}', 'w', encoding='UTF8' ) as f :
        f.write(html)

    
def data_generation(stats, Errors,  account, path):
    sync_folders = stats[3][1]
    sync_messages = stats[4][1]

    size = stats[15][1]
    size = size.split(" ")[2][1:] +" "+ size.split(" ")[3][:3] #size in GiB

    if Errors:
        #Check if the error list is empty or not. 
        errors = f'\u274C {len(Errors)} errors detected, you can see them in the <a href="{path}/resume/errors/html/{account}_errors.html">errors file</a>'
    else:
        errors = f'\u2705 no error detected'

    return [get_date_and_time(), account,sync_folders,sync_messages,size, errors]

def list_files(basepath):
    """
    list all the file in the directory
    create the folder if it doesn't exist
    """
    file_list = []
    for entry in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, entry)):
            file_list.append(entry)
    
    try:
        os.makedirs(f'{path}/resume/errors/html')
    except:
        print('the folder already exist')
    return file_list

def get_date_and_time():
    """
    get the current time 
    """
    now_time = datetime.datetime.now()
    return now_time.strftime("%d/%m/%Y %H:%M:%S")



path = input("Please ente the path to the log folder \n")
file_list = list_files(path)

for file in file_list:
    logs = open_logs(path, file)
    out = data_generation(logs[0], logs[1], logs[2], path)
    save_resume_in_CSV(out, path)
    print(f'Done for {logs[2]}')

save_in_html(f'{path}/resume/', 'resume_logs.csv', './css_style/style_css.txt', 'resume_logs.html')



print(f'You can view the resume in this file : {path}/resume/resume_logs.html')
