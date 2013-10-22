Highrise Reports
==========

A simple script for fetching some deal data from Highrise. Currently, takes a start date (which it implictly assumes is the beginning of the month, it'll break if you do something different) and fetches, for the quarter following the start date, the following data, putting each dataset in a separate csv file:

* deals that were created in the quarter in question
* deals whose status was changed to "won" in the quarter
* deals whose status was changed to "lost" in the quarter


Quick Start
-------------------------------------
* Copy config-example.py to config.py and replace the dummy data with the real thing.
* Create a directory called "output" in the same folder as the script.
* Run it.
