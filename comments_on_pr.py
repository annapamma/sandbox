# POST /repos/:owner/:repo/pulls/:number/comments

# https://api.github.com/repos/annapamma/sandbox/issues/

# get PR associated with a commit
# https://app.circleci.com/jobs/github/annapamma/sandbox/236

# SHA = 8f24a1b05222c739cc2f42b3aa8ba22d384b2a25

# res = GET https://api.github.com/repos/annapamma/sandbox/commits/8f24a1b05222c739cc2f42b3aa8ba22d384b2a25/pulls

# pr_number = res[0]['number']

# https://developer.github.com/v3/issues/comments/#create-a-comment
# https://api.github.com/repos/annapamma/sandbox/pulls/4/comments