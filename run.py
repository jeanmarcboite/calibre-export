import subprocess, json
from calibrestekje import Book, Publisher, init_session
calibredb = ["calibredb", "--with-library=http://localhost:8080"]


def run_calibre(args):
    command = calibredb + args
    print(' '.join(command))
    cmd = subprocess.run(calibredb + args, stdout=subprocess.PIPE)
    print(cmd)
    if (cmd.returncode != 0):
        print(cmd.output)
        return []
    return json.loads(cmd.stdout)

#cmd=subprocess.run(["calibredb", "--with-library=http://localhost:8080",  "-s",  "#bookshelf:=Biography",  "list",  "-f",  "id",  "--for-machine"], stdout=subprocess.PIPE)

#ids = run_calibre(["-s",  "#bookshelf:=Biography",  "list",  "-f",  "id",  "--for-machine"])
#print(ids)

bookshelves=run_calibre(["custom-columns"])