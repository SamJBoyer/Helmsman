This is project was created with Helmsman. Read every document in @docs/ 


how to use the documents in docs: 

----

glossary:
terms: project specific dictionary of important terms used in scope. These terms are to be used aggressively in code to develop a shared language between the agent and developer. terms section of glossary is the ground truth for the definitions

do: 
- ask if you’re unsure of terms
do not:
 - ever add new terms or modify term definitions without asking for explicit permission 
diagrams: helmsman makes aggressive use of diagrams. lucid chart is the preferred diagram service, and the ground truth diagrams ALWAYS live in lucid chart. NOT IN THIS PROJECT. the diagrams section contains the title of the diagrams, a description of what the diagram contains, a summary of when to refer to the diagram, a link to the lucid chart diagram and any relevant info needed to link from the local repo to the lucid chart ground truth, and a direction to any cached diagrams. 

---

git-tech: 

A document explaining how agents should use github, what each branches do, and norms around this repo. Always read this before interacting with github

 ---
wants:
wants is a file that has a list of things the developer “wants” to happen in this project. it is a jot down of the current desires before made actionable. this file serves as a dynamic and changing quick file for the developer to jot down their desires before more work is put in to make it actionable.

---
high-level:
summary of the project. this file explains what the project should do. essentially high level document. reading it should tell you everything you need to know about this repo.

---
status:
this document explains where the project currently is from the perspective of the developer. this document is an important truth control that bridges what the project should do in the documents, and the state of the actual code. documents are aspirational and upward facing. we always write in our documents what should happen what should be the case. the code is what’s actually the case.  often times the developer knows that the code reality of the code doesn’t match the aspirations of the docs. status is a document to make explicit what actually developer thinks about the code and what they view as the next steps to convert reality if the code into the aspirations of the docs

---
overlay: document listing which other helmsman projects are important to this one and how they interact at a large level 

---
questions:
things i’m not sure about that i want to record 

---
git-tech: a stated log of how i want git to be used in this project 

---
artifacts: previous significant changes stored in a log. this should be used when weird behavior emerges or it’s unclear why an architectural decision was made, as it might be an artifact from a previous version. this document should be used before looking at git history 

---
Ehan document: (everything has a nature): document about higher-level or philosophical thoughts about the nature of the system we’re implementing 

