#This is a very very simple module that emulates the behavior you'll see out of
# the actual printer output.  If you look in the status folder there are multiple
# files with .json extensions.  Each one represents a different value returned
# by the printer.
#If you import this and make use of it, the transition to real live data
# should be pretty trivial.
#david at davidmbp in ~/dev/v0MatrixMonitor on master! ± python
#Python 2.7.18 (default, Apr 22 2020, 05:03:29)
#[GCC 4.2.1 Compatible Apple LLVM 11.0.3 (clang-1103.0.32.29)] on darwin
#Type "help", "copyright", "credits" or "license" for more information.
#>>> import fetch
#>>> fetch.get('http://ip.of.printer:port/printer/status?extruder')
#'{"result":{"extruder":{"pressure_advance":0.788,"target":235,"temperature":234.63319843630617,"smooth_time":0.04}}}'

import json

class Response:

    def __init__(self, text):
        self.text = text

    def json(self):
        return self.text

def get(endpoint):
    with open('status/{}.json'.format(endpoint.split('?')[-1])) as file_object:
        file_contents = file_object.read()
        json_object = json.loads(file_contents)
    resp = Response(json_object)
    return resp