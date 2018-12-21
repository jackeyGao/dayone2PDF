# -*- coding: utf-8 -*-
'''
File Name: markdown.py
Author: JackeyGao
mail: gaojunqi@outlook.com
Created Time: 五  8/12 09:59:17 2016
'''
import sys, re
import misaka as m
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

cleanr =re.compile('<.*?>')


class HighlighterRenderer(m.HtmlRenderer):
    def __init__(self, flags=0, nesting_level=0, photos=[]):
        super(HighlighterRenderer, self).__init__(flags=0, nesting_level=0)
        self.photos = { x["identifier"]: "%s.%s" % (x["md5"], x["type"]) for x in photos}

    def blockcode(self, text, lang):
        _id = hash(text)
        _id = "code%s" % str(_id)

        if ':' in lang:
            lang, title = lang.split(':')
        else:
            lang, title = lang, ''

        
        if '#' in title:
            flag, title = title.split('#')
        else:
            flag, title = '', title
            

        langDiv = '<a href="#%s" id="%s" class="lang-label">Raw</a>'% (_id, _id)
        titleDiv = ''
        
        if flag == 'warning':
            flagDiv = '<i class="yellow exclamation mini icon"></i>'
        elif flag == 'error':
            flagDiv = '<i class="red exclamation mini icon"></i>'
        elif flag == "good":
            flagDiv = '<i class="green check mini icon"></i>'
        else:
            flagDiv = ''
            
        if title:
            if flag:
                titleDiv = '<div class="title-label">%s</div>' % (flagDiv + title)
            else:
                titleDiv = '<div class="title-label">%s</div>' % title
        else:
            titleDiv = '<div class="title-label empty">&nbsp;</div>'

        if not lang:
            return '''<div class="code-wrapper">''' + langDiv + titleDiv + \
        '''\n<div class="highlight"><pre>%s</pre></div></div>\n''' % text.strip()


        try:
            lexer = get_lexer_by_name(lang, stripall=True)
            language = lang
        except ClassNotFound:
            lexer = get_lexer_by_name('text', stripall=True)
            language = lang
            
        formatter = HtmlFormatter()
        text = text.encode('utf-8')
        content = highlight(text, lexer, formatter)
            
        langDiv = '<a href="#{0}" id="{0}" class="lang-label">'.format(_id) + language + '</a>'
        return '<div class="code-wrapper">' + langDiv + titleDiv + content + '</div>'


    def blockquote(self, content):
        _real = re.sub(cleanr,'', content).strip()
        if _real.startswith('%center\n'):
            content = content.replace('%center', '')
            className = "blockquote-center"
        elif _real.startswith('%warning'):
            content = content.replace('%warning', '')
            className = "blockquote-warning"
        elif _real.startswith('%error'):
            content = content.replace('%error', '')
            className = "blockquote-error"
        else:
            content = content
            className = "blockquote-normal"
        
        content = content.strip()
        content = content.replace('\n', '<br/>')
        content = content.replace('</p><br/>', '</p>')
        content = content.replace('<p><br/>', '<p>')

        #print content

        # content = content.strip('<br/>')

        return '''<blockquote class="%s">
                %s</blockquote>''' % (className, content)

    def image(self, link, title="", alt=''):
        #link = link.replace('/uploads', 'https://o8uou7r4o.qnssl.com')
        identifier = link.replace('dayone-moment://', '')
        
        if identifier in self.photos:
            link = "../../dayone/photos/" + self.photos[identifier]
        else:
            link = identifier

        if 'cover' in title:
            self.cover = link

        if 'border' in title:
            css_class = "hassubimage border"
        else:
            css_class = "hassubimage"

        if 'radius' in title:
            css_class += ' radius'

        if alt == 'hidden':
            return '<p style="display: none;"></p>'

        if alt:
            return  '''
                    <p class="%s"><img src="%s"></p>
                    <p class="img-title"><span class="symbol">#</span>%s</p>''' % (css_class, link, alt)
        else:
            return '<p class="%s"><img src="%s"></p>\n' % (css_class, link)

    def table(self, content):
        return '<div class="code table-wrapper"><table class="ui selectable celled table">'\
                + content + '</table></div>'


markdown = m.Markdown(
    HighlighterRenderer(),
    extensions=\
    m.EXT_FENCED_CODE |\
    m.EXT_TABLES |\
    m.EXT_QUOTE
)


def get_markdown(photos=[]):
    return m.Markdown(
        HighlighterRenderer(photos=photos),
        extensions=\
        m.EXT_FENCED_CODE |\
        m.EXT_TABLES |\
        m.EXT_QUOTE
    )

#toc = m.Markdown(m.HtmlTocRenderer())

def markrender(content):
    md = markdown(content)
    print(dir(markdown))
    return md

if __name__ == '__main__':
    print(markrender('''> %center'''))
