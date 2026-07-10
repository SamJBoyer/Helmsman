<helmsman-summary>

This is a Helmsman project.

Helmsman is an idea-to-product developement pipeline designed to faciliate collaboration between developers and agents. Helmsman works by taking basic, unstructured ideas about wants and questions and passing them through multiple layers of structuring until they become actionable. 

Helmsman projects have a tag that tells which canon version of the document they're using. Look in the .helmsman/hVersion.md for this version.

HELMSMAN.md should be kept consistent to the canonical tagged version, and glossary.md should have the required sections and terms. 

</helmsman-summary>

<repo-structure>

Helmsman Repo Structure: 

.helmsman/
- .chronicle/
- hVersion.md 

hDocs/
- artifacts.md
- glossary.md
- jot.md
- master.md
- overlay.md 
- questions.md
- status.md
- wants.md
HELMSMAN.md
AGENTS.md
jot.md

Helmsman projects should always be git projects. They should have 2 branches by default:
- main: branch with the most recent functional project 
- dev: the branch with active development. agents merge work trees to the dev branch. only a human can merge to main, or an agent with explicit permission

NEVER read the jot.md file. This is human ONLY file for keeping notes. 
NEVER edit file in the hDocs folder without EXPLICIT permission. 

</repo-structure>

<documents>

Read every document in hDocs 

hDocs contain the following documents:
- glossary 
- artifacts
- master
- overlay 
- status
- questions
- wants

how to use each document:

<glossary>

Glossary contains the canon definitions used in a project. Glossary, by default, has 3 sections: 
- terms: project specific dictionary of important terms used in scope. These terms are to be used aggressively in code to develop a shared language between the agent and developer. terms section of glossary is the ground truth for such definitions
- itags: itag stands for issue-tags. issue-tags refer to the tag in the repository git issues page and are used to demarkate types of issues. 
- hLabels: colored emoji squares that demarkate different ideas connected laterally instead of hyierarchically. 

do: 
- ask if you’re unsure of terms
- check if an itag already exists before making a new one 
do not:
 - ever add new terms or modify term definitions without asking for explicit permission 

</glossary>

<wants>

wants is a file that has a list of things the developer “wants” to happen in this project. it is a jot down of the current desires before made actionable. this file serves as a dynamic and changing quick file for the developer to jot down their desires before more work is put in to make it actionable.

</wants>

<master>

summary of the project. this file explains what the project should do. essentially high level document. also has assumptions

</master>

<status>

this document explains where the project currently is from the perspective of the developer. this document is an important truth control that bridges what the project should do in the documents, and the state of the actual code. documents are aspirational and upward facing. we always write in our documents what should happen what should be the case. the code is what’s actually the case. often times the developer knows that the code reality of the code doesn’t match the aspirations of the docs. status is a document to make explicit what actually developer thinks about the code and what they view as the next steps to convert reality if the code into the aspirations of the docs

</status>

<overlay>

Explains which other projects are important to this one and how they interact at a high level 

</overlay >

<questions>

things i’m not sure about that i want to record 

</questions>

<artifacts>

previous significant changes stored in a log. this should be used when weird behavior emerges or it’s unclear why an architectural decision was made, as it might be an artifact from a previous version. this document should be used before looking at git history 

</documents>