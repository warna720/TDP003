Portfolio system
==============

About
-----

The portfolioproject is a template-based webserver created by Warhell Nasim and Henrik Björs.

The portfoliosystem simplifies managing smaller porfolio webpages for user with limited knowledge about HTML and programming generally


Installation instructions
-------------------------

### Linux
**1:** `sudo apt-get update && sudo apt-get install –y python3 python3-pip python-virtualenv git´

**2:** Download latest version of system `svn checkout https://svn-und.ida.liu.se/courses/TDP003/2014-1-PRA1/ip1-2-5/TDP003/portfolio --username <username> ~/portfolio´
Replace "<username>" with your username.

**3:** Navigate to the path where you saved the system. `cd ~/portfolio´

**4:** Create a virtual environment `virtualenv portfolio´

**5:** Activate the virtual environment `. portfolio/bin/activate´

**6:** Install Flask `pip install flask´

**7:** Start the system `python3 portfolio.py´



Documents
---------
You can find installation instructions, user manual, system documentation and test documentation inside the folder "doc" which is stored within the root of this project.
(/doc/*.pdf)
