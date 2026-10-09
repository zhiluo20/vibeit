"""Preview the GitHub Pages base path locally without changing generated URLs."""
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import argparse
ROOT=Path(__file__).resolve().parent.parent
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT),**kwargs)
    def do_GET(self):
        if self.path=="/":
            self.send_response(302);self.send_header("Location","/vibeit/cookbook/");self.end_headers();return
        if self.path.startswith("/vibeit/"):self.path=self.path[len("/vibeit"):]
        return super().do_GET()
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--port",type=int,default=8764);args=p.parse_args()
    print(f"Cookbook preview: http://127.0.0.1:{args.port}/vibeit/cookbook/",flush=True)
    ThreadingHTTPServer(("127.0.0.1",args.port),Handler).serve_forever()
