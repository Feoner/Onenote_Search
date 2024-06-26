# Onenote_search
This tool will assist in searching through a Onenote Notebook and look for any sensitve informtaion, such as usernames, passwords, tokens etc.

## Install 
You will need a local copy of the Onenote Notebook.
<br>
 To Download the Notebook locally
  * Open Onenote and select the notebook you will be downloading
  * Click on file and chose "Export" from the left hand menu
  * Under "1. Export Current:" select "Notebook"
  * For "2. Select Format:" chose "PDF
Ensure requirements are installed 
<br>

```
pip install -r requirements.txt
```

<br>

## Usage 
Alter the script to reflect the path of the downloaded pdf and add any patterns that you wish to search for then run the script.
<br>

```
python onenote_search.py
```

<br>
When the script complets it will output multiple formats of the findings.
