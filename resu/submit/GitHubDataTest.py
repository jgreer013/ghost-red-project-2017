from github import Github
import sys

import getopt


def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hs:o:")
    except getopt.GetoptError:
        print 'GitHubDataTest.py -s <searchString> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
           print 'GitHubDataTest.py -s <searchString> -o <outputfile>'
           sys.exit()
        elif opt in ("-s"):
           searchString = arg
        elif opt in ("-o"):
           outputfile = arg
    #searchString = raw_input("Search String:")
    writeFile = open(outputfile + ".tsv", 'w')
    me = Github("GhostHackery", "Test123")
    users = me.search_users(searchString)
    users = me.search_users(searchString)
    
    for user in users:
        if user.name is not None: #so long as the username exists, do the things
            writeFile.write((user.name.encode('utf8')))
            writeFile.write("\n" + str(user.contributions))
            if user.location is not None:
                writeFile.write("\n" + user.location.encode('utf8'))
            else:
                writeFile.write("\nNone")
            writeFile.write("\nCommitMessages")
            #writeFile.write("\n"+ str(user.public_repos)) #Repos
            #writeFile.write("\n" + str(user.followers)) #followers
            #writeFile.write("\n" + str(user.following)) #following
            #writeFile.write("\n")
            repos = user.get_repos()
            #get_commit_messages(user.get_repos(), user.name)
            repocount=0
            for repo in repos:
                writeFile.write("\n" + str(repo.name))
                #writeFile.write("\n" + str(repo.forks_count))
                writeFile.write("\n" + str(repo.get_languages()))
                writeFile.write("\n" + repo.description.encode('utf8').replace("\t", " ").replace("\n"," "))
                #commits = repo.get_commits():
                writeFile.write("\n")
                count = 0
                for commit in repo.get_commits():
                    count = count + 1
                    if count > 60:
                        break
                    if commit.author is not None:
                        if commit.author.name == user.name:
                            writeFile.write("\t" + commit.commit.message.encode('utf8').replace("\t", "").replace("\n",""))
                repocount= repocount + 1
                if repocount > 15:
                    break
        break
        #we should only ever hit 1 user, so break 
    writeFile.close()

if __name__ == "__main__":
   main(sys.argv[1:])


