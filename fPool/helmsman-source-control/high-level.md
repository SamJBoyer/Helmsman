Critical Desire: To create a structure that allows the helmsman technique to be implemented across diverse projects to add structure to ideas, disambiguate concepts, create core terminology, enforce rules for agents, and ultimately allow many helmsman projects to work together. 

Critical Question: How to implement this in a way thats both flexible enough to allow Helmsman to change as needed while stoping divergence. 

Wants (all wants are sub-components of the critical desire):
- A git repo called Helmsman that contains the ground truth version of helmsman. As helmsman evolves, new complete versions of helmsman will be marked with tags in git. Instances of helmsman will have the tag id in the .helmsman/version.md document based off the version of helmsman used to create it. 
- Helmsman projects should have some mechanism that allows it to transfer from version to version. 
- and whether the current helmsman project is synconized with the source of truth 
- A clear policy that forbids agents from modifying certain helmsman documents without specific approval  

Question: 
- what happens if I want to add or remove helmsman documents? How are these changes propogated 
- how should the create a helmsman skill work? it would be very dumb to store the helmsman documents in the skill, where does it find the source of truth? 

Capabilities: 
- A skill that setsup new helmsman project with the appropraite documents in a default state. 
- A version string that identifies different versions of helmsman projects. 

Todo:
[ ] remove hanging documents 
[ ] clean up terminology
[ ] proof read  

Should:
- hVersion tags should be descriptive 
