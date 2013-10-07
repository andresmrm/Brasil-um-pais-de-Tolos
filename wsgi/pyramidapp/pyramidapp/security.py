from .models import (
    DBSession,
    BdJogador,
    )

def groupfinder(nome, request):
    dbsession = DBSession()
    jog = dbsession.query(BdJogador).filter_by(nome=nome).first()
    if jog:
        return ['g:jogador']
        #return ['g:%s' % g for g in jog.groups]
