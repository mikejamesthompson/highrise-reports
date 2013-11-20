Highrise Reports
==========

A couple of scripts for fetching useful business development report data from Highrise. There are two main scripts: `dealfetcher.py` and `peoplefetcher.py`. The latter is still somewhat experimental. 

`Dealfetcher.py` can collect three types of report for a given period of time: new deals (deals that were created within the period given), won deals (deals whose status was updated to "won" within the period given) and lost deals (you get the idea). `Dealfetcher.py` can be called from the command line with three arguments: the type of report, the start date and the end date. Dates should be provided in the format: DD Mmm YYYY, for example: 01 Jan 2013.


Quick Start
-------------------------------------
* Copy config-example.py to config.py and replace the dummy data with the real thing.
* Create a directory called "output" in the same folder as the script.
* Run: `python dealfetcher.py won "01 Jul 2013" "30 Sep 2013"`, for example, to get the deals marked as won during the third quarter of 2013.
