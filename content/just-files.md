Title: Just files
Date: 2020-03-19
Description: A virtualenv for system packages.
Status: Draft

![Archive - Photo by  Fabien Barral](/images/just-files.jpg "Archive - Photo by  Fabien Barral")

A package manager is a program that gets a bunch of files "packaged" in a certain format from a repository of packages and places them on a filesystem.

The manager part implies that it can keep track of installed packages, versions, dependencies, etc.

Packages are basically a box that contains files and metadata (checksums, content types, filepaths where to place the files, etc). Some may include compiled binaries or source files for building a project and testing it, reusable libraries, debug symbols, images, icons, documentation, songs, etc.

Guess what, plugins are also files, so your browser has a package-manager of sorts to handle those.

Different programming languages ship with their own package managers to install libraries: `pip` for Python, `cargo` for Rust, `npm` for node, etc.

A Linux distribution is a combination of a kernel + a package manager + a process manager. A kernel and a process manager can also be installed via the package manager, since they are also binary files.

So all you need to create a Linux distribution is just files, an a policy to manage those files.

Like applications do, each distribution establishes it's own policies on packaging. How files are packaged, a release cycle, a filesystem layout where those files get unpacked, a target architecture, etc.

Any package manager needs at least a dependency graph solver (semver maybe), filesystem inventory tracking and an archive format to transport files (tar balls maybe).

We could agree that there should be only one package manager to rule them all. After all different policies simply dictate how packages are built. And some configurations could make the package manager versatile enough to resolve versioning and extract those files.

But the ecosystem is very fragmented. Even within the Linux community, there are many different package managers. Policy and implementation gets mixed more often than not.

## Dependency hell
https://utcc.utoronto.ca/~cks/space/blog/linux/MicrosoftTeamsBadArrogance

As applications have plugin manager and dependencies, distributions have packages and dependencies too.
Like software which needs to be built + released, systems can also be built (packages installed) and released (services started, db migrations run, etc).

Over time there has been a shift to let developers ship their apps with their
own libraries and versions. Users also enjoy having the lates features and fixes.
The problem is that since traditional package managers maintain a global state
all packages need to be curated, or users would have to embrace the dependency hell.

That is why containers are on the raise today.

They tend to solve many issues:
- Bundle your own binaries and dependencies
- Ship them as a single artifact to any distro
- To avoid duplication and save disk space, docker uses layered images. So you download ubuntu once. But many containers use different base images and you can't delete files, images only grow since they are an append only log.
- Containers also allow sandboxing, limiting cpu, memory, network and filesystem access.

"The downside is that the approach works best when packages are aware of the Nix approach. But the packages have not been written with Nix in mind, and some work is needed per package to adapt to the approach."

https://drewdevault.com/dynlib.html -> sharing packages is ok, sharing libs is an overkill

Docker + docker-compose re implement a package distribution + process manager and orchestration + build system.

## Misc

https://lwn.net/Articles/821367/ Merkle trees and build systems

Transactional updates: https://www.youtube.com/watch?v=ureneyH06AE

We need a virtualenv but for system packages. Otherwise python, rust, javascript, etc re-implement the wheel over and over.



Reproducible builds come at the cost of more disk space, you need a lib which works fine with versions v0.[1-3], the user already installed v0.2 but you specified v0.1 in your dependencies, the user will get both copies installed (v0.1 and v0.2), even though only one was enough.

Como se hace la configuracion desde directorios globales para packetes dentro de nix? /etc/systemd/units/my-app.service?

Que pasa con los paquetes tradicionales cuando borras un servicio que es administrado por systemd?

https://cachix.org/
https://www.redox-os.org/news/pkgar-introduction/
https://github.com/whyrusleeping/gx



Qué pasa si dos librerías dependen de de una misma dependencia pero en distintas versiones, es el mismo caso que dos apps distintas dependan de distintas versiónes de una misma librería. Para esto es necesario los locks. Uno puede especificar versiones de depenencias con rangos.
Updates de seguridad implican actualizar todo? Si, sino se pierde la build reproducible. En fin: locks -> build reproducible

https://www.youtube.com/watch?v=4ua5aeKKDzU
https://en.wikipedia.org/wiki/Package_manager
https://en.wikipedia.org/wiki/PackageKit
Pakfile -> toml: contiene el listado de dependencias
Packfile.lock -> contiene el graph freezado de dependencias
un clon de nix en C y sin el DSL
http://holocm.org/
https://www.gobolinux.org/at_a_glance.html
https://wiki.archlinux.org/index.php/Pacman/Rosetta
https://micromind.me/en/posts/from-docker-container-to-bootable-linux-disk-image/
https://reproducible-builds.org/
https://www.tweag.io/posts/2020-05-25-flakes.html
https://ostree.readthedocs.io/en/latest/manual/related-projects/
https://xyrillian.de/thoughts/posts/argh-pm.html
https://www.microsoft.com/en-us/research/uploads/prod/2018/03/build-systems.pdf
https://dependabot.com/
https://nixos.org/nixos/nix-pills/
https://michael.stapelberg.ch/posts/2020-05-09-distri-hermetic-packages/
https://github.com/andrewchambers/hermes -> nix in c
https://github.com/spack/spack -> python package manager (https://spack.io/)

