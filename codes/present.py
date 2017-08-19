# A set of functions for displaying pretty text output in our presentation

from __main__ import HTML, display, time, clear_output, F, T, L
import copy

def present(string, size=60, font='Baskerville'):
    """
    Return pretty output for presentation.
    Requires a string.
    Optional arguments: size for font size, font for font-type
    
    Make sure HTML and display are loaded from IPython.display.
    """

    # html code for formatting the presented message
    html_template=\
    """
    <div class="present" style="font-size: {size}px; font-family: {font}">
       {string}
    </div>
    """
    
    # replace newline statements with a break
    string = string.replace('\n', '<br>')

    # fill in the values for font-size, font-family
    html_formatted = html_template.format(string=string, size=size, font=font)

    # present
    display(HTML(html_formatted))


def animate_text(words, slots, template, progress_dict, show_dict, sleep=.1):
    
    '''
    Modify a string of format statements in a desired sequence.
    
    Words is a dictionary with a key: word_consonants + word_node
        this key is used rather than just the word_node 
        since keywords for string formats cannot be integers.
        There is one value: 'node', with the bare TF node number (as integer).
        
    Slots is a string with format values that correspond 
        to the keys in progress_dict and show_dict, i.e., the word id.
        
    Template is an html string which receives the formatted text.
        
    Requires a progress_dict, i.e., with word ID keys and values wherein
        the values are slots to be progressively filled in with values from show_dict.
        
    Requires a show_dict, i.e. with word ID keys and values wherein
        the values are the text to be displayed.
    '''

    # run the loop and display slots
    for word_id, word_node in words.items():
        
        # set the present object's value to be displayed
        progress_dict[word_id] =  show_dict[word_id] 
        
        # get all the display text, including the new added value
        run_text = slots.format(**progress_dict)

        # display it
        display(HTML(template.format(txt=run_text)))
        
        time.sleep(sleep)
        
        clear_output(wait=True)
        

def display_slots(passage):
    
    '''
    Blah blah blah
    '''
  
    # the html code
    # this can be stored in a file and opened when needed so its out of sight
    template =\
    '''
    <html>

    <body>

        <div class="present_animation">
        
            <div class="present_title">
                <span>Text-Fabric Slots</span>   
                <hr style="border-top: 1px solid grey; width: 25%">
            </div>
        
            <div class="hebrew_text">
                {txt}
            </div>
            
        </div>

    </body>

    </html>
    '''
    
    
    # get word nodes from the provided passage
    word_nodes = L.d(T.nodeFromSection(passage), otype='word')
    
    
    # build word id
    
    # get lexeme plain text from word nodes 
    word_lexs = [F.g_cons.v(w) for w in word_nodes]
    
    # format into a word ids dictionary
    words = dict((lex+str(word), word) for lex, word in zip(word_lexs, word_nodes)
                )
        
    # formatted string with slots
    word_slots = ['{' + word + '}' for word in words]
    slots = ''.join(word_slots)
    
    # track progress here
    progress = dict((word, '') for word in words)
    
    
    # first animation: hebrew text
    
    heb_style = '{}<span style="color:blue">&nbsp; | &nbsp;</span>'
    heb_words = [F.g_cons_utf8.v(word_n) for word, word_n in words.items()] # get utf8 text
    show_hebrew = dict((word_id, heb_style.format(word)) for word_id, word in zip(words, heb_words)
                     )
    # run animation
    animate_text(words, slots, template, progress, show_hebrew)

    # wait for input
    input()

    # second animation: slots and node numbers
    
    # work-around so that the hebrew words are displayed on phrases slide
    progress2 = copy.deepcopy(progress)

    # span style for font/colorizing the line
    nodes_style = '<span style="font-size: 28px;">{}</span>\
                    <span style="color:blue">|</span>'
    # show slot node numbers
    show_nodes = dict((word, nodes_style.format(words[word])) for word in words
                     )
    # run animation
    animate_text(words, slots, template, progress2, show_nodes)
    
    # progressively build up the data by returning the progress dict
    return progress, words


def obj_boundaries(word_node, obj):
    
    '''
    Check to see if a given word node is at the beginning
    or end of a given object.
    Return 1 for beginning and 2 for end.
    '''
   
    obj_word_nodes = L.d(obj, otype='word')

    if obj_word_nodes[0] == obj_word_nodes[-1] == word_node:
        return 1
    
    elif obj_word_nodes[0] == word_node:
        return 2
    
    elif obj_word_nodes[-1] == word_node:
        return 3
    
    else:
        return None


