# ImapSync_Enhanced_logs

This script allow you to extract only some informations from the log files produced by [Imapsync](https://github.com/imapsync/imapsync).
Those informations are : 
- The account name
- The amount of synced folders
- The amount of synced messages
- The size
- The amount of errors
- Wich messages get error while being synchronized

## Requirements

You'll need python 3.xx or higher installed on your computer 
You'll also need the library pandas, which you can install with this command:
```
pip install pandas
```

## How to execute

First you'll need to clone the main branch of this repository.

### On windows

Just execute the Start.bat file, it will automatically install the dependency of the program and then execute it.

### On Linux

You'll need to open a terminal in the folder where the code is stored.
The file need to be executable so launch this command :
``` 
chmod u+x Start.sh 
```
And the this one to execute the file :
``` 
./Start.sh 
```
it will automatically install the dependency of the program and then execute it.

## How to use

Once you have launched the program. You'll need to enter the path of the logs' folder and where to save the output.

In both cases you can either use this format :
````
C:\path\to\your\logs
````
or this one :
````
/path/to/your/logs
````

Then the program analyse your logs, it can take time depending on the number of synchronized account.

and then you can find the resume in two format either CSV or HTML.
Same for the errors files

you can find them with those path :
````
C:\the\path\you\gave\before\resume\resume_logs.html
````
or 
````
/the/path/you/gave/before/resume_logs.html
````

You can open the HTML resume with you favorite browser.

