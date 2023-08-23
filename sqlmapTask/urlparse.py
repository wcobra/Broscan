from hbases import *
import urlparse3




def parame():
    if sqlmapHbase() is not None:
        parameter = urlparse3.parse_url(sqlmapUri().decode(encoding="utf-8"))
        return parameter

par = []
def parQuery():
    if sqlmapHbase() is not None:
        for k in parame().query:
            par.append(k)
            par.sort()
        if len(par) is 0:
            return None
        else:
            return par