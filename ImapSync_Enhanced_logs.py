import os, csv, pandas as pd


def open_logs(path, file):
    """open the logs file and return the statistics part of the file in a list, all the errors encourtered if they exist and the account name"""

    with open(f'{path}/{file}', encoding='utf-8') as f:
        logs = f.read()
    #ici on isole la partie statistics
    tmp = logs.split("++++ Statistics" )[1]
    tmp = tmp.split("\n")
    Stats = []
    for a in tmp:
        if ":" in a:
            Stats.append(a.split(":", 1))
    Stats = Stats[:28]
    compte = file.split('_')[7]

    #ici on isole la partie des erreurs s'il y en a
    Errors = []
    if "errors encountered" in logs :
        tmp = logs.split("++++ Listing" )[2] #indice 2 car il y a une fois listing pour les dossiers dans les logs
        tmp = tmp.split("\n")
        Errors = []
        for a in tmp:
            if ":" in a:
                Errors.append([a])
        save_errors_in_CSV(Errors, compte, path)


    return Stats, Errors, compte

def save_resume_in_CSV(resume, path):
    """
    Save the condensed log in a csv.
    if the file doesn't exist already, it will be created 
    """
    if not os.path.isfile(f'{path}/resume/resume_logs.csv'):
        with open(f'{path}/resume/resume_logs.csv', 'w', encoding='UTF8', newline='' ) as f :
            writer = csv.writer(f)
            writer.writerow(["compte","dossiers synchronisés","message synchronisés","taille","erreurs de synchronisation"])
    with open(f'{path}/resume/resume_logs.csv', 'a+', encoding='UTF8', newline='') as f :
        writer = csv.writer(f)
        writer.writerow(resume)

    
def save_errors_in_CSV(Errors, compte, path):
    """
    Crrate a new file with all the errors found during the transfert of the account
 
    """
    
    with open(f'{path}/resume/errors/{compte}_errors.csv', 'w', encoding='UTF8', newline='' ) as f :
            writer = csv.writer(f)
            writer.writerows(Errors)
    a = pd.read_csv(f'{path}/resume/errors/{compte}_errors.csv')
    a.to_html(f'{path}/resume/errors/html/{compte}_errors.html', escape=False)

    


    
def data_generation(stats, Errors,  compte):
    sync_folders = stats[3][1]
    sync_messages = stats[4][1]

    size = stats[15][1]
    size = size.split(" ")[2][1:] +" "+ size.split(" ")[3][:3] #taille GiB

    if Errors:
        #on verifie si la liste des erreurs est vide ou non. 
        errors = f'\u274C {len(Errors)} détectées, visible dans le <a href="./errors/html/{compte}_errors.html">fichier erreur</a>'
    else:
        errors = f'\u2705 aucune erreur détectée'

    return [compte,sync_folders,sync_messages,size, errors]

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
        print('le dossier existe déjà')
    return file_list




path = input("entrez le chemin jusqu'au dossier de log \n")
file_list = list_files(path)

for file in file_list:
    logs = open_logs(path, file)
    out = data_generation(logs[0], logs[1], logs[2])
    save_resume_in_CSV(out, path)
    print(f'fait pour {logs[2]}')


a = pd.read_csv(f'{path}/resume/resume_logs.csv')
a.to_html(f'{path}/resume/resume_logs.html', escape=False)
