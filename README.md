# Easton Scraper
A portfolio project which consolidates data from the Easton gyms in the Denver area, and allows a user to search classes at all gyms at once.

## Operation
The user can retrieve data from all but one Easton gyms (Longmont needs to be added), have it stored locally, and search class names and instructors.  Enter the **easton_scraper_py** folder, then the commands below can be entered.

**Example commands:**
* To retrieve data from all gyms for today, just run the program without parameters: 
	* ``python3 scraper.py``
* To load from disk after running the above command:
	* ``python3 scraper.py --load``
* To print tomorrow's classes:
	* ``python3 scraper.py --tomorrow``
* To print classes for next Saturday
	* ``python3 scraper.py --weekday=saturday``
* To print the Denver schedule for the week:
	* ``python3 scraper.py --gym=denver --days=7``
* To do the same, but load from disk after running above command and exclude children's classes:
	* ``python3 scraper.py --load --gym=denver --days=7 --not=tiger``
* To search for intermediate muay thai classes for this week at all gyms:
	* ``python3 scraper.py --days=7 --and="muay thai" --and=int ``
* To search for BJJ and randori classes today:
	* ``python3 scraper.py --or=bjj --or=randori --or=roll``
* To delete classes that are over from disk:
    * ``python3 scraper.py --delete``

## Requirements

### Ubuntu Linux
Python 3 must be installed.  BeautifulSoup as well.  To install, run the following commands:
```
sudo apt-get install python3 python3-pip
pip3 install bs4 pytz
```

Or if using a virtual environment, in the base folder:
```
python3 -m venv env
env/bin/activate
pip install bs4 pytz
```

Or just use the pipfile:
```
pipenv run python scraper.py
```

If running unit tests:
```
pip3 install mock
```

### Other
This program was written in and run on Linux Mint (Ubuntu), but should work for any system with Python 3 installed, provided the equivalent installations are performed on the system.

## Testing
To run unit tests, enter the following commands:
* In the folder with **scraper.py**: 
	* ``export PYTHONPATH=$PYTHONPATH:$PWD``
* To run the tests, in the base repository folder:
	* ``python3 -m unittest discover -v``

## Future Improvements
* Use async.io for data retrieval
* Turn it into a webpage
* Add a GUI
* Add an actual database
* Do more testing, especially around the internet data retrieval and local data retrieval functions
