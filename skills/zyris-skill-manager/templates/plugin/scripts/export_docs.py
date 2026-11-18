#!/usr/bin/env python3
"""ZYRIS documentation export v1. Canonical implementation: documentation plugin template.

Copies selected Markdown/assets verbatim; index.json is derived and never edited.
No target code execution, network, HTML rendering or publication.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlsplit
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ASSET_SUFFIXES = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg', '.avif', '.mp4', '.webm', '.pdf'}
FORBIDDEN = {'.git', '.tmp', '.env', '__pycache__', 'node_modules', 'dist', 'candidate', 'runs'}


def encode(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()


def source_file(root, name):
    if not isinstance(name, str) or not name or '\\' in name or name.startswith('/'):
        raise ValueError('Expected a repository-relative POSIX file path')
    parts = name.split('/')
    if any(p in ('', '.', '..') or p in FORBIDDEN or p.startswith('.env') for p in parts):
        raise ValueError('Unsafe/private source path: ' + name)
    path = root
    for part in parts:
        path /= part
        if path.is_symlink():
            raise ValueError('Source symlinks are not permitted: ' + name)
    if not path.is_file():
        raise ValueError('Source file missing: ' + name)
    return path


def configuration(root):
    data = json.loads(source_file(root, 'docs/documentation.json').read_text())
    if not isinstance(data, dict):
        raise ValueError('Documentation manifest must be an object')
    config = data.get('export')
    if not isinstance(config, dict) or set(config) != {'schema_version', 'pages', 'assets'} or type(config['schema_version']) is not int or config['schema_version'] != 1:
        raise ValueError('export requires schema_version=1, pages and assets; no duplicated product facts')
    policy = data.get('documentation', {})
    if not isinstance(policy, dict):
        raise ValueError('Documentation language policy must be an object')
    languages = policy.get('languages')
    default = policy.get('default_language')
    if not isinstance(languages, list) or not languages or any(x not in ('de','en') for x in languages) or len(set(languages)) != len(languages) or default not in languages:
        raise ValueError('Explicit valid documentation language policy required for export')
    pages, assets = config['pages'], config['assets']
    if not isinstance(pages, dict) or 'overview' not in pages:
        raise ValueError('export.pages must map stable page IDs to language/source maps and include overview')
    selected = set()
    for page_id, localized in pages.items():
        if not re.fullmatch(r'[a-z][a-z0-9-]*', page_id) or not isinstance(localized, dict) or set(localized) != set(languages):
            raise ValueError('Each page ID must provide exactly the selected languages')
        for language, name in localized.items():
            path = source_file(root, name)
            valid = name.startswith('docs/' + language + '/') or name == ('README.md' if language == default else f'README.{language}.md')
            if not valid or path.suffix != '.md' or name in selected:
                raise ValueError('Page path must be unique and belong to its selected language: ' + name)
            selected.add(name)
    if not isinstance(assets, list) or not all(isinstance(x,str) for x in assets) or len(set(assets)) != len(assets):
        raise ValueError('export.assets must contain unique explicit file paths')
    for name in assets:
        path = source_file(root, name)
        if not name.startswith(('docs/assets/', 'assets/')) or path.suffix.lower() not in ASSET_SUFFIXES:
            raise ValueError('Only approved media under docs/assets or assets may be exported: ' + name)
    return data, config, policy


def prose(text):
    text = re.sub(r'^\s*(`{3,}|~{3,})[^\n]*\n.*?^\s*\1\s*$', '', text, flags=re.M | re.S)
    return re.sub(r'`+[^`\n]*`+', '', text)


def links(text):
    """Supported public-doc syntax: inline Markdown, reference links, HTML href/src.

