Critical Desire: To create a structure that allows the helmsman technique to be implemented across diverse projects to add structure to ideas, disambiguate concepts, create core terminology, enforce rules for agents, and ultimately allow many helmsman projects to work together. 

Critical Question: How to implement this in a way thats both flexible enough to allow Helmsman to change as needed while stoping divergence. 

Wants (all wants are sub-components of the critical desire):
- A git repo called Helmsman that 
- A source of truth for all helmsman projects 
- A way of quickly setting up helmsman projects 
- and whether the current helmsman project is synconized with the source of truth 
- A way for each helmsman project to understand what version of helmsman it's currently at and a way for it to read the change log and update itself. 
- A clear policy that forbids agents from adding certain jot documents into its context
- A clear policy that forbids agents from modifying certain helmsman documents without specific approval  

Question (all questions are sub-components of the critical question): 
- where should the ground truth for helmsman be stored?  
- what happens if I want to add or remove helmsman documents? How are these changes propogated 
- How should the version strings be stored? Perhaps we can use a git tagging system. Since helmsman, in itself, is a repo, it makes sense for it to also be a git for version control 

Capabilities: 
- A skill that setsup new helmsman project with the appropraite documents in a default state. 
- A version string that identifies different versions of helmsman projects. 
- A lot of version strings (like a git) 

