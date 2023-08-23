from hbases import *
import urlparse3


def awvsParameter():
    parame = urlparse3.parse_url(awvsUri().decode(encoding="utf-8"))
    return parame

def awvsKeys():
    keys = awvsParameter().query.keys()
    return keys

awvsPar = []
def awvsParQuery():
        for k in awvsParameter().query:
            awvsPar.append(k)
            awvsPar.sort()
        if len(awvsPar) is 0:
            return None
        else:
            return awvsPar