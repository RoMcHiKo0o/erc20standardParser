import requests
from github import Github
from github import Auth
import time
import pickle


def save_repo(username='OpenZeppelin', reponame='openzeppelin-contracts', filename='repo'):
    with open('token.txt','r') as file:
        token = file.read()

    auth = Auth.Token(token)
    g = Github(auth=auth)

    user = g.get_user(username)

    repo = user.get_repo(reponame)
    with open(filename, 'wb') as file:
        file.write(pickle.dumps(repo))

def get_repo_from_file(filename='repo'):
    with open(filename,'rb') as file:
        return  pickle.loads(file.read())

def get_all_tags(repo):
    return list(repo.get_tags())


def save_all_releases(repo, filename='releases.txt'):
    releases = [r.name for r in get_all_tags(repo)]
    with open(filename, 'w') as file:
        for i in releases:
            file.write(i)
            file.write('\n')

def fetch_tokens(repo, releases_filename='releases.txt'):

    url_rate_limit = 'https://api.github.com/rate_limit'
    r = requests.get(url_rate_limit)
    rate_limit = int(r.json()['resources']['core']['remaining'])
    print('limit: ', rate_limit)


    with open(releases_filename, 'r') as file:
        releases = file.read().split('\n')


    cnt=1
    for i,r in enumerate(releases):
        if cnt==rate_limit-1:
            break
        time.sleep(.1)
        try:
            print(i,len(releases))
            cnt+=1
            token_code = repo.get_contents('contracts/token/ERC20/ERC20.sol', r).decoded_content.decode('utf-8')
            with open(f'token_releases_codes/{r}.sol', 'w') as file:
                file.write(token_code)
        except Exception as e:
            print('error with release: ' + r)
            with open('errors.txt', 'a') as file:
                file.write(r + ': ' + str(e))
                file.write('\n')


if __name__ == "__main__":

    # save_repo()
    repo = get_repo_from_file()

    # save_all_releases(repo)

    fetch_tokens(repo)