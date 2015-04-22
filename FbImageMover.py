from BaseHTTPServer import BaseHTTPRequestHandler
import sys
import argparse
import os
import re
import urlparse
from facebook import FacebookAPI, GraphAPI
import threading
from ContentParser import ContentParser

__author__ = 'szyszy'


import SimpleHTTPServer
import SocketServer

PORT = 8000



class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global code
        url_parts = urlparse.urlparse(self.path)
        query = dict(urlparse.parse_qsl(url_parts[4]))
        code = query['code']
        self.send_response(200)

        access_token = f.get_access_token(code)
        final_access_token = access_token['access_token']
        print final_access_token
        graph = GraphAPI(final_access_token)

        print graph.get('912718602075890')

        print graph.get('182142105167327/feed')



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputs_basedir', required=True,
                        help='base dir for the input files')
    args = parser.parse_args()
    argsDict = vars(args)
    # #deletes null keys
    argsDict = dict((k, v) for k, v in argsDict.items() if v)
    return argsDict


def main():
    args_dict = parse_args()
    inputs_basedir = args_dict['inputs_basedir']


    httpd = SocketServer.TCPServer(("", PORT), MyHandler)
    print "serving at port", PORT
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = False
    server_thread.start()
    print "Server loop running in thread:", server_thread.name

    #ImageMover
    global f
    client_id = '900950606613375'
    client_secret = '4abcc9e6925437194bcc2c58ac3c43d9'
    #TRAILING SLASH IN URL IS MANDATORY
    f = FacebookAPI(client_id=client_id, client_secret=client_secret, redirect_uri='http://localhost:'+str(PORT) + '/')
    #scope = ['publish_stream', 'user_photos', 'user_status'] ##this wasnt work
    #'user_groups'
    scope = ['public_profile', 'user_groups']
    auth_url = f.get_auth_url(scope=scope)

    print 'Connect with Facebook via: %s' % auth_url

    #exit(0)
    # files = [f for f in os.listdir(inputs_basedir) if os.path.isfile(os.path.join(inputs_basedir,f))]
    # for f in files:
    #     if re.match('\d+_\d+_\d+_\w\..*', f):
    #         img_id = f.split('_')[1]
    #         ContentParser.parse(img_id)


if __name__ == "__main__":
    main()