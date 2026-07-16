<Terms>

<helmsman-terminology>

hDocs: shorthand for helmsman documents. 

itags: itag stands for issue-tags. issue-tags refer to the tag in the repository git issues page. Helmsman makes heavy use of git issues as a cheap and accessible way to create tickets related to the project. As a result, there are many different tags used to designate which issues mean which thing. For example, issues may be marked as ideas, features, bugs, etc. itag may have shared definitions between projects and repo-unique definitions. The itag section is the ground truth for what each tag means, which tags are used, and when to use each tag.

iticket: an instance of a git issue that has an itag

iPool: a document that contains a variably-structured list of thoughts, ideas, questions, and wants. Typically will live inside a lucidchart. Look at hDocs/remotes#lucidchart section to check for a remote iPool document.

critical desire: lives in the fPool. Is a 2 sentence summary of the most important desire the piece of infrastructure will fufill. All wants in the 

critical question: a 2 sentence summary of the fundemental uncertainty that balances a critical desire

</helmsman-terminology>

<helmsman-version-control>

hVersion: The official version of helmsman currently used in this hProject OR the last official version used in this hProject. hVersion can be checked by looking at .helmsman/hVersion.md which contains the hTag 

hTag: the tag that indicates the hVersion. This matches an official canonical version found in the Helmsman github. The hTag will always be formatted vX.Y.Z and mathces a git tag.

canonical version: an official helmsman release tagged on the github. These releases are finished, polished, and documented to offer a standardized starting point for new helmsman projects and a way to compare drift 
in an individual hProject to a baseline.

</helmsman-version-control>

<misc-features>

hlabel: stands for helmsman label. Uses colored emojis to mark certain ideas. [ ] 

hLabels are available and [X] hLabels are taken. If an hLabel is taken, it needs to have
a defined name and useage. 

</misc-features>


</Terms>

bug: something that is broken or behaving incorrectly. marked with the bug tag on git issues

quickssue: a quick, low-ceremony issue captured from casual input without deep investigation. marked with the quickssue tag on git issues

wonders: an open curiosity or "I wonder if..." question worth capturing for later exploration, not yet an idea or commitment. marked with the wonders tag on git issues
 
</iTags>
<hLabels>

[ ]: 🔴 #EA4335, [label], [useage]
[ ]: 🟠 #FF6D01, [label], [useage]
[ ]: 🟡 #FBBC04, [label], [useage]
[ ]: 🟢 #34A853, [label], [useage]
[ ]: 🔵 #4285F4, [label], [useage]
[ ]: 🟣 #9334E9, [label], [useage]
[ ]: 🟤 #A14236, [label], [useage]
[ ]: ⚫ #000000, [label], [useage]
[ ]: ⚪ #FFFFFF, [label], [useage]
[ ]: 🟥 #EA4335, [label], [useage]
[ ]: 🟧 #FF6D01, [label], [useage]
[ ]: 🟨 #FBBC04, [label], [useage]
[ ]: 🟩 #34A853, [label], [useage]
[ ]: 🟦 #4285F4, [label], [useage]
[ ]: 🟪 #9334E9, [label], [useage]
[ ]: 🟫 #A14236, [label], [useage]
[ ]: ⬛ #000000, [label], [useage]
[ ]: ⬜ #FFFFFF, [label], [useage]

</hLabels>