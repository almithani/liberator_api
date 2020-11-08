# liberator_api

API for liberator sites

## dev notes

I keep losing my dev workflow, so here's some info for you Al:

* check out local password storage system for any credentials you'll need. The entry is called "Liberator client/server"
* your local folder is using Sublime Text w/ Sublime SFTP to upload to the live site automatically
    * it doesn't look like the staging site is attached to anything =x
* to see changes, you'll need to restart uwsgi with `service uwsgi reload`
* when you're happy with the changes push from remote server to git (local folder is not under source control)
