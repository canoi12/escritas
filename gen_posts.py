import yaml
import pypandoc
import os
import json
import unicodedata
import shutil
import sys

PUBLIC_DIR = 'public/'
POSTS_DIR = '_posts/'
MEDIA_DIR = 'media/'

def extract_meta(content):
    if content.startswith('---'):
        end = content.find('---', 3)
        if end != -1:
            meta_section = content[3:end].strip()
            metadata = yaml.safe_load(meta_section)
            return metadata
    return None

def extract_content(markdown):
    return pypandoc.convert_text(markdown, 'html', format = 'md', extra_args = ['--lua-filter', 'filter.lua'])

def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass

    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")

    return str(text)

class StaticSite:
    posts_meta = []
    base_dir = POSTS_DIR
    build_dir = PUBLIC_DIR
    def build(self):
        if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
            self.base_dir = sys.argv[1]

        if not os.path.isdir(self.build_dir + self.base_dir):
            os.mkdir(self.build_dir + self.base_dir)

        if not os.path.isdir(self.build_dir + MEDIA_DIR):
            os.mkdir(self.build_dir + MEDIA_DIR)

        self.generate_posts(self.base_dir)

        with open(self.build_dir + self.base_dir + 'meta.json', 'w', encoding='utf-8') as file:
            json.dump(self.posts_meta, file, ensure_ascii=False, indent=4)

    def process_file(self, dirpath, filename):
        # print(dirpath)
        if 'media/' in dirpath:
            # print(dirpath, filename)  
            shutil.copyfile(dirpath + filename, self.build_dir + MEDIA_DIR + filename)

    def process_post(self, dirpath, filename):
        if not filename.endswith('.md'):
            self.process_file(dirpath, filename)
            return
        print('Converting ', dirpath + filename, ' to JSON')
        with open(dirpath + filename, 'r', encoding='utf-8') as file:
            source = file.read()
        
        metadata = extract_meta(source)
        content = extract_content(source)

        if metadata and content:
            
            final_name = strip_accents(filename.replace('.md', '.json').replace('#', '').lower())
            path = self.build_dir + self.base_dir + final_name  
            metadata['content'] = content
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(metadata, file, ensure_ascii=False, indent=4)

            meta = {}
            meta['filepath'] = final_name
            meta['linkname'] = final_name.replace('.json', '')

            for item in metadata:
                if not 'content' in item:
                    meta[item] = metadata[item]

            # meta['title'] = metadata['title']
            # meta['author'] = metadata['author']
            # meta['date'] = metadata['date']
            # meta['tags'] = metadata['tags']
            # meta['category'] = metadata['category']
            self.posts_meta.append(meta)
        else:   
            print("Erro ao extrair metadata")

    def generate_posts(self, dirpath):
        for f in os.listdir(dirpath):
            if 'obsidian' in f:
                continue
            if os.path.isdir(dirpath + f):
                self.generate_posts(dirpath + f + '/')
            else:
                self.process_post(dirpath, f)

static = StaticSite()
static.build()