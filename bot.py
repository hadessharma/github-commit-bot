# bot.py
import os, random, datetime
from github import Github, GithubException

MAX_LINES = 100

def run():
    token = os.getenv("GITHUB_TOKEN")
    gh    = Github(token)
    user  = gh.get_user()
    repos = list(user.get_repos())

    to_make = random.randint(3, 8)
    for i in range(1, to_make + 1):
        repo = random.choice(repos)
        path = "notes.txt"
        branch = "main"
        ts = datetime.datetime.utcnow().isoformat()
        header = f"🕒 {ts} — commit #{i}"

        try:
            file = repo.get_contents(path, ref=branch)
            lines = file.decoded_content.decode().splitlines()
            # insert new line at top, trim to MAX_LINES
            new_lines = [header] + lines
            new_lines = new_lines[:MAX_LINES]
            content = "\n".join(new_lines) + "\n"
            repo.update_file(path, f"Bot auto-commit #{i}", content, file.sha, branch=branch)
            print(f"[{i}/{to_make}] Updated {repo.full_name}/{path}")

        except GithubException as e:
            if e.status == 404:
                # create fresh file with just this line
                content = header + "\n"
                repo.create_file(path, f"Bot create {path} #{i}", content, branch=branch)
                print(f"[{i}/{to_make}] Created {repo.full_name}/{path}")
            else:
                print(f"[{i}/{to_make}] Error on {repo.full_name}: {e}")

if __name__ == "__main__":
    run()
