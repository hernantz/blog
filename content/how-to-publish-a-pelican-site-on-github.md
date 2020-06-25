Title: How to publish a pelican site on Github
Date: 2014-05-18
Category: Programming 
Tags: pelican, git, python
Summary: Step by step guide on how to publish a pelican website on Github.


![Pelican a static site publishing tool](/images/pelican-a-static-site-publishing-tool-github.png)

This is a step by step guide on how to publish a pelican website on Github, and
how not to get the site's codebase so tightly coupled to where it is deployed.
If in the future we want to publish it somewhere else, there isn't much to be
changed. Another thing to mention is that even though we reference pelican
here, the process I'll show you can be applied to almost any static site
generator tool.

1) Create a repository in Github following this exact naming convention:
`username.github.io`

2) [Setup your pelican site][1] on a separate repository, ie my-blog, and
[start adding content][2] to it. You'll notice that the generated output goes
by default to a folder (conveniently) named *output*, but it can be changed to
something else with the `OUTPUT_PATH` setting in your `pelicanconf.py` file

3) We will make use of *git submodules* to point our output directory to the
repo created in step 1, so that it holds what's going to be published in Github.

```bash
git submodule add https://github.com/username/username.github.io.git output
```

Adding a git submodule will create another version controlled file called
`.gitmodules` with the following content:

```
[submodule "output"]
    path = output
    url = https://github.com/username/username.github.io.git
    ignore = all
```

As the output directory is now managed by the independent git repository
from step 1, we don't want to have to version-control it again from our pelican
site repo, and that's why we added the last *ignore* statement.

4) Pelican has two types of configuration files, `pelicanconf.py` for general
settings, and `publishconf.py` that is used for publishing, as you probably
guessed. Pelican's Makefile comes with a built-in command to generate the
output that will be published:

```bash
make publish  # generates output using publishconf.py
```

But before running it, make sure the following settings are in `publishconf.py`:

```python
# don't delete our .git submodule dir
DELETE_OUTPUT_DIRECTORY = False

# use the correct abs url
SITEURL = 'http://username.github.io'
RELATIVE_URLS = False
```

**Heads up!** Pelican regenerates the output automatically when running the http
server and making changes to the contents. So `make publish` should be the last
command to be run before releasing.

5) Now every time you regenerate your site contents and want to publish them, cd
to your output directory and run git commands (like add, commit, push, etc).
Those commands will only take effect on your repo from step 1, because you are
inside the output submodule. Once you push your new output content to your master
branch of `username.github.io`, Github will take some minutes to update your site.
And that's it.

Happy blogging!


[1]: http://docs.getpelican.com/en/latest/install.html#kickstart-your-site
[2]: http://docs.getpelican.com/en/latest/content.html#writing-content