def display_objects(passage, obj_type, words={}, progress={}):
    
    # deep copy words/progress dicts to prevent cumulative overwrites
    # the wrods/progress dicts are inherited from the previous runs
    words = copy.deepcopy(words)
    progress_dict = copy.deepcopy(progress)

    # the html code
    # this can be stored in a file and opened when needed so its out of sight
    template =\
    '''
    <html>

    <body>

        <div class="present_animation">
        
            <div class="present_title">
                <span>Slots into {obj_type}</span>   
                <hr style="border-top: 1px solid grey; width: 25%">
            </div>
        
            <div class="hebrew_text">
                {txt}
            </div>
            
        </div>

    </body>

    </html>
    '''.format(obj_type=obj_type, txt='{txt}')
    
    # get word nodes from the provided passage
    word_nodes = L.d(T.nodeFromSection(passage), otype='word')
    
    # get object types
    objects = L.d(T.nodeFromSection(passage), otype=obj_type)
    
    # formatted string with slots
    word_slots = ['{' + word + '}' for word in progress_dict]
    slots = ''.join(word_slots)
    
    
    # animate objects
    
    div_start = '<div class="{}">'.format(obj_type)
    
    div_end = '</div>'
    
    # mapping from a wordnode to its ID 
    node_to_id = dict((node, ID) for ID, node in words.items())
    
    # display on object-by-object basis
    for obj in objects:
        
        obj_words = L.d(obj, otype='word')
            
        # change words at the boundaries of the object
        for word in obj_words:
                        
            is_bound = obj_boundaries(word, obj)
            
            # do not modify words without boundaries
            if not is_bound:
                continue
                            
            word_id = node_to_id[word]
            
            # prepare div tag 
            if is_bound in {1,2}:
                
                slot_range = '<div class="slotrange">{}-{}</div>'.format(obj_words[0], obj_words[-1])\
                                if len(obj_words) > 1\
                                else '<div class="slotrange">{}</div>'.format(obj_words[0])
                        
                div_start_ranges = div_start + slot_range
                
                # prepare node tag, only applied at end of obj, i.e. is_bound == 1 or 3
                node = '<div class="node_id">{}</div>'.format(obj)
            
            # add div tag to beginning or end as required
            if is_bound == 1:
                progress_dict[word_id] = div_start_ranges + progress_dict[word_id] + node + div_end
                
            elif is_bound == 2:
                progress_dict[word_id] = div_start_ranges + progress_dict[word_id]
                
            else:
                progress_dict[word_id] = progress_dict[word_id] + node + div_end
                
        # animate
        animate_text(words, slots, template, progress_dict, progress_dict, sleep=0)
        
    return slots, progress_dict

def display_span(clause_atom_list):
    html_span = '<span style="font-size: 14pt; font-family: Times New Roman">{content}</span>'
    
    html_div =\
    '''
        <div class="time_spans"  style="font-size: 20pt; 
                font-family: Times New Roman; 
                direction: rtl; 
                color:{color};
                width: 80%">

                {content} 
    </div>
    '''

    book, chapter, verse = T.sectionFromNode(clause_atom_list[0])

    # show header
    display(HTML(html_span.format(content=f'{book} {chapter}')))
    print()

    for ca in clause_atom_list:

        book, chapter, verse = T.sectionFromNode(ca)
        
        # look for time markers
        time_markers = [phrase for phrase in L.d(ca, otype='phrase')
                           if F.function.v(phrase) == 'Time'
                       ]

        text = T.text(L.d(ca, otype='word'))
        indent = '...' * F.tab.v(ca)
        typ = F.typ.v(ca)
        text_indented = f'{chapter}:{verse}' +\
                        '&nbsp;&nbsp;&nbsp;&nbsp;' +\
                        str(F.tab.v(ca)) +\
                        '&nbsp;&nbsp;' +\
                        typ +\
                        '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' +\
                        indent +\
                        text

        # format color
        cur_clause = L.u(ca, otype='clause')[0]
        color = 'blue' if time_markers else ''

        yield html_div.format(color=color, content=text_indented)
    print()
