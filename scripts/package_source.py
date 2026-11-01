"""Export a GitHub-ready source archive without Site identity or secrets."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

root=Path(__file__).resolve().parents[1]
out=root/'dist/researchpatch-source.zip'
excluded={'.git','.openai','__pycache__','node_modules','output'}
with ZipFile(out,'w',ZIP_DEFLATED) as z:
    for p in sorted(root.rglob('*')):
        relative=p.relative_to(root)
        if not p.is_file() or p==out or any(x in excluded for x in relative.parts):continue
        if p.name.startswith('.env') or p.suffix in {'.pt','.pth','.partial','.pyc'}:continue
        z.write(p,str(Path('researchpatch')/relative))
with ZipFile(out) as z:
    assert z.testzip() is None
    assert 'researchpatch/README.md' in z.namelist()
print(f'Source archive: {out} ({out.stat().st_size} bytes)')
