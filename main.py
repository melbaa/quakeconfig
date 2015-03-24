import os
from os.path import join

import cherrypy
import mako.lookup

import quakeconfig.libs.cfgcompare as cfgcompare


# relative to the web root, which should be above this directory
PROJECT_NAME = 'quakeconfig'
DATA_DIR = join(PROJECT_NAME, 'data/')
TEMPLATE_DIR = join(PROJECT_NAME, 'templates/')
MODULE_DIR = join(TEMPLATE_DIR, 'compile/') # compiled templates

loader = mako.lookup.TemplateLookup(
    directories=[TEMPLATE_DIR],
    collection_size=25,
    module_directory=MODULE_DIR,
    output_encoding='utf-8',
    input_encoding='utf-8',
    strict_undefined=True
)


def get_configs(kwargs):
    cfg_a = kwargs.get('cfgA')
    if cfg_a is not None:
        cfg_a = cfg_a.file
       
    cfg_b = kwargs.get('cfgB')
    if cfg_b is not None:
        cfg_b = cfg_b.file
       
    return cfg_a, cfg_b
    
def get_showdiff(kwargs):   
    if kwargs.get('showdiff') == 'showdiff':
        return True
    return False
          
  
class Quakeconfig:
    def __init__(self, logger):
        self.loader = loader
        self.logger = logger
        self.quake_data = cfgcompare.Data(DATA_DIR)
    
    def _render(self, **kwargs):

        template = self.loader.get_template('cfgcompare.txt')
            
        max_file_size = cherrypy.server.max_request_body_size
          
        cfg_a, cfg_b = get_configs(kwargs)
        """
        the cfg vars can have 3 values
        None
        Part with a None .file
        Part with a nonempty .file

        only the last case will cause us to do work
        """
        
        showdiff = get_showdiff(kwargs)

        (sections,
            sections_map,
            report_binds, 
            report_aliases, 
            report_section, 
            report_uncat, 
            report_unknown) = self.quake_data.cfgcompare(cfg_a, cfg_b, showdiff)
            
        return template.render(
            title='Quake Live Configuration Analyzer',
            max_file_size=max_file_size,
            sections=sections,
            sections_map=sections_map,
            report_binds=report_binds,
            report_aliases=report_aliases,
            report_section=report_section,
            report_uncat=report_uncat,
            report_unknown=report_unknown)
    
    @cherrypy.expose
    def index(self, *args, **kwargs): 
        rendered_text = self._render(**kwargs)    
        return rendered_text

  