This is link inventory, not a Markdown/HTML renderer. Consumers must sanitize.
"""
    text = prose(text)
    values = re.findall(r'!?\[[^\]\n]*\]\(<?([^\s)>]+)>?(?:\s+["\'][^\n]*?["\'])?\)', text)
    definitions = {key.strip().casefold(): target for key,target in re.findall(r'^\s{0,3}\[([^\]]+)\]:\s*<?([^\s>]+)>?',text,re.M)}
    references = re.findall(r'!?\[([^\]\n]+)\]\[([^\]\n]*)\]',text)
    for label,key in references:
        key=(key or label).strip().casefold()
        if key not in definitions:
            raise ValueError('Undefined Markdown link reference: ' + key)
        values.append(definitions[key])
    # Including all definitions also covers shortcut reference links.
    values.extend(definitions.values())
    values.extend(re.findall(r'<[^>]+\b(?:href|src)\s*=\s*["\']([^"\']+)["\']', text, re.I))
    return sorted(set(values))


def heading_anchors(text):
    found, counts = set(), {}
    # Keep inline heading text while excluding fenced code.
    text = re.sub(r'^\s*(`{3,}|~{3,})[^\n]*\n.*?^\s*\1\s*$', '',text,flags=re.M|re.S)
    for heading in re.findall(r'^#{1,6}\s+(.+)$',text,re.M):
        heading=re.sub(r'<[^>]*>','',heading).lower()
        base=re.sub(r'\s','-',re.sub(r'[^\w\s-]','',heading))
        count=counts.get(base,0);counts[base]=count+1
        found.add(base if not count else f'{base}-{count}')
    found.update(re.findall(r'\bid=["\']([^"\']+)["\']',text))
    return found


def provenance(root, selected=()):
    def git(*args):
        return subprocess.run(['git','-C',str(root),*args],check=True,capture_output=True,text=True).stdout.strip()
    try:
        if Path(git('rev-parse','--show-toplevel')).resolve() != root:
            return {'revision':None, 'working_tree_dirty':None}
        try:
            revision=git('rev-parse','HEAD')
        except subprocess.CalledProcessError:
            revision=None
        dirty=bool(git('status','--porcelain','--untracked-files=all'))
        # Ignored-but-exported files must not be attributed to a clean commit.
        tracked=set(git('ls-files','-z').split('\0'))
        dirty=dirty or any(name not in tracked for name in selected)
        return {'revision':revision, 'working_tree_dirty':dirty}
    except (OSError,subprocess.CalledProcessError):
        return {'revision':None, 'working_tree_dirty':None}


def build_files(root):
    root=Path(root).expanduser().resolve()
    data,config,policy=configuration(root)
    manifest_bytes=source_file(root,'plugin.json').read_bytes()
    plugin=json.loads(manifest_bytes)
    if not isinstance(plugin,dict) or not isinstance(plugin.get('name'),str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',plugin['name']):
        raise ValueError('Valid plugin.json identity required')
    metadata={key:plugin[key] for key in ('name','version','description','license','author','homepage','repository') if key in plugin}
    interface=plugin.get('extensions',{}).get('com.openai',{}).get('interface',{})
    if interface.get('displayName'):
        metadata['display_name']=interface['displayName']
    files={};pages=[];assets=[];by_source={}
    def copy(name):
        content=source_file(root,name).read_bytes()
        destination='content/'+name
        files[destination]=content
        return {'source_path':name,'file':destination,'sha256':hashlib.sha256(content).hexdigest(),'bytes':len(content)}
    for page_id,localized in sorted(config['pages'].items()):
        for language,name in sorted(localized.items()):
            entry=copy(name)
            text=files[entry['file']].decode('utf-8')
            titles=re.findall(r'^# (.+)$',prose(text),re.M)
            if len(titles)!=1 or re.search(r'\{\{[^}]+\}\}',text):
                raise ValueError('Page must have one H1 and no unresolved placeholders: '+name)
            entry.update(id=page_id, language=language, title=titles[0])
            pages.append(entry);by_source[name]=entry
    asset_paths=set(config['assets'])
    for name in sorted(asset_paths):assets.append(copy(name))
    for page in pages:
        text=files[page['file']].decode('utf-8');inventory=[]
        for href in links(text):
            parsed=urlsplit(href)
            if parsed.scheme or parsed.netloc:
                if parsed.scheme not in ('http','https','mailto') or (parsed.scheme in ('http','https') and not parsed.netloc):
                    raise ValueError('Unsupported URL scheme: '+href)
                inventory.append({'href':href,'kind':'external'});continue
            decoded=unquote(parsed.path)
            if decoded.startswith('/') or '\\' in decoded:
                raise ValueError('Local links must be relative: '+href)
            target=(root / page['source_path']).parent / decoded if decoded else root/page['source_path']
            # Normalize .. in links while still checking every resulting source component.
            relative=os.path.relpath(os.path.abspath(target),root)
            path=source_file(root,relative)
            if parsed.fragment and path.suffix=='.md' and unquote(parsed.fragment) not in heading_anchors(path.read_text()):
                raise ValueError('Missing heading anchor: '+href)
            item={'href':href,'source_path':relative,'fragment':parsed.fragment,'query':parsed.query}
            if relative in by_source:
                other=by_source[relative];item.update(kind='page',page_id=other['id'],language=other['language'])
            elif relative in asset_paths:
                item.update(kind='asset',file='content/'+relative)
            elif relative.startswith(('docs/','assets/')) or relative.startswith('README'):
                raise ValueError('Linked page/asset is not declared in export: '+relative)
            else:
                # Public source references remain repository links, never recursively copied.
                if path.suffix.lower() in ('.key','.pem'):
                    raise ValueError('Private link target: '+relative)
                item.update(kind='repository')
            inventory.append(item)
        page['links']=inventory
    digest=hashlib.sha256()
    inputs={'plugin.json':manifest_bytes,'docs/documentation.json':source_file(root,'docs/documentation.json').read_bytes(),**files}
    for name,content in sorted(inputs.items()):digest.update(name.encode()+b'\0'+content+b'\0')
    selected=['plugin.json','docs/documentation.json',*[entry['source_path'] for entry in pages+assets]]
    source={**provenance(root,selected),'content_sha256':digest.hexdigest()}
    index={'schema_version':1,'format':'zyris.documentation','plugin':metadata,'documentation':policy,
           'source':source,'pages':pages,'assets':assets}
    files['index.json']=encode(index)
    return index,files


def export(root,output=None,check=False):
    root=Path(root).expanduser().resolve()
    index,files=build_files(root)
    if check:return {'valid':True,'pages':len(index['pages']),'assets':len(index['assets'])}
    output=Path(output).expanduser().absolute() if output else root/'dist'/f"{index['plugin']['name']}-documentation.zip"
    if output.suffix!='.zip' or output.name in ('','.','..'):
        raise ValueError('Export destination must be a .zip file')
    if any(p.is_symlink() for p in (output,*output.parents)):
        raise ValueError('Export destination must not contain symlinks')
    if output.is_relative_to(root) and output.parent != root/'dist':
        raise ValueError('In-repository exports must go directly into dist; source content must remain untouched')
    if output.exists():
        try:
            with zipfile.ZipFile(output) as old:
                previous=json.loads(old.read('index.json'))
                if not isinstance(previous,dict) or previous.get('format')!='zyris.documentation' or not isinstance(previous.get('plugin'),dict) or previous['plugin'].get('name')!=index['plugin']['name']:
                    raise ValueError('Unowned export destination')
        except (zipfile.BadZipFile,KeyError,ValueError) as exc:
            raise ValueError('Refusing to overwrite an unowned export destination') from exc
    output.parent.mkdir(parents=True,exist_ok=True)
    fd,temporary=tempfile.mkstemp(prefix='.docs-export-',dir=output.parent);os.close(fd)
    try:
        with zipfile.ZipFile(temporary,'w',zipfile.ZIP_DEFLATED) as archive:
            for name,content in sorted(files.items()):
                info=zipfile.ZipInfo(name,(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
                info.external_attr=0o100644<<16;archive.writestr(info,content)
        os.replace(temporary,output)
    finally:Path(temporary).unlink(missing_ok=True)
    return {'output':str(output),'pages':len(index['pages']),'assets':len(index['assets']),
            'source':index['source'],'published':False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,default=ROOT)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    try:
        print(json.dumps(export(args.source,args.output,args.check),indent=2));return 0
    except (OSError,ValueError,KeyError,TypeError,UnicodeError) as exc:
        print('ERROR: '+str(exc),file=sys.stderr);return 1


if __name__=='__main__':sys.exit(main())
