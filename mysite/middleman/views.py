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
    #q =WildcardQuery("agent", "\"SAMSUNG-SGH-E250i*")
    q =WildcardQuery("timestamp", "20/Jun/2012:06:*")
    results = conn.search(query = q)
    q =WildcardQuery("timestamp", "20/Jun/2012:07:*")
    results2 = conn.search(query = q)
    q =WildcardQuery("timestamp", "20/Jun/2012:08:*")
    results3 = conn.search(query = q)
    #return render(request, 'es-results.html', {
     #  'agents': prepare_es_results(results, 'agent'),
      # 'results': results,
      # })
    return render(request, 'first3.html', {
     'agents': prepare_es_results(results, 'agent'),
      'results': results,
      'results2': results2,
      'results3': results3,
      })
