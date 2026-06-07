What is Helmsman? 

Helmsman is my software factory using the cursor system. It contains the guis and basically just everythign I need to work very effectively on every system. It should be portable and use containers as much as possible to be as portable as possible.  

Helmsman.. its unclear what does or does not go into helsman at the moment. It probably needs multiple repos. It should have a repo for the dev container. It should have a repo for skills. It should have a repo for the ralph loops and basic harnesses. It would probably also be good to have.. actually lets flush it out. 

Dev-container: Repo with the code needed to set up a docker 
dev container with my dev tools and env. It can be connected to cursor via vscode's attatch to running session 
- Why is this a seperate module? we want to keep it light weight. so there are situations where I'd want to be able to have my env up and running where I wouldn't want to download everything else. 
- Ai stuff might be large and take a while to download which interfers with being flexible and portable. 
- So this is a decision boundry. Things get split up when 
    1. they require seperate dependencies that conflict with eachother and have a heavy dependencies. 
    2. They have different auth and need different levels of secret injection. Should this auth seperating be lateral or verticle? or does such a thing really exist? 


Agent-tools: Repo with code needed to set up agent stuff: 
- Prompts
- Harness code
Questions? 
- How to use REDIS in orchestration? 
- Should it be a library? 

Oh I need the skills repo here too. 


Ok so what should helsman do? 

Containers:
- Dev-container
- REDIS server 
- MCP toolkit 

