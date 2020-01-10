'''Demoserver for RobotFlow
'''
from os.path import abspath
import cherrypy
from pathlib2 import Path


class FormGenerator():
    '''Main CherryPy class for showing pages
    '''
    def __init__(self):
        self.valid_customers = ['345', '732', '834']
        self.expired_customers = ['432', '545', '678']

    @cherrypy.expose
    def index(self):
        '''Display main page
        '''
        # pylint: disable=no-self-use
        return open("form/form.html")

    @cherrypy.expose
    def generate(self, **kwargs):
        '''Show customerId status
        '''
        keywords = kwargs.keys()
        if 'customerid' not in keywords:
            raise Exception
        customerid = kwargs['customerid']
        result = ''
        try:
            if len(customerid) == 3:
                if customerid == '000':
                    raise cherrypy.HTTPError(500)
                if customerid in self.valid_customers:
                    result = 'Customer is valid'
                elif customerid in self.expired_customers:
                    result = 'Customer is expired'
                else:
                    result = 'Unknown customer'
            else:
                result = 'Invalid CustomerId'
        except NameError:
            result = 'Invalid CustomerId'

        html_reply = '<HTML><body style="background-color:#E54B00">' \
                     '<div style="width:500px;height:200px;padding:20px;background-color:#DCDCDC;' \
                     'margin:100px auto 0px auto;border: 2px solid black;"' \
                     '<h1>CustomerId result</h1><p>Result is:<a style="color:red" id="result">'
        html_reply = html_reply + result
        html_reply = html_reply + '</a></p></div></body></HTML>'
        return html_reply

FORMPATH = Path('.') / Path('form')
CP_CONF = {
    '/': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': abspath(str(FORMPATH))
        }
    }

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': 8080})
    cherrypy.quickstart(FormGenerator(), '/', CP_CONF)
