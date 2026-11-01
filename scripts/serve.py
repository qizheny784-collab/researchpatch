"""Serve only dist/ on loopback; no dependencies or model training."""
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import argparse

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port',type=int,default=4173)
    args=parser.parse_args()
    public=Path(__file__).resolve().parents[1]/'dist'
    handler=partial(SimpleHTTPRequestHandler,directory=str(public))
    print(f'ResearchPatch: http://127.0.0.1:{args.port}',flush=True)
    with ThreadingHTTPServer(('127.0.0.1',args.port),handler) as server:server.serve_forever()
