#!/usr/bin/python
import subprocess
code_dir = "code"
title = "Stanford ACM-ICPC Team Notebook"

def get_sections():
    sections = []
    section_name = None
    with open('contents.txt', 'r') as f:
        for line in f:
            if '#' in line: line = line[:line.find('#')]
            line = line.strip()
            if len(line) == 0: continue
            if line[0] == '[':
                section_name = line[1:-1]
                print(section_name)
                subsections = []
                if section_name is not None:
                    sections.append((section_name, subsections))
            else:
                tmp = line.split()
                tmp = [tmp[0], ' '.join(tmp[1:])]
                if len(tmp) == 1:
                    raise ValueError('Subsection parse error: %s' % line)
                filename = tmp[0]
                print(filename)
                subsection_name = tmp[1]
                if subsection_name is None:
                    raise ValueError('Subsection given without section')
                subsections.append((filename, subsection_name))
    return sections

def get_style(filename):
    ext = filename.lower().split('.')[-1]
    if ext in ['c', 'cc', 'cpp']:
        return 'cpp'
    elif ext in ['java']:
        return 'java'
    elif ext in ['py']:
        return 'py'
    else:
        return 'txt'

# TODO: check if this is everything we need
def texify(s):
    return s

def get_tex(sections):
    tex = []
    add = tex.append
    for (section_name, subsections) in sections:
        print(section_name)
        add('\\section{%s}\n' % texify(section_name))
        for (filename, subsection_name) in subsections:
            add('\\subsection{%s}\n' % texify(subsection_name))
            add('\\raggedbottom\\lstinputlisting[style=%s]{%s/%s}\n' % (get_style(filename), code_dir, filename))
            add('\\hrulefill\n')
        add('\n')
    return ''.join(tex)

if __name__ == "__main__":
    sections = get_sections()
    tex = get_tex(sections)
    with open('contents.tex', 'w') as f:
        f.write(tex)
    subprocess.call(['rm', 'notebook.pdf'])
    latexmk_options = ["latexmk", "-pdf", "notebook.tex"]
    subprocess.call(latexmk_options)

