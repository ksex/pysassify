import re
import os
import argparse


'''
PySassify: turns your css into sass

Usage: 

python sassify.py [relative source directory] [relative destination directory]
'''

ALLOWED_TYPE = '.css'

class Sassify(object):
    def __init__(self):
        parser = argparse.ArgumentParser(description='Sassify our css.')
        parser.add_argument('source_folder', metavar='s', type=str,
                           help='source folder (relative to current path)')        
        parser.add_argument('destination_folder', metavar='d', type=str,
                           help='destination folder (relative to current path)')
        
        self.args = parser.parse_args()
        self.base_url = os.getcwd()
        self.tab = '  '
    
    def set_source_directory(self):
        self.source_dir = os.path.join(self.base_url, self.args.source_folder)
        
    def set_dest_directory(self):
        self.destination_dir = os.path.join(self.base_url, self.args.destination_folder)
        
    def generate_sass(self): 
        self.set_source_directory()
        self.set_dest_directory()
        
        for ddir in os.listdir(self.source_dir):
            css_path = os.path.join(self.source_dir, ddir)
            if not os.path.isfile(css_path): continue
            base, ext = os.path.splitext(ddir)
            if ext.lower() == ALLOWED_TYPE:
                
                css_file = ddir
                sass_path = os.path.join(self.destination_dir, '%s.sass' % base)
                sass_file = open(sass_path, 'wb')
                self.read_css(css_path, sass_file)

     
    def read_css(self, css_file, sass_file):


        #open css for reading
        with open(css_file) as x: css_file = x.read()
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