# Installation
You will need Python installed on your system.  
I downloaded it for Windows from here:  
https://www.python.org/downloads/  
Load a command prompt and try:  
`python --version`  
if it shows some form of an error, Python isn't installed sufficiently.  
  
To install required external packages, run  
`pip3 install -r requirements.txt`  
 
You may also want to install git - that's up to you, you can also just download the code as a zip file.  

You will need a swgoh.gg account to scrape mods from.  
 
# Mod extraction
Then to extract your mods, make sure you are in the directory with the swgoh_mods code, then:  
`python mod_extractor.py username path`  
Where username is your swgoh.gg username and path is where you want your file to be outputted to.  
For example:  
`python mod_extractor.py tommo tommo_mods.csv`  
The file in `path` (`tommo_mods.csv` in my example) will then contain all of your mods, scraped from swgoh.gg.  
The file is in comma separated variable (csv) format.  
You can load it in your favourite spreadsheet program - just make sure to tell it the cells should be comma separated.  
The first row is a header and should tell you what all of the columns mean.  Don't worry about the `new_toon` column just yet - that will get filled in by the `mod_magician`.

# Automatic mod assignment
Finally, the mod magician can automatically optimise your mod placement based on your character demands:  
`python mod_magician.py path_to_extracted_mods path_to_csv_file_of_character_demands path_to_output_mod_file`  
There are examples called `example_extracted_mods.csv`, `example_character_demands.csv` and `example_output_mods.csv` to give you something to get started with - they are some examples of some modding I did recently.  

## To place your mods
In the output csv file a number of `new_toon` entries will have been filled in.  
You need to move the mod referenced on that row from the toon labelled in `current_toon` to the toon labelled in `new_toon`.  
Yes, this part is tedious.  

## Character demands
Note that the mod magician optimises mods for the character in the first row, then the second with whatever is left, then the third with whatever is left after that etc., so put your higher priority characters higher up.  
`example_character_demands.csv` gives you somehting to get started with, but here's a breakdown of the columns:  
**name:** call them whatever you want, this is what will get put in the `new_toon` column of the mod_magician output. Doesn't have to correspond to anything in particular - it's just a label.  
**minpip:** if there is a minimum number of pips / dots you want mods on this character to have, specify here. If you don't care, put 0. The mod magician will get mods of this minimum pip level if possible, but will use lower pip mods if the other demands make that impossible.  
**minlevel:** if there is a minimum level you want mods on this character to have, specify here. If you don't care, put 0. The mod magician will get mods of this minimum level if possible, but will use lower level mods if the other demands make that impossible.  
**modset:** which modsets you want.  for every entry here the mod magician will get two mods of the chosen set if possible (if not it will substitute alternatives). Note that for critical damage, to make a full set you need 4 mods, so will need to have critical damage twice here.  
**primary:** the mod magician will try to get mods with your chosen primaries (with priority corresponding to the order you put them), but with lowish priority.  
**secondary:** the mod magician will optimise its mod selection based on the secondaries you put here, with more emphasis on the first choice than the second etc.  

## recommended use
The way I use the mod magician is to put a few character demands in, see what it gets and iterate a bit.  
For example, I might change the modsets for a toon a couple of times until it gets loads of speed secondary. Or I might change which primaries I ask for and so on.  
Then once I'm happy with a few toons I'll add a couple more and iterate those.  
Bit by bit I'll then get through the toons I want to optimise.  
Remember, the mod magician can't make your mods better, just help you pick which ones to pick where, so if you use all your good mods on your arena team don't expect it to be able to make good mods on your backup TW teams!  

## Excluding mods
You may wish to exclude certain mods from the mod magician (perhaps you are happy with your arena mods and just want to mod your HAAT team for example).  
In that case, just open the extracted mods csv file, delete the mods you don't want the mod magician to optimise with, save and close the extracted mods file and carry on. It can't optimise mods it doesn't know about!


# Algorithm:
In depth, when selecting mods for a character the magician does:
For each shape, find a list of mods with the requested sets, minimum pips and level (if not possible, make best effort).  
Then for each mod give it a rating.  
If it has the first secondary at max value, it gets up to +100 (scaling dependent on value). If it has the first primary, it gets 10 * number of pips.  
If it has the second secondary at max value, it gets up to +50 (scaling dependent on value). If it has the second primary, it gets 5 * number of pips.   
If it has the third secondary at max value, it gets up to +20 (scaling dependent on value). If it has the third primary, it gets 2 * number of pips.  
The program then optimises the sum rating of a full set of mods of each shape, whilst keeping target modsets if at all possible.  
