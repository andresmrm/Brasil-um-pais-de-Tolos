# Create your views here.
import math,random
from django.http import HttpResponse
from django.conf import settings
from jinja2 import FileSystemLoader, Environment
from slimish_jinja import SlimishExtension

template_dirs = getattr(settings,'TEMPLATE_DIRS')
default_mimetype = getattr(settings, 'DEFAULT_CONTENT_TYPE')
env = Environment(loader=FileSystemLoader(template_dirs), extensions=[SlimishExtension])
env.slim_debug = True

def render_to_response(filename, context={},mimetype=default_mimetype):
    template = env.get_template(filename)
    rendered = template.render(**context)
    return HttpResponse(rendered,mimetype=mimetype)



class Jogador():

    def __init__(self):
        self.nome = "Tolo"
        self.dinheiro = 5
        self.mao = []
        self.mesa = {}



def index(request):
    users = [{'name': 'foo', 'last_name': 'bar'},
             {'name': 'bar', 'middle_name': 'baz'},
             {'name': 'baz'}]

    j1 = Jogador()
    j1.mao = [1,2,3,4]
    j2 = Jogador()
    j3 = Jogador()
    j4 = Jogador()
    j5 = Jogador()
    jogadores = [ j.__dict__ for j in [j2, j2, j3, j4, j5]]

    return render_to_response('jogo.slim',{'jogadores':jogadores})
