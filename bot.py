# bot.py
import os, random, datetime
from github import Github, GithubException

# List the exact repo names you want to target:
TARGET_REPOS = [
    "portfolio-react",
    "Fintrack",
    "terraZure",
]

MAX_LINES = 100

def run():
    token = os.getenv("GITHUB_TOKEN")
    gh    = Github(token)
    user  = gh.get_user()
    # Only keep the repos whose .name is in your TARGET_REPOS
    repos = [r for r in user.get_repos() if r.name in TARGET_REPOS]

    if not repos:
        print("No matching repos found; check TARGET_REPOS names.")
        return

    to_make = random.randint(3, 8)
    for i in range(1, to_make + 1):
        repo = random.choice(repos)
        path = "notes.txt"
        branch = repo.default_branch
        ts = datetime.datetime.now(datetime.timezone.utc)
        header = f"🕒 {ts.isoformat()} — commit #{i}"

        try:
            file = repo.get_contents(path, ref=branch)
            lines = file.decoded_content.decode().splitlines()
            new_lines = [header] + lines
            new_lines = new_lines[:MAX_LINES]
            content = "\n".join(new_lines) + "\n"
            repo.update_file(path,
                             f"Bot auto-commit #{i}",
                             content,
                             file.sha,
                             branch=branch)
            print(f"[{i}/{to_make}] Updated {repo.full_name}/{path}")

        except GithubException as e:
            if e.status == 404:
                # create notes.txt if missing
                try:
                    content = header + "\n"
                    repo.create_file(path,
                                     f"Bot create {path} #{i}",
                                     content,
                                     branch=branch)
                    print(f"[{i}/{to_make}] Created {repo.full_name}/{path}")
                except GithubException as e2:
                    print(f"[{i}/{to_make}] Skipped {repo.full_name} (branch: {branch}): {e2}")
            else:
                print(f"[{i}/{to_make}] Error on {repo.full_name}: {e}")

if __name__ == "__main__":
    run()
