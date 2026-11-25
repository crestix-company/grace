"""Collect the six authorized original JPEGs for a static or ZIP release."""
import argparse
import base64
import json
import os
import posixpath
import re
import tempfile
from pathlib import Path
from urllib.request import Request, urlopen
from zipfile import ZipFile, ZIP_DEFLATED

from original_media import FILES, ORIGIN, UPLOADS

DIST = Path(__file__).resolve().parents[1] / 'dist'
LIMIT = 24 * 1024 * 1024


def jpeg(data):
    if len(data) > LIMIT or not data.startswith(b'\xff\xd8\xff') or b'\xff\xd9' not in data[-1024:]:
        raise ValueError('有効なJPEG画像を確認できません。')
    return data


def collect(read_existing, interior):
    photos = {}
    for name in FILES:
        data = read_existing(UPLOADS + name)
        if name == 'IMG_9091-1.jpg' and interior:
            data = interior.read_bytes()
        if data is None:
            request = Request(ORIGIN + name, headers={'User-Agent':'grace-site-build/1.0', 'Accept':'image/jpeg'})
            try:
                with urlopen(request, timeout=25) as response:
                    data = response.read(LIMIT + 1)
            except OSError as error:
                raise SystemExit(f'{name} を店舗サイトから取得できませんでした。{error}') from error
        photos[name] = jpeg(data)
    return photos


def localize(markup, path):
    for name in FILES:
        tag = f'data-original="{name}" src="'
        relative = posixpath.relpath(UPLOADS + name, posixpath.dirname(path) or '.')
        markup = re.sub(re.escape(tag) + r'[^"]*"', lambda _: tag + relative + '"', markup)
    return markup


def write_atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as f:
        tmp = Path(f.name)
    try:
        tmp.write_bytes(data)
        os.chmod(tmp, 0o644)
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


def patch_preview(preview, photos):
    text = preview.read_text()
    pattern = r'(<script type="application/json" id="site-photos">)(.*?)(</script>)'
    def patch(match):
        data = json.loads(match[2])
        for name, body in photos.items():
            data[name] = 'data:image/jpeg;base64,' + base64.b64encode(body).decode()
        return match[1] + json.dumps(data, separators=(',',':')) + match[3]
    text, count = re.subn(pattern, patch, text, flags=re.S)
    if count != 1:
        raise ValueError('対応するプレビューを確認できません。')
    write_atomic(preview.with_name('grace-offline.html'), text.encode())


def bundle(source, output, interior):
    if source.resolve() == output.resolve():
        raise ValueError('出力先には別のZIPを指定してください。')
    with ZipFile(source) as src, tempfile.TemporaryDirectory(dir=output.parent) as temp:
        names = set(src.namelist())
        photos = collect(lambda key: src.read(key) if key in names else None, interior)
        tmp = Path(temp) / 'site.zip'
        with ZipFile(tmp,'w',ZIP_DEFLATED) as dest:
            for item in src.infolist():
                if item.filename in {UPLOADS+n for n in FILES}:
                    continue
                data = src.read(item)
                if item.filename.endswith('.html'):
                    data = localize(data.decode(),item.filename).encode()
                dest.writestr(item, data)
            for name, data in photos.items():
                dest.writestr(UPLOADS+name,data)
        with ZipFile(tmp) as check:
            if check.testzip() is not None:
                raise ValueError('ZIPの検証に失敗しました。')
        os.replace(tmp, output)
    return photos


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dist',type=Path,default=DIST)
    parser.add_argument('--zip',type=Path)
    parser.add_argument('--output',type=Path,default=Path('grace-cloudflare.zip'))
    parser.add_argument('--preview',type=Path)
    parser.add_argument('--interior',type=Path)
    args = parser.parse_args()
    if args.zip:
        photos = bundle(args.zip,args.output,args.interior)
    else:
        root = args.dist
        if not (root/'index.html').is_file():
            parser.error('dist/index.html を確認できません。')
        photos = collect(lambda key: (root/key).read_bytes() if (root/key).is_file() else None,args.interior)
        for name, data in photos.items():
            write_atomic(root/UPLOADS/name,data)
        for page in root.rglob('*.html'):
            markup = page.read_text()
            updated = localize(markup, page.relative_to(root).as_posix())
            if updated != markup:
                write_atomic(page,updated.encode())
    if args.preview:
        patch_preview(args.preview,photos)
    print('公式ロゴ・店内・採用写真の6点を同梱しました。')


if __name__ == '__main__':
    main()
