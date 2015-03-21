This is the source for http://melbalabs.com/quakeconfig  

The project has multiple features:  
* parse and annotate configs
* see unused and unknown cvars (think console commands)
* compare two configs side by side

Major components include:  
* a quake live config parser, which I believe is the most interesting.
People's configs are quite a mess, many of them take advantage of the
the recovering parser of the game, so they put all kinds of ascii art and
invalid strings. Some even manage to crash the game.
* a comparator of configs
* a cherrypy website and assets that make things easier to compare
* a database of cvar descriptions from http://www.regurge.at/ql/
* some example configs to play around with

esr thread http://www.esreality.com/post/2543295/quake-live-config-analyzer/