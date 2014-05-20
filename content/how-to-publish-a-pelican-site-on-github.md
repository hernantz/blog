Title: How to publish a pelican site on Github
Date: 2014-05-18 17:50
Category: Pelican
Tags: pelican, git
Slug: how-to-publish-a-pelican-site-on-github
Author: hernantz 
Summary: Step by step guide on how to publish a pelican website on Github


![Pelican a static site publishing tool](/static/images/pelican-a-static-site-publishing-tool-github.png)

This is a step by step guide on how to publish a pelican website on Github, and how not to get the site's
codebase so tightly coupled to where it is deployed. If in the future we want to publish it somewhere else
there isn't much to be changed. Another thing to mention is that even though we
reference pelican here, this process can be applied to almost any static site
generator tool.

1) Create a repository in github with exactly the following naming convention:
`your-github-username.github.io`

2) [Setup your pelican site](http://docs.getpelican.com/en/latest/install.html#kickstart-your-site) 
on a separate repository, ie my-blog, and [start adding content](http://docs.getpelican.com/en/latest/content.html#writing-content) to it.
You'll notice that the generated output goes by default to a folder (conveniently) named `output`,
but it can be changed to something else with the setting `OUTPUT_PATH` in your `pelicanconf.py` file

3) We will make use of "git submodules" to point our output directory to the 
repo created in step 1, so that it holds what's going to be published in github.
```bash
git submodule add https://github.com/username/username.github.io.git output
```

Adding a git submodule will create another version controlled file called `.gitmodules` with the following content:
```
[submodule "output"]
    path = output
    url = https://github.com/username/username.github.io.git
```

4) As the output directory is now managed by the independant git repository from step 1, we don't want to have to version-control 
it again from our pelican site repo. To ignore it just add a `ignore` statement like this:
```
[submodule "output"]
    path = output
    url = https://github.com/username/username.github.io.git
    ignore = all
```

5) Now every time you regenerate you site contents and want to publish them, cd to your output directory
and run git commands (like add, commit, push, etc) that will only take effect on your repo from step 1. Once you 
push your new output content to your master branch of `your-github-username.github.io`, Github will take 
some minutes to update your site.

Fin.
