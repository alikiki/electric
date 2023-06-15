import re
import os
import json
from lang.program import Program
from lang.utils import get_title, separate

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def get_config(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config

CONFIG = get_config("/Users/hwjeon/Documents/PROJECTS/electric/config.json")


class Post:
    def __init__(self, template, source, target):
        self.template = template
        self.source = source
        self.target = target

        self.title = None
        self.post = None

    def build(self):
        print(f"Building {self.source}.....", end="", flush=True)
        with open(self.source, "r") as source_f:
            text = source_f.read()
            head, body, offset = separate(text)
            head, body = Program(head), Program(body, offset)
            head_html, body_html = head.eval(), body.eval()
            self.title = get_title(head.get_ast())
            with open(self.template, "r") as template_f:
                template = template_f.read()
                html = re.sub(r'\|\|head\|\|', head_html, template)
                html = re.sub(r'\|\|body\|\|', body_html, html)

                self.post = html
        print("complete.")

    def get_link(self):
        if self.title is None:
            raise ValueError("must build the post first!")
        relative_path = f"posts/{os.path.basename(os.path.dirname(self.target))}/{os.path.basename(self.target)}"

        return f"<li><a href=\"{relative_path}\">{self.title}</a></li>"

    def publish(self):
        if self.title is None:
            raise ValueError("must build the post first!")
        print(f"Publishing {self.source}.....", end="", flush=True)
        with open(self.target, "w") as f:
            f.write(self.post)
        print("complete")

class MyHandler(FileSystemEventHandler):
    def on_any_event(self, _):
        posts = []

        # building posts
        for file in os.listdir(CONFIG["source_post_dir"]):
            src_path = os.path.join(CONFIG["source_post_dir"], file)
            trg_path = os.path.join(
                CONFIG["target_post_dir"], os.path.splitext(file)[0] + ".html")
            p = Post(
                CONFIG["post_template"],
                src_path,
                trg_path
            )
            p.build()
            p.publish()
            posts.append(p)

        # make post lists
        print(f"Build post list.....", end="", flush=True)
        with open(CONFIG["post_index_template"], "r") as f:
            template = f.read()
            titles = ''.join([post.get_link() for post in posts])
            html = re.sub(r'\|\|post-list\|\|', titles, template)
            with open(CONFIG["post_index"], "w") as index:
                index.write(html)
        print("complete.")


def watch_directory(path):
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print(f"Watching directory: {path}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    watch_directory(CONFIG["source_post_dir"])


    

    