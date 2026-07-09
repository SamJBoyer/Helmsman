---

# Merging thoughts in the thought pool

Often when enunciating throughts, I realize that 2 ideas I assumed were independent actually share enough overlap that they should be merged into a single thought. A common pattern of this is when 1 thought has many wants and questions and a different one has few wants or questions. In this case, merging the thin thought into the larger one is appropriate 

example of a thin thought: 

Critical Desire: to have a simple way to setup a new helmsman project 

Critical Question: what should a new helmsman project have 


wants:
- when a new helmsman project is created with a glossary, it should automatically have the i-tag definition in glossary 
- when setting up helmsman, it should auto init the docs with some default 

questions:

This ultimately got merged into the much fuller thought: 

Critical Desire: to create a source of truth for all helmsman projects that clearly defines what each document is for, how both humans and agents should use the document structure, rules and regulations on modifying certain documents, and whether the current helmsman project is synconized with the source of truth 

Critical Question: How to implement this in a way thats both flexible enough to allow Helmsman to change as needed while stoping divergence. 

Wants (all wants are sub-components of the critical desire):
- A way for each helmsman project to understand what version of helmsman it's currently at and a way for it to read the change log and update itself. 
- A clear policy that forbids agents from adding certain jot documents into its context
- A clear policy that forbids agents from modifying certain documents without specific approval  
- A skill that sets up a helsman project in a new repo 


Question (all questions are sub-components of the critical question): 
- where should the ground truth for helmsman be stored?  
- what happens if I want to add or remove helmsman documents? How are these changes propogated 