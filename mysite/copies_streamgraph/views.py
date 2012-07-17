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
        conn.default_indices=["logstash-2012.07.17"]
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
           q4 = WildcardQuery("agent", mystr2)
           q4 =q4.search()
           q4.facet.facets.append(facets.DateHistogramFacet('date_facet',field='timestamp',interval='minute'))
           results4 = conn.search(query = q4)
           finals[count]={u'term' : mystr ,u'entries' : results4.facets.date_facet.entries}
           #final[count]={u'term' : mystr ,u'count' : [{u'x': u'20/Jun/2012:06',u'y': x[0]},{u'x': u'20/Jun/2012:07' ,u'y': x[1]},{u'x':u'20/Jun/2012:08',u'y': x[2]}]}
           #finals[count]={u'term' : mystr ,u'count' : [{u'x': 0,u'y': x[0]},{u'x': 1 ,u'y': x[1]},{u'x':2,u'y': x[2]}]}
           count = count + 1
        print finals
        entry = simplejson.dumps(finals)
        return render(request, 'first5.html', {'agents': prepare_es_results(results, 'agent'),'finals': finals,'results':results,'entry':entry})
