You will need Python installed on your system.  
I downloaded it for Windows from here:  
https://www.python.org/downloads/  
Load a command prompt and try:  
`python --version`  
if it shows some form of an error, Python isn't installed sufficiently.  
  
To install required external packages, run  
`pip3 install -r requirements.txt`  
  
Then to extract your mods:  
`python mod_extractor.py username path`  
Where username is your swgoh.gg username and path is where you want your file to be outputted to.

Finally, to use your mods:
`python mod_magician.py path_to_extracted_mods path_to_csv_file_of_character_demands path_to_output_mod_file`

There are examples called `example_extracted_mods.csv`, `example_character_demands.csv` and `example_output_mods.csv` to give you something to get started with before I get around to documenting all of this properly...


# Algorithm:
For each shape, find a list of mods with any of the requested sets, minimum pips and level (if not possible, make best effort).  
Then for each mod give it a rating.  
If it has the first secondary at max value, it gets +100 (scaling). If it has the first primary, it gets 15 * number of pips.  
If it has the second secondary at max value, it gets +50 (scaling). If it has the second primary, it gets 7.5 * number of pips.   
If it has the third secondary at max value, it gets +20 (scaling). If it has the third primary, it gets 3 * number of pips.  
The program then optimises the sum rating of the mods, whilst keeping target modsets if at all possible.  
