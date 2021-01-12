import os
import re

regex = re.compile("\{% macro [a-zA-Z]+\(\) %\}")

print(os.listdir("."))

macros = {}
with open('macros.html', 'r') as f:
    contents = f.read()

    for i in range (10):
        match = regex.search(contents)
        if match:
            start = match.span()[1]

            macro = contents[start : contents.index("{%endmacro%}")]
            call = contents[match.span()[0] : match.span()[1]]
            name = call[call.index("macro") + 6 : call.index("(")]
            macros[name] = macro

            print(start, contents.index("{%endmacro%}"))

            contents = contents[contents.index("{%endmacro%}") + len("{%endmacro}%}"):]
        else:
            break;

    #print(macros)

for f in os.listdir('.'):
    if f != 'macros.html':
        with open(f, 'r') as alter:
            contents = alter.read()

            replace = re.compile("\{% from \"macros.html\" import [a-zA-Z]+ %\}")
            
            match = replace.finditer(contents)

            for m in match:
                span = m.span()
                
                call = contents[span[0] : span[1]]
                name = call[call.index('import') + 7 : call.index(" %}")]
                contents = contents[:span[0] - 1] + macros[name] + contents[span[1] : ]
            
        with open('build/' + f, 'w') as n:
            n.write(contents)

    


            

