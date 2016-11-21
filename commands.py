import controls
from os.path import dirname, abspath, basename, isfile
import  math, sys, getopt, threading, atexit, json, importlib, glob
__author__="Nick Pesce"
__email__="npesce@terpmail.umd.edu"

if __name__ == "__main__":
    print "This is module can not be run. Import it and call start()"
    sys.exit()

SPEED = 0b10
COLOR = 0b1
t = None
stop_event = threading.Event()
effects = {}
commands = []
ranges = {}
default_range = None

with open('configuration/speeds.json') as data_file:    
    speeds = json.load(data_file)

with open('configuration/colors.json') as data_file:    
    colors = json.load(data_file)

with open('configuration/ranges.json') as data_file:    
    rangeJson = json.load(data_file)
    for k in rangeJson:
        if default_range is None:
            default_range = k
        r = rangeJson[k]
        ranges[k] = range(r['start'], r['end'])

np = controls.Led_Controller(ranges)
np.set_ranges([default_range])

def start(effect_name, **args): 
    global t
    if not is_effect(effect_name):
        return (help(), False)
    
    if 'speed' in args:
        args['speed'] = 10**((args['speed']-50)/50.0)

    #Stop previous effect
    stop_event.set()
    if t is not None:
        t.join()
    stop_event.clear()
    np.off()

    if 'ranges' in args:
        np.set_ranges(args['ranges'])
    else:
        np.set_ranges([default_range])

    args['lights'] = np
    args['stop_event'] = stop_event

    try:
        effect = effects[effect_name.lower()]
        t = threading.Thread(target=effect.start, kwargs=args)
        t.daemon = True
        t.start()
        return (effect.start_string,  True)
    except Exception, e:
        return (str(e), False)

def help():
    return """Effects:\n    ~ """ + ("\n    ~ ".join(d["name"] + " " + modifiers_to_string(d["modifiers"]) for d in commands))

def modifiers_to_string(modifiers):
    ret = ""
    if(modifiers & SPEED):
        ret += "[-s speed]"
    if(modifiers & COLOR):
        ret += "[-c (r,g,b)]"
    return ret

def get_effects():
    return commands

def get_colors():
    return colors

def get_speeds():
    return speeds 

def get_ranges():
    return [k for k in ranges]
    
def get_value_from_string(type, string):
    """Given a attribute represented as a string, convert it to the appropriate value"""
    if type.lower() == 'color':
        for c in colors:
            if c['name'].lower() == string.lower():
                return c['color']
        return [255, 255, 255]
    elif type.lower() == 'speed':
        return speeds.get(string.lower(), 1)
    elif type.lower() == 'ranges':
        return string.split(",")
    return string

def combine_colors_in_list(list):
    """Takes a list of strings, and combines adjacent strings that are not known to be speeds"""
    ret = []
    cat = None
    for i in range(0, len(list)):
        if speeds.has_key(list[i].lower()):
            if not cat is None:
                ret.append(cat)
                cat = None
            ret.append(list[i].lower())
        else:
            if cat is None:
                cat = list[i].lower()
            else:
                cat += " " + list[i].lower()
    if not cat is None:
        ret.append(cat)
    return ret

def is_effect(name):
    return name.lower() in effects

def import_effects():
    files = glob.glob(dirname(abspath(__file__))+'/effects/*.py')
    module_names = [ basename(f)[:-3] for f in files if isfile(f) and basename(f) != '__init__.py' and basename(f) != 'template.py']
    package = __import__('effects', globals(), locals(), module_names, -1)
    modules = []

    for m in module_names:
        modules.append(getattr(package, m))

    for m in modules:
        name = getattr(m, 'name')
        modifiers = getattr(m, 'modifiers')
        effects[name.lower()] = m
        commands.append({'name' : name, 'modifiers' : modifiers})

def _clean_shutdown():
    stop_event.set()
    if t is not None:
        t.join()
    np.off()

import_effects()
atexit.register(_clean_shutdown)
