
import operator
from os import path

from requests import Session as S
from zeep import Client
from zeep.transports import Transport

from .adapters import SSLAdapter


class Session:

    url=property(operator.attrgetter('_url'))
    host=property(operator.attrgetter('_host'))
    keyfile=property(operator.attrgetter('_keyfile'))
    certfile=property(operator.attrgetter('_certfile'))
    passphrase=property(operator.attrgetter('_passphrase'))

    def __init__(self,url,host,keyfile,certfile,passphrase=None):
        self.url = url
        self.host = host
        self.keyfile = keyfile
        self.certfile = certfile
        self.passphrase = passphrase

    @url.setter
    def url(self, u):
        if not u: raise Exception("url cannot be empty")
        self._url = u

    @host.setter
    def host(self, h):
        if not h: raise Exception("host cannot be empty")
        self._host = h

    @keyfile.setter
    def keyfile(self, kf):
        if not kf: raise Exception("keyfile cannot be empty")
        if not path.exists(kf): raise Exception("keyfile path does not exist")
        self._keyfile = kf

    @certfile.setter
    def certfile(self, cf):
        if not cf: raise Exception("certfile cannot be empty")
        if not path.exists(cf): raise Exception("keyfile path does not exist")
        self._certfile = cf

    @passphrase.setter
    def passphrase(self, cf):
        self._passphrase = cf

    def connect(self):
        session = S()
        session.verify = False
        session.mount("https://{host}".format(host=self.host),SSLAdapter(certfile=self.certfile,keyfile=self.keyfile,password=self.passphrase))

        transport = Transport(session=session)
        client = Client(self.url,transport=transport)    
        self.service = client.service

    def call(self, name: str, *args, **kwargs):
        if  hasattr(self, 'service'):
            do = f"{name}"
            if hasattr(self.service, do) and callable(func := getattr(self.service, do)):
                return func(*args, **kwargs)
            else:
                Exception(f"this service does not exist")

        raise Exception("Need to connect to the service first")