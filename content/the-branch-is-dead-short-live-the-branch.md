Title: The branch is dead, short live the branch!
Date: 2015-08-28
Category: Programming
Tags: ideas, agile, git
Summary: Implement big changesets little by little. Don't let Theseus' ship sink!

*tl;dr*: When implementing big changesets, maintaining and merging long-lived
branches is hard. Use short-lived branches instead, and merge them ASAP.

![The ship of Theseus](/images/ship.jpg)


## The Theseus paradox

> *"The ship of Theseus, also known as Theseus' paradox, is a thought experiment
> that raises the question of whether an object which has had all of its 
> components replaced remains fundamentally the same object."*
>
> <cite>[Ship of Theseus][1]</cite>. Wikipedia.

The answer to the paradox seems to be related to how those changes are
implemented. It is easy if a large portion of the ship is replaced at once, but
it becomes more confusing if the change happens gradually, one plank at a time.

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
complications become unnecessarily complicated**.

Long-lived branches exist because a big changeset needs to be implemented, and
the merge is delayed for a long time until all tasks are finished.

Let's review some of these complications that arise from working with
long-lived branches.


### 1. Merge conflicts

In a project with a medium-sized team, the integration branch may have a higher
refresh rate, as smaller features or bugfixes get merged, that will cause
conflicts with the long-lived branch, which gets quite often out of sync.

Consider this scenario: *On a branch, some comments are added to a function.
On a second branch, the name of that function is changed and everywhere it is
invoked. On a third branch, the function declaration is moved to another file.*

This is an extreme example, I know, but even if you you are not **polluting your
branches with merges** (in git this would mean [using rebase][5]), and you have
managed to **avoid the merge hell** that makes your branch history look like a
[metro map][3], in general, **solving merge conflicts is hard**, and the bigger
the changeset is, the trickier it gets.


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

Because feature branches are *work in progress*, documenting and testing are
left as last-minute tasks. You may think that the big messy branch will be
prevented from geting merged until it gets polished, but in reality, **code
reviews become code overviews**, and big changesets just [look fine][2]. Who
dares to approve a merge of *225 commits with 6,180 additions and 1,313
deletions that affect 112 files*, and say it is DRY, well tested, etc?.


### 4. Big releases

It turns out that on personal projects and sometimes on many community driven
open-source projects, development is focused on big releases that are shipped
*when ready*. 

Following the analogy of the ship, this means that it won't set sail until all
the work is finished. But for startups and technology based companies, it
happens that the ship is sailing! and it cannot wait on stand-by mode until it
gets fixed, re-painted and it's oars replaced, all this must be done on the fly.

All the aforementioned pain points cannot be avoided but mitigated, with enough
care and discipline, but this last one requires a mind change, commiting towards
**shipping something valuable** sprint by sprint. This becomes especially
important once the app is already being used because of the unpredictable
[nature of software projects][8], where priorities and requirements change quite
often, and the branch could be left incomplete at any time.


## Always. Be. Merging. 

*Coffee is for mergers*. The quicker you merge a piece of code/feature/refactor,
the better, and for this, [the simpler][6] the branching model you adopt, the
better.

When you plan a big changeset, dividing it into smaller tasks and start working
with the ones whom all the other tasks depend on, it's not enough. The key
thing is that **each task that is finished has to be mergeable**, and this
implies that:

1. Merge conflicts are resolved from day one.
2. Other features, refactores and bugfixes have to deal with or can make use of
   the new (good quality? working?) code that is shipped sprint after sprint.
3. Changes might not be tackled in the original logical order, but the
   transition towards the big changeset happens in a smooth and predictable
   manner.

Dispite having mentioned branches a lot, the ideas expressed here still apply,
no matter the technique used to integrate the changes.


## Some examples of smooth transitions

I think I've gotten to the point already, but I felt like sharing some examples,
without getting into too much detail, of real life scenarios where requirements
are implemented by using other strategies than long-lived branches.

Among all the [strategies available][7] to **migrate an Python app from Python 2
to Python 3**, I would try to modify the code so that it runs under both Python
2 and Python 3  as much as I can. I certaintly wouldn't create a
*python-3-migration* branch to do all the work there, because chances are that
your Python 2 app would still be used for a long time until the migration is
finished, and you'll have to be duplicating features, bugs and bugfixes in your
main branch and in the migration branch.

To **translate the app** into another language, you can start by notifying the
entire team that translation is in progress so that each new piece of ui that is
added has the labels modified to be translatable.

The customer wants **a redesign of the site** (change colors and layouts), and
decides take the opportunity to also to upgrade to the latest version of
Bootstrap. Do not! Upgrade Bootstrap first and then do the redesign. But the
[upgrade must live][9] with the previous version for a while, so [compile your
own version][10], merge that and then start the migration, page by page.

When **renaming a class** that is used everywhere, is better to just create an
alias for that class and simply commit that change. From then on, make every
developer use the alias for the new code and at last, when all the codebase is
using the alias, rename the original class.

Finally, you could try **feature flags or compile time flags**, to [enable or
disable certain parts][11] of the system depending on some conditions, but
keeping all the parts integrated in the same codebase.


[1]: https://en.wikipedia.org/wiki/Ship_of_Theseus "Ship of Theseus"
[2]: https://twitter.com/iamdevloper/status/397664295875805184 "Code reviews"
[3]: http://www.tugberkugurlu.com/archive/resistance-against-london-tube-map-commit-history-a-k-a--git-merge-hell "Merge Hell"
[4]: http://nvie.com/posts/a-successful-git-branching-model/ "Git Flow"
[5]: https://www.atlassian.com/git/tutorials/merging-vs-rebasing/workflow-walkthrough "Merging vs Rebasing"
[6]: http://scottchacon.com/2011/08/31/github-flow.html "Github Flow"
[7]: http://python3porting.com/strategies.html "Migration strategies"
[8]: http://projectcartoon.com/cartoon/1 "How Projects Really Work"
[9]: http://slides.com/pamelafox/when-bootstrap-attacks "When bootstrap attacks"
[10]: http://ruby.bvision.com/blog/please-stop-embedding-bootstrap-classes-in-your-html "Please stop embedding Bootstrap classes in your HTML!"
[11]: http://blog.travis-ci.com/2014-03-04-use-feature-flags-to-ship-changes-with-confidence/ "Using Feature Flags to Ship Changes with Confidence"
