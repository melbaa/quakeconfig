import io
from pprint import pprint

from pyparsing import *


def strip_quotes(value):

    if value != '' and len(value) > 2 and (value[0] == value[-1] == '"' or value[0] == value[-1] == "'"):
        value = value[1:-1]
    return value


class CfgTokenizer:

    def __init__(self):

        ws = ' \t'
        ParserElement.setDefaultWhitespaceChars(ws)

        identifier = Word(printables.replace(';', ''))
        identifier.setName('identifier')
        self.identifier = identifier
        """
        this magical regex does
          match an opening "
          match everything not an "\r\n
          match an optional "
          ensure a \r or \n follows but don't match them
          
          mydblQuotedString = Regex(r'"[^"\r\n]*?"?(?=[\r\n])')
          mydblQuotedString.setName('mydblquoted')
          
        problem is a quoted string can be followed by a comment
        """

        dblquoted_string_unclosed = Regex(r'"[^"\r\n]*?(?=[\r\n])')
        dblquoted_string_unclosed.setName('dbl quoted unclosed')
        self.dblquoted_string_unclosed = dblquoted_string_unclosed

        dblquoted_string_closed = Regex(r'"[^"\r\n]*?"')
        dblquoted_string_closed.setName('dbl quoted string closed')
        self.dblquoted_string_closed = dblquoted_string_closed

        lineComment = dblSlashComment + OneOrMore(lineEnd)
        lineComment.setName("// comment")
        self.lineComment = lineComment

        arg = dblSlashComment.suppress() | dblquoted_string_closed  \
            | dblquoted_string_unclosed | identifier
        arg.setName("argument")
        self.arg = arg

        seta_cvar = (Literal('seta') | Literal('set')).suppress() + \
            identifier + ZeroOrMore(arg)

        cvar = identifier + ZeroOrMore(arg)
        cvar.setName("cvar")
        self.cvar = cvar

        cmd = Optional(';').suppress() + \
            Group((seta_cvar | cvar) + Optional(';').suppress())
        cmd.setName("command")
        self.cmd = cmd

        line = lineComment.suppress() | OneOrMore(
            cmd) | OneOrMore(lineEnd).suppress()
        line.setName("line")
        self.line = line

        cfg_grammar = (ZeroOrMore(cStyleComment.suppress() | line)) + stringEnd
        self.cfg_grammar = cfg_grammar

        """
        NOTE: if you want debugging for the website, have to override the default
        debug actions
        
        search for self.debug and setDebug in the pyparsing source
        """

        # elems = [line, cfg_grammar, cmd
        #, lineComment, ccmd, cvar, arg,identifier, dblquoted_string_closed
        #, dblquoted_string_unclosed ]

        # for el in elems:
        # el.setDebug()
        #  pass

    def tokenize(self, cfgstring):
        if cfgstring is None:
            return []

        tokens = self.cfg_grammar.parseString(cfgstring)

        return tokens


if __name__ == '__main__':
    tokenizer = CfgTokenizer()
    tokens = tokenizer.tokenize(
        open('hugetest.cfg', encoding='utf8', errors='replace').read())

    tokens_list = tokens.asList()
    pprint(tokens_list)

    for tok in tokens_list:
        if tok[0] == 'bind' and len(tok) == 3:
            binding = tok[2]
            binding = strip_quotes(binding)
            binding_toks = tokenizer.line.parseString(binding)
            pprint(binding_toks.asList())
