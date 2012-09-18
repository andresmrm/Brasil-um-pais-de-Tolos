from .models import (
    DBSession,
    BdJogador,
    )

GROUPS = {'admin':['g:admin'],
          '1':['g:jogador'],
         }

def groupfinder(nome, request):
    dbsession = DBSession()
    record = dbsession.query(BdJogador).filter_by(nome=nome).first()
    if record:
        return ['g:jogador']
    #if nome in USERS:
    #    return GROUPS.get(nome, [])
