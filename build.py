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

for f in os.listdir('./templates'):
    if f != 'macros.html' and f.endswith(".html"):
        with open('./templates/' + f, 'r') as alter:
            contents = alter.read()

            delete = re.compile("\{% from \"macros.html\" import [a-zA-Z]+ %\}")

            for i in range (10):
                m = delete.search(contents)

                if m == None:
                    break;

                # delete the occurence of the match 
                span = m.span()
                contents = contents[:span[0]] + contents[span[1]:]

            replace = re.compile("\{\{[a-zA-Z]+\(\)\}\}")

            for i in range (10):
                m = replace.search(contents)
               
                if m == None:
                    break;

                print(m)
                span = m.span()
                
                call = contents[span[0] : span[1]]
                print(call)
                name = call[call.index('{') + 2: call.index("(")]
                contents = contents[:span[0]] + macros[name] + contents[span[1] : ]
            
        with open(f, 'w') as n:
            n.write(contents)

    


            

