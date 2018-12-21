# -*- coding: utf-8 -*-
"""
    @JackeyGao
    Create at 2018-12-18
"""
import json
import traceback
import os
import jinja2
import arrow
import shutil

from urllib.parse import unquote

from md import get_markdown

loader = jinja2.FileSystemLoader(searchpath="templates")
env = jinja2.Environment(loader=loader)


def log(msg):
    """Log"""
    print('+ %s' % (msg))


class Handler(object):

    def __init__(self, file):
        self.file = file
        self.toc = []

    @property
    def name(self):
        name = unquote(self.file).replace('.json', '')
        return name.split('/')[-1]

    def read_json(self):
        with open(self.file, 'r') as f:
            return json.loads(f.read())
    
    def render_entry(self, entry):
        if 'photos' in entry:
            markdown = get_markdown(photos=entry["photos"])
        else:
            markdown = get_markdown(photos=[])
    
        if 'text' in entry:
            content = markdown(entry["text"])
        else:
            content = ''

        t = env.get_template('entry.html')
        create = arrow.get(entry["creationDate"])

        entry["create"] = create

        name = create.format("YYYYMMDDHHmmss")
        log('正在生成%s' % name)

        output = t.render(
            content=content, entry=entry, book=self.name, name=name
        )
        
        with open('output/entries/%s.html' % name, 'w') as f:
            f.write(output)

        self.toc.append(name)


    def render(self):
        data = self.read_json()

        for entry in data["entries"]:
            self.render_entry(entry)

        with open('output/%s.json' % self.name, 'w') as f:
            f.write(json.dumps(self.toc, indent=2, ensure_ascii=False))


def initialization():
    if os.path.exists('output'):
        shutil.rmtree('output')

    os.mkdir('output')
    os.mkdir('output/entries')


def main():
    try:
        _dir = './dayone'

        # 初始化
        initialization()

        log("初始化;")

        json_files = [ os.path.join(_dir, x) \
            for x in os.listdir(_dir) \
            if x.endswith('.json') 
        ]

        if not json_files:
            log("Warning: 在 dayone 目录中没有找到 JSON 文件.")
            log("Warning: 请将dayone导出目录解压到当前目录, 并重命名为dayone。")
        
        for file in json_files:
            handler = Handler(file)
            handler.render()
    except FileNotFoundError:
        log("Error: 请将dayone导出目录解压到当前目录, 并重命名为dayone。")
    except Exception as e:
        log("Error: 未知错误 \n%s" % traceback.format_exc())

    log("生成HTML完成.")


if __name__ == '__main__':
    main()
