import os, json

def manage_dirs():
    DIRS = {}  
    WORKSPACE_DIR = 'workspace'
    PAGES_DIR = 'pages'

    OPT_SRC_DIR = os.path.join(WORKSPACE_DIR, 'opt-src.json')
    if not os.path.exists(OPT_SRC_DIR):
        with open(OPT_SRC_DIR, 'w') as f:
            json.dump([], f, indent=4)

    OPT_HTML_TEMPLATE_DIR = os.path.join(PAGES_DIR, "opt-template.html")
    OPT_HTML_DIR = os.path.join(PAGES_DIR, "opt.html")

    DIRS.update({
        'WORKSPACE_DIR': WORKSPACE_DIR,
        'OPT_SRC_DIR': OPT_SRC_DIR,
        'OPT_HTML_TEMPLATE_DIR': OPT_HTML_TEMPLATE_DIR,
        'OPT_HTML_DIR': OPT_HTML_DIR,
        })
    return DIRS