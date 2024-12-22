import os
import re
import click

from pathlib import Path
import shutil
from github import Auth, Github, GithubException

from git import Repo


@click.command
@click.option('--candidate_username', required=True)
@click.option('--github_token', required=True, default=os.environ.get('BOT_TOKEN'))
def setup_interview(candidate_username: str, github_token: str):
    repo_name = 'kyruus-interview-' + re.sub(r'[^a-z0-9]', '-', candidate_username.lower())
    print('Creating repo...')
    auth = Auth.Token(github_token)
    g = Github(auth=auth)
    org = g.get_organization("Kyruus-Interviews")

    try:
        github_repo = org.create_repo(repo_name, private=True, visibility='private')
    except GithubException as e:
        if e.status == 422:
            # repo already exists
            github_repo = org.get_repo(repo_name)
            print('Repo exists, continuing...')
        else:
            raise e

    # for repeated testing
    if Path(repo_name).exists():
        shutil.rmtree(repo_name)

    # now clone it down
    repo = Repo.clone_from(github_repo.ssh_url, repo_name)
    if not repo.heads:
        print('Copying files...')
        for path in Path('.').iterdir():
            if (
                path.name in ('meta', '.git', '__pycache__', repo_name)
                or
                (path.name.startswith('.') and path.name != '.gitignore')
                or
                path.name.startswith('kyruus-interview')  # for repeated runs
            ):
                continue
            print(path.absolute())
            if path.is_dir():
                shutil.copytree(path.absolute(), f'{repo_name}/{path.name}', dirs_exist_ok=True)
            else:
                shutil.copy(path.absolute(), repo_name)

        print('Pushing up changes...')

        repo.config_writer().set_value("user", "name", "Kyruus").release()
        repo.config_writer().set_value("user", "email", "ents@kyruus.com").release()

        repo.git.add(A=True)
        repo.git.commit(m='Initial commit')
        current = repo.create_head('main')
        current.checkout()
        repo.git.push('--set-upstream', 'origin', current)
    else:
        print('Repo not bare, skipping file operations')

    # check collaborators
    existing_collaborators = github_repo.get_collaborators()
    found_candidate = False
    for collaborator in existing_collaborators:
        if collaborator.login == candidate_username:
            found_candidate = True
            print("Candidate already a collaborator")

    if not found_candidate:
        print('Inviting candidate...')
        github_repo.add_to_collaborators(candidate_username, permission='push')

    print(f'Finished. Access/watch repo at {github_repo.svn_url}')


if __name__ == '__main__':
    setup_interview()