• mkpak is like makepkg (runs inside a chroot to build), it has a build.yml and a Pakfile with build dependencies. It could also output a container image or a tar.gz archive as a package.
• unpriviliged package management
• per-user profiles (Pak profiles are package groups (bundles of packages))
• atomic updates and rollbacks (update symlinks)
• reproducible builds (no es build tool, pero permite pinear dependencias en un Pakfile.lock)
• Not source-based but transparent binary downloads.

https://media.libreplanet.org/u/libreplanet/m/practical-verifiable-software-freedom-with-guixsd/
What if instead of using symlinks we used images mounts? https://distr1.org/
https://getkiss.org/
https://stefanoborini.com/current-status-of-python-packaging/
https://github.com/David-OConnor/pyflow
https://sedimental.org/the_packaging_gradient.html

https://www.youtube.com/watch?v=ULqoCjANK-I
For building: https://zserge.com/posts/containers/ (Linux containers in a few lines of code).

runpak a sandboxed runtime for a binary (is flatpak without big runtimes).

How to manage dotfiles and XDG-HOME, the user has to create those?

nix-thesis: https://edolstra.github.io/pubs/phd-thesis.pdf


## CLI

`--root` can change the default store directory.


Maybe each `pak [un]install <package-name==version>`

This uses a local `Pakfile` in the pwd, other files can be used by passing the `--pakfile=<path-to-pakfile>` param or `PAKFILE` environment variable.

All packages are installed in a store `/var/lib/pak/<package-name-and-version>/<package-md5-sum>/`.

`Pakfile` lists dependencies and package metadata. It is better that KISS packages that have one file for each metadatum (version, sources, checksums, etc)

We don't need checksums for every file inside the package, this integrity should be checked with the download file checksum and signature.

`package-name-version.pak.zst` is a tar file (zstd) with all the package content that needs to be extracted. Pak keeps track of all files. We can ask pak which package installed which file.

`pak env <envname>` enters the enviroment, and sets the `PAKFILE` env to `/usr/share/pak/envs/envname/Pakfile`.

It also creates symlinks in the global filesystem to all the files in the store. For example `/bin/nginx` is going to be a symlink to `/var/lib/pak/store/<package-name-and-version>/<package-md5-sum>/nginx`
Another possibility is that `pak env` puts you in a shell with `$PATH` env var pointing to the different binaries in the store?

`pak env --list` lists all available envs in `/usr/share/pak/envs/`

`pak run <commmand>` run the command within the environment

`pak update` updates all versions updating also the lock file

`pak update <package-name==version>` updates only the package name, updating also the lock file

`pak taste <package-name>` one off shell with the package installed

`pak search <package-name>` search

`pak gc` removes all unreachable packages from the store.

Hierarchy: package stores/environments/configs can be also defined in `~/.local/share/pak/`, etc.

Sandboxing GUI apps should be done with another binary that allows to set firewalls and also allow GUI interactions to happen via portals like in flatpak (https://github.com/containers/bubblewrap). Another example would be Opensnitch.



## How it works
Pak is a runtime environment manager.

> How the Nix user environment mechanism works. Essentially user environments are symlink trees that blend all currently installed packages into a single component so that they can be referenced from a single location. Another symlink layer manages generations of user environments. We can atomically switch between these generations by flipping symlinks. By adding the latter symlink to a user's PATH, packages can be automatically found without providing any absolute paths with hash codes in them that are difficult to remember.

Besides exposing packages in a user's PATH, Nix profiles are also used in NixOS to automatically find other resources, such as manual pages (through MANPATH) and KDE desktop menu items (through XDG_DATA_DIRS).
An environment is defined in a Pakfile it might list dependencies of `.pak` files that can be pinned in a Pakfile.lock

System directories should be mounted as RO. To avoid malicius packages from globally altering the system.

There are no optional dependencies or "extras", if something is optional it can be installed explicitly by the user.

## No hooks
Some package managers allow you to run scripts after installing a package. This should be done with oneshot scripts in systemd (like run migrations for example). There are no pre/post install scripts or hooks, these have to be commands that every package provides and a user or system needs to run.
https://michael.stapelberg.ch/posts/2019-07-20-hooks-and-triggers/ -> in order to get rid of some hooks we need to turn scripts into configuration. For example new users and password need to be a file (systemd-homed?). The man program should detect the need to re-run it's index.

https://www.youtube.com/watch?v=oPymb2-IXbg NixOS: How it works and how to install it!

http://www.cse.unsw.edu.au/~plaice/archive/WWW/1993/P-SPE93-Sloth.pdf

https://xkcd.com/2347/
https://jmmv.dev/2020/08/config-files-vs-directories.html
https://jmmv.dev/2020/08/database-directories.html

## Technology stack
Use python 3.8 + nuitka (give a talk: compyling).

Pakfile -> toml
Pakfile.lock -> json?

https://github.com/g-plane/tiny-package-manager

Transport layer: http, but eventually we could add ipfs/torrents/ssh.

Los packetes se pueden obtener de distintos repos/mirrors (http/ipfs/torrent/etc), that return a URI (http link, magnet link, etc) for a given key (package name)

## Dependency resolution
When does dependency resolution happen? Before downloading the packages or after downloading all dependencies in parallel?
When you say `pak install git`, we go get the `Pakfile.lock` for git. There we have a graph of all dependencies that we can compare with our local `Pakfile.lock` of our profile.
If there is a sub-dependency at any point that conflicts we show an error. If there are no conflicts, we can download in parallel every sub-dependency.