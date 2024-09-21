import json


def update_opt():
    from src.directory import manage_dirs
    DIRS = manage_dirs()

    with open(DIRS['OPT_SRC_DIR'], 'r') as f:
        opt_src = json.load(f)

    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alphax = 0 # pointer
    alphad, alphadx = {}, {}

    opts = ""
    opts_nav = []
    opt_src.sort()
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