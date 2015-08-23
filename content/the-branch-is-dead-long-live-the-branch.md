Title: The branch is dead, long live the branch!
Date: 2015-08-15
Category: Programming
Tags: ideas, agile, git
Summary: The bigger the branch gets, the harder it is to merge it.
Status: draft

*tl;dr*: When implementing big changesets, maintaining and merging long-lived
branches is hard. Use short-lived branches instead, and merge them ASAP.

![The ship of Theseus](/images/Ship.jpg)


## The Theseus paradox

> *"The ship of Theseus, also known as Theseus' paradox, is a thought experiment
> that raises the question of whether an object which has had all of its 
> components replaced remains fundamentally the same object."*
>
> <cite>[Ship of Theseus][1]</cite>. Wikipedia.

The answer to the paradox is easy if a large portion of the ship is replaced at
once, but it becomes more confusing if the change happens gradually, one plank
at a time. The answer to the paradox seems to be related to how those changes
are implemented.

On software projects, something similar occurs. There's a new requirement that
implies many changes, could be a refactor, a redesign or a new feature, that
can be implemented in small or huge stages.


## Branches for all

To implement these changes, collaboratively and simultaneously with other
developers (among other advantages) is that we use a version control system,
where each feature and sub task is implemented in its own branch.

Generally, every serious project also has an integration branch and a stable
branch, which may be the same [or not][4]. When the feature/redesign/refactor is
complete, the changes can be merged into the integration or stable branch.


## The problem with long-lived branches

The strategy of not integrating a branch until it is ready can lead to some
complications, especially when working with long-lived branches, where **these
complications become unnecessarily complicated**. Long-lived branches exist
because a big changeset needs to be implemented, and the merge is delayed for a
long time until all tasks are finished.

Let's review some of these complications that arise from working with
long-lived branches.


### 1. Merge conflicts

In a project with medium-sized team, the integration branch may have a higher
refresh rate, as smaller features or bugfixes get merged, that will cause
conflicts with the long-lived branch, which gets quite often out of sync.

Consider this scenario: *On a branch, some comments are added to a function.
On a second branch, the name of that function is changed and everywhere it is
invoked. On a third branch, the function declaration is moved to another file.*

This is an extreme example, I know, but even if you keep you are not **poluting
your branches with merges** (in git this would mean [using rebase][5]), and you
have managed to **avoid the merge hell** that makes your branch history look
like a [metro map][3], in general, **solving merge conflicts is hard**, and the
bigger the changeset is, the trickier it gets.


### 2. Sharing improvements between branches

Enhancements, refactors, bugfixes and other **improvements cannot be easily
shared between feature-branches** because they are WIP. Creating a common
*develop* branch, to integrate all WIP would require having all the features
finished in order to merge it into the integration branch, and thus, defeat the
purpose of using separate branches to enable parallel work.


### 3. Quality of code

Long branches have to be catching up with the ever changing integration branch,
and more often than not, you'll see lots of commits with messages like: *fixing
abc, fixing more abc, revert fixing abc, WIP broken tests*.

Because feature branches are in progress, documenting and testing are left as
last-minute tasks. You may think that the big messy branch will be prevented
from geting merged until it gets polished, but in reality, **code reviews
become code overviews**, and big changesets just [look fine][2]. Who dares to
approve a merge of *225 commits with 6,180 additions and 1,313 deletions that
affect 112 files*, and say it is DRY, well tested, etc?.


### 4. Big releases

It turns out that on personal projects and sometimes on many community driven
open-source projects, development is focused on big releases that are shipped
*when ready*. 

Following the analogy of the ship, this means that the ship won't set sail
until all work is finished. But for startups and technology based companies, it
happens that the ship is sailing! and it cannot wait on stand-by mode until it
is fixed, re-painted and it's oars replaced, all this must be done on the fly.

All the aforementioned pain points cannot be avoided but mitigated with enough
care and discipline, but this last one requires a mind change, commiting towards
**shipping something valuable** sprint by sprint.


## Always. Be. Merging. 

*Coffee is for mergers*. The quicker you merge a piece of code/feature/refactor, the better,
and for this, [the simpler][6] the branching model you adopt, the better.

Now when you plan a big changeset, dividing it into smaller tasks and start
working with the ones whom all the other tasks depend on, it's not enough. The key thing is that
**each task that is finished has to be mergeable**, and this implies that: 

1. Merge conflicts are resolved from day one.
2. Other features, refactores and bugfixes have to deal with or can make use of the new (quality working) code that is shipped sprint after sprint.
3. Changes might not be tackled in the original logical order, but the transition towards the big changeset happens in a smooth and predictable manner.


Ejemplos como hacer una migracion de a partes

1. Traducir la applicacion a otro idioma
2. Hacer un upgrade de bootstrap
3. Cambio de widgets y layout
4. Un cambio donde se usen feature flags
5. Cambiar el nombre a una clase que se usa mucho (usar un alias) 


## Conclusion

Hable particularmente sobre branches, pero en general estas ideas se aplican a cualquier 
forma de integrar cambios es un projecto de software. Especialemente cuando la aplicacion ya esta en uso.
Implement big changesets little by little. Don't let Theseus' ship sink!


[1]: https://en.wikipedia.org/wiki/Ship_of_Theseus "Ship of Theseus"
[2]: https://twitter.com/iamdevloper/status/397664295875805184 "Code reviews"
[3]: http://www.tugberkugurlu.com/archive/resistance-against-london-tube-map-commit-history-a-k-a--git-merge-hell "Merge Hell"
[4]: http://nvie.com/posts/a-successful-git-branching-model/ "Git Flow"
[5]: https://www.atlassian.com/git/tutorials/merging-vs-rebasing/workflow-walkthrough "Merging vs Rebasing"
[6]: http://scottchacon.com/2011/08/31/github-flow.html "Github Flow"
