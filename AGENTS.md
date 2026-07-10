Read @HELMSMAN.md

Skills are found in the Skillet submodule. Whenever you update a skill in the Skillet, write a git commit with a descriptive message, push to main, then use the skillet-link/pull-master to propogate the change to the repo in the .cursor/skill-set directory (which teh symlink points to), so all repos have global access 

Skill policy:

We store our skills in a central repo called Skillet. This repo is a submodule in helmsman, and is cloned to the user/.cursor/skill-set folder so its accessible everywhere. We have a symlink called 
skillet-link. Skillet has scripts to easily pull the 
origin. This way, we can modify scripts in our submodule, push them, then call the Skillet/pull-master scripts to sync the changes and make them global

Never modify canon without asking 