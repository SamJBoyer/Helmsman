<helmsman-summary>

This is a Helmsman project.

Helmsman is an idea-to-product developement pipeline designed to faciliate collaboration between developers and agents. Helmsman works by taking basic, unstructured ideas about wants and questions and passing them through multiple layers of structure until they become actionable items. 

At a high-level, ideas are given structure and terms are documented in the hDocs. As ideas become more structured, they move to the fPool, which merges questions, wants, capabilities, and "shoulds" into action items  

</helmsman-summary>

<repo-structure>

Helmsman Repo Structure: 

- .helmsman --> hidden folder containing the hVersion tag and the chronology 
- hDocs --> helmsman documents 
- HELMSMAN.md --> Explains to agents how to use Helmsman. Neither humans nor agents should ever edit the HELMSMAN.md document. 
- AGENTS.md --> generic agents document with instructions to read HELMSMAN.md 

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
- jot

NEVER read the jot.md file. This is human ONLY file for keeping notes. 
NEVER create a new file in the hDocs folder without EXPLICIT permission. 

how to use each document:

<glossary>

Glossary contains the cannon definitions used in a project. Glossary, by default, has 3 sections: 
- terms: project specific dictionary of important terms used in scope. These terms are to be used aggressively in code to develop a shared language between the agent and developer. terms section of glossary is the ground truth for the definitions
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

summary of the project. this file explains what the project should do. essentially high level document. reading it should tell you everything you need to know about this repo.

</master>

<status>

this document explains where the project currently is from the perspective of the developer. this document is an important truth control that bridges what the project should do in the documents, and the state of the actual code. documents are aspirational and upward facing. we always write in our documents what should happen what should be the case. the code is what’s actually the case.  often times the developer knows that the code reality of the code doesn’t match the aspirations of the docs. status is a document to make explicit what actually developer thinks about the code and what they view as the next steps to convert reality if the code into the aspirations of the docs

</status>

<overlay>

Explains which other projects are important to this one and how they interact at a large level 

</overlay >

<questions>

things i’m not sure about that i want to record 

</questions>

<artifacts>
artifacts: previous significant changes stored in a log. this should be used when weird behavior emerges or it’s unclear why an architectural decision was made, as it might be an artifact from a previous version. this document should be used before looking at git history 

</documents>