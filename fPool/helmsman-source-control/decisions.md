
Decision name: ground-truth 

Question: 
- where should the ground truth for helmsman be stored?  
- How should the version strings be stored? Perhaps we can use a git tagging system. Since helmsman, in itself, is a repo, it makes sense for it to also be a git for version control 


Answer: on github. versions should be maintained using git tags, and helmsman projects should have a .helmsman/version.md file with the tag that created it. 
