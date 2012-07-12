#from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render
from pyes import *
from django.utils import simplejson
from django.template.loader import render_to_string


def prepare_es_results(results, key):
    for result in results:
        for value in result['@fields'][key]:
            yield value

def hello_world(request):
        conn = ES('127.0.0.1:9200')
        conn.default_indices=["logstash-2012.07.10"]
        conn.refresh()
        print "i'm in"
        q = MatchAllQuery()
        q = q.search()
        q.facet.add_term_facet(field='agent',size=4)
        results = conn.search(query = q)
       
        z= results.facets['agent']['terms'][0]['term']
        if z == '"Java/1.5.0_15"' :
          results.facets.agent.terms.pop(0)
        else :
          results.facets.agent.terms.pop(3)
       
        finals= [{},{},{}]
        count=0
        for item in results.facets['agent']['terms']:
           mystr = item['term']
           mystr = mystr[:mystr.find('/') ]
           mystr = mystr[1:]
           mystr2 = "*" + mystr +"*"
           print mystr
           q2 = WildcardQuery("agent", mystr2)
           results2 = conn.search(query = q2)
           print results2.count()
           finals[count]={u'term' : mystr ,u'count' : results2.count()}
           count = count + 1
        return render(request, 'first3.html', {'agents': prepare_es_results(results, 'agent'),'finals': finals,'results':results})
