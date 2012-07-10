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
    conn.default_indices=["logstash-2012.07.04"]
    conn.refresh()
    q = TermQuery("agent", "\"SAMSUNG-SGH-E250i/E250iJAKA1 Profile/MIDP-2.0 Configuration/CLDC-1.1 UP.Browser/6.2.3.3.c.1.101 (GUI) MMP/2.0\"")
    results = conn.search(query = q)

    #return render(request, 'es-results.html', {
     #  'agents': prepare_es_results(results, 'agent'),
      # 'results': results,
      # })
    return render(request, 'first3.html', {
     'agents': prepare_es_results(results, 'agent'),
      'results': results,
      })
