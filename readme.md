# HEMA Ratings analysis
This script takes a country based toplist from HEMA Ratings like https://hemaratings.com/periods/details/?ratingsetid=1&nationality=us and calculates an average rating for each club listed on it.
For better results you can define a minimal number of counted members for a club to be calculated and a minimal confidence level for fencers, e.g. you might only want to take clubs with at least three listed fencers with high or medium confidence into account.

## Installation
You need Python 3 to run this script and two libraries: lxml and requests

Install both libraries like this:
```
pip3 install lxml
pip3 install requests
```

## Usage
* If you run the script without any parameters it displays an average rating list of all american HEMA clubs, e.g. `py .\crawler.py`.
* `-h` displays the help
* With the `-u` parameter you can specify a different toplist to access, e.g. average all clubs with canadian fencers `py .\crawler.py -u "https://hemaratings.com/periods/details/?ratingsetid=1&nationality=ca"`
* With the `-c` confidence parameter you can specify which fencers should be counted towards the average of a club. There are three allowed values `"high"` which means only high confidence fencers are counted, `"medium"` which means high and medium confidence fencers are counted an `"all"` where everyone is calculated. `"all"` has the same effect as not specifying this parameter, e.g. calculate german clubs taking only their high confidence members into account `py .\crawler.py -c "high"`
* With the `-m` member parameter you can specify a minimal number of members listed, for a club to be taken into consideration. Clubs under this threshold will not be calculated and displayed in the results, e.g. display all german club rating averages with at least five listed members `py .\crawler.py -m 5`

## Limitations
* This script only works on country specific toplists and not on the overall toplists and is not intended to.
* It doesn't take into account if a club has members from different countries.
* Don't take the output of the scripts or HEMA Ratings in general too seriously, this is meant as an interesting experiment playing with the rating data.