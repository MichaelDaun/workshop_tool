# Startar noden och lådans beteende. Samma fil i alla lådor.
import config
from nod import Nod

lada = __import__("lador." + config.LADA, None, None, ["starta", "varv"])
nod = Nod(config)
nod.kor(lada)
