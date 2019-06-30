import os
import re
import sys

sys.path.append(os.path.abspath("anki"))
from anki.storage import Collection

# The range is taken from here:
# https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_(Unicode_block)
CJK_UNIFIED_RE = re.compile(r"[\u4e00-\u9FFF]")

def load_collection(db_dir, db_file):
    db_dir = os.path.expanduser(db_dir)
    coll_path = os.path.join(db_dir, db_file)
    return Collection(coll_path, log=True)

def has_chinese(s):
    return bool(CJK_UNIFIED_RE.search(s))

def tag_chinese(col):
    for cid in col.findNotes("tag:*"):
        note = col.getNote(cid)
        is_chinese_note = any(has_chinese(f) for f in note.fields)
        if is_chinese_note:
            tags = note.tags
            if 'chinese' not in tags and 'geography' not in tags:
                front = note.fields[0]
                print("tagging note: [tags: %s]: %s" % (tags, front))
                note.addTag('chinese')
                note.flush()

def main():
    # Real database:
    DB_DIR = "~/Library/Application Support/Anki2/Sphynx"
    DB_FILE = "collection.anki2"

    # For experiments:
    # DB_DIR = "~/anki-experiments/app/User 1"

    col = load_collection(DB_DIR, DB_FILE)
    tag_chinese(col)
    print('saving to db...')
    col.save()

if __name__ == '__main__':
    main()
