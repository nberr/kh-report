# kh-report
Tool to compare assets in a keyper locker and homenet inventory

This tool was created for Ford of Ventura. The primary goal of this tool is to identify tools that exist in the keyper locker but not in homenet.

## Dependencies and Setup
* linux subsystem
* chromedriver placed in C:\Drivers
* python
* pip - pandas, selenium

After downloading the project put the folder in the home folder. Create a shortcut of the batch file and place it on the desktop. Before running make sure there are not files in the downloads folder with the name temp.csv or InventoryReport-[current_date].xls. 

The script will need to be tweaked if the keyper locker local IP changes or if the dealership ID changes on homenet.
