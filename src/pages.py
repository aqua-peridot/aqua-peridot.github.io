import json, glob, os

OPT_SRC_DIRS = [ # local@erico's machine
    "C:\\Users\\ericotjoa\\Desktop\\mygarage\\atatabi-control-panel\\chrepo\\ch",
]

def load_py_script_vars(py_dict_dir):
    namespace = {} 
    with open(py_dict_dir, 'r') as f:
        exec(f.read(), {}, namespace)
    return namespace


def update_opt():
    from src.directory import manage_dirs
    DIRS = manage_dirs()

    fetch_opt(DIRS)
    convert_compiled_opt_to_src(DIRS)
    write_opt_to_catalogue(DIRS)

def fetch_opt(DIRS):
    compiled = {
        # name : {
        #   "semantic_list": [], # in case there are multiple instances (homonyms)
        #   "components_list": [],
        # }
    }
    for dir_ in OPT_SRC_DIRS:
        for ch_dir in glob.glob(f"{dir_}/*.py"):
            chscript = load_py_script_vars(ch_dir)
            CPACK = chscript.get('CPACK')
            # print(CPACK['chname'], CPACK['chtitle'])
            
            for opt in CPACK['opt']['items']:
                name = opt['name']
                if not name in compiled:
                    compiled.update({name:{ "semantic_list": [], "components_list": [],}})
                compiled[name]["semantic_list"].append(opt["semantic"])
                compiled[name]["components_list"].append(opt["components"])

    with open(DIRS['OPT_COMPILED_DIR'], 'w') as f:
        json.dump(compiled, f, indent=2)

def transcribe_one_set_of_components(components):
    # components is like [['capybara', None], ['baros', 'heavy - Greek']]
    t = []
    try:
        for w1, lang in components:        
            if lang is None:
                t.append(w1)
            else:
                t.append(f"{w1} ({lang})")
    except:
        print(components)
        print("error at transcribe_one_set_of_components???")
    t = ' + '.join(t)
    return t

def convert_compiled_opt_to_src(DIRS):
    with open(DIRS['OPT_COMPILED_DIR'], 'r') as f:
        compiled = json.load(f)

    opt_src = []
    for name, content in compiled.items():
        ctranscribed = []
        for components in content['components_list']:
            ctranscribed.append(transcribe_one_set_of_components(components))
        ctranscribed = ' | '.join(ctranscribed)
        opt_src.append(f"{name} : {ctranscribed}")

    with open(DIRS['OPT_SRC_DIR'], 'w') as f:
        json.dump(opt_src, f, indent=4)

def write_opt_to_catalogue(DIRS):
    with open(DIRS['OPT_SRC_DIR'], 'r') as f:
        opt_src = json.load(f)

    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alphax = 0 # pointer
    alphad, alphadx = {}, {}

    opts = ""
    opts_nav = []
    opt_src.sort(key=lambda y: y.lower())

    for i, opt in enumerate(opt_src):        
        atmp = opt[0].upper() 
        if atmp in alphad:
            alphad[atmp].append(i)
        else:
            alphad[atmp] = [i]

    for x, ixs in alphad.items():
        alphadx[ixs[0]] = x

    for i, opt in enumerate(opt_src):        
        if i in alphadx:
            opts += f"  <div class='opt-nav' id='{alphadx[i]}'>{alphadx[i]}</div>\n"
            opts_nav.append(f"<a href='#{alphadx[i]}'>{alphadx[i]}</a>")
        opts += f"  <p>{opt}</p>\n"

    with open(DIRS['OPT_HTML_TEMPLATE_DIR'], 'r') as h:
        template = h.read()

    opt_page = template.replace("[[opt-page-content]]", opts)
    opt_page = opt_page.replace("[[opt-nav-content]]", ' | '.join(opts_nav))
    
    with open(DIRS['OPT_HTML_DIR'], 'w') as h:
        h.write(opt_page)