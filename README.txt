The folder that has useful content is the streamgraph folder 

Requirements
use Elastic search version 0.18.7 or O.18.6
use logstash-1.1.0-monolithic
Python Elasticsearch
D3.js

-I rewrote the logstash index template to have the dates in a date format rather strings

-Mysite is based on Django and middleman is the Django app

-In middle man ,there's a view.py where i make elastic search queries using pyes(python wrapper for rest api)
 
-In mysite/templates stream.html is responsible for sketching the stream graph

-Please use the log file attached as my stream.html is set to handle that data ,i need 2 add more flexiblity to it