#from git import Repo
#repo_dir = 'Dissertation'
#repo = Repo(repo_dir)
#file_list = [
#    'Dissertation/FeedPar_test.py',
#    'Dissertation/SplitDoc.py',
#    'Dissertation/PIKES_rest.py'
#]
#commit_message = 'First push!'
#repo.index.add(file_list)
#repo.index.commit(commit_message)
#origin = repo.remote('origin')
#origin.push()

from git import Repo
join = osp.join
bare_repo = Repo.init(join(rw_dir, 'bare-repo'), bare=True)
assert bare_repo.bare
