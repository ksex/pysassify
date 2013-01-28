import re
import os


'''
PySassify: turns your css into sass

@todo: set up defaults
@todo: handle directory arguments
'''

ALLOWED_TYPE = '.css'

class Sassify(object):
    def __init__(self):
        self.base_url = os.getcwd() + '/data/'
        self.tab = '  '
    
    
    def generate_sass(self): 
        css_file = 'test.css'

        #open sass for writing
        sass_file = open(self.base_url + 'test.sass', 'wa')

        self.read_css(css_file, sass_file)
    
    '''
    @todo: generate new files based on current css file names
    '''    
    def read_css(self, css_file, sass_file):


        #open css for reading
        with open(self.base_url + css_file) as x: css_file = x.read()
        sel_re = re.compile(r'([^{]+){([^}]*)}', re.S)

        for match in sel_re.finditer(css_file):
            selector, body = match.groups()
            self.clean_css(selector, body, sass_file)
    
    
    def clean_css(self, selector, body, sass_file):
        '''
        @todo: handle >, commas, etc.
        '''   

        despaced_selectors = selector.strip().split()
        delined_decls = body.strip()
        
        # no empties
        if delined_decls:             
            highest = 0
            index = 0
            for x in despaced_selectors:
                if index > highest:
                    highest = index
                    
                new_results = [self.tab*index, x, "\n"]
                new = ''.join(new_results)
                sass_file.write(new)
                
                index += 1
                
            highest += 1
                    
            split_decls = [d.strip() for d in delined_decls.split(';')]
            
            for x in split_decls:
                new_results = [self.tab*highest, x, "\n"]
                new = ''.join(new_results)
                sass_file.write(new)


  


if __name__ == '__main__':
    sass = Sassify()
    sass.generate_sass()