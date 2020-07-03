Title: Introducing Pak
Date: 2020-03-19
Description: A virtualenv for system packages.
Status: Draft

A distribution is a combination of a kernel + a package manager + a process manager.
Each distribution establishes it's own policies on packaging, release cycle, filesystem layout, etc.

Some package managers allow you to run scripts after installing a package. This should
be done with oneshot scripts in systemd (like run migrations for example).

A package manager is a program that gets a bunch of files (binaries, images, etc) from somewhere (a package) and distributes them on a filesystem (your pc for example). The manager part implies that it can keep track of installed packages, versions, etc. Packages are archives that contain files and metadata, the metadata specifies where to place the files. 

https://lwn.net/Articles/821367/ Merkle trees and build systems

Transactional updates: https://www.youtube.com/watch?v=ureneyH06AE

We need a virtualenv but for system packages. Otherwise python, rust, javascript, etc re-implement the wheel over and over.

Documentation should teach, not tell.
Reprocible builds come at the cost of more disk space, you need a lib which works fine with versions v0.[1-3], the user already installed v0.2 but you specified v0.1 in your dependencies, the user will get both copies installed (v0.1 and v0.2), even though only one was enough.

Qué pasa en Nix con paquetes que cambian de acuerdo a la arquitectura o SO -> Son packetes distintos.
Cómo se hace configuración, man pages, etc en Nix, symlinks igual que con binarios?

https://cachix.org/
https://www.redox-os.org/news/pkgar-introduction/
https://github.com/whyrusleeping/gx

https://michael.stapelberg.ch/posts/2019-07-20-hooks-and-triggers/ -> in order to get rid of some hooks we need to turn scripts into configuration. For example new users and password need to be a file (systemd-homed?). The man program should detect the need to re-run it's index.

Packages can contain arch independent files like images or docs.
Some may include source files for building the project and testing it.

Qué pasa si dos librerías dependen de de una misma dependencia pero en distintas versiones, es el mismo caso que dos apps distintas dependan de distintas versiónes de una misma librería. Para esto es necesario los locks. Uno puede especificar versiones de depenencias con rangos.
Updates de seguridad implican actualizar todo? Si, sino se pierde la build reproducible. En fin: locks -> build reproducible

https://www.youtube.com/watch?v=4ua5aeKKDzU
https://en.wikipedia.org/wiki/Package_manager
https://en.wikipedia.org/wiki/PackageKit
Pakfile -> toml: contiene el listado de dependencias
Packfile.lock -> contiene el graph freezado de dependencias
un clon de nix en C y sin el DSL
http://holocm.org/
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

• unpriviliged package management
• per-user profiles (Pak profiles are package groups (bundles of packages))
• atomic updates and rollbacks
• reproducible builds (no es build tool, pero permite pinear dependencias en un Pakfile.lock)
• source-based with transparent binary downloads
https://media.libreplanet.org/u/libreplanet/m/practical-verifiable-software-freedom-with-guixsd/
What if instead of using symlinks we used images mounts? https://distr1.org/
https://getkiss.org/
https://stefanoborini.com/current-status-of-python-packaging/
https://github.com/David-OConnor/pyflow
https://sedimental.org/the_packaging_gradient.html
https://github.com/g-plane/tiny-package-manager
https://www.youtube.com/watch?v=ULqoCjANK-I
For building: https://zserge.com/posts/containers/ (Linux containers in a few lines of code)

Over time there has been a shift to let developers ship their apps with their
own libraries and versions. Users also enjoy having the lates features and fixes.
The problem is that since traditional package managers maintain a global state
all packages need to be curated, or users would have to embrace the dependency hell.

That is way containers are on the raise today.

They tend to solve many issues:
- Bundle your own binaries and dependencies
- Ship them as a single artifact to any distro
- To avoid duplication and save disk space, docker uses layered images. So you download ubuntu once. But many containers use different base images and you can't delete files, images only grow since they are an append only log.
- Containers also allow sandboxing, limiting cpu, memory, network and filesystem access.

"The downside is that the approach works best when packages are aware of the Nix approach. But the packages have not been written with Nix in mind, and some work is needed per package to adapt to the approach."

nix-thesis: https://edolstra.github.io/pubs/phd-thesis.pdf

`pak --lock` should create a Pakfile.lock?

--root can change the default store directory.

there are no optional dependencies, if something is optional it can be installed explicitly by the user.

Maybe each `pak [un]install <package-name==version> --lock`

This uses a local `Pakfile` in the pwd, other files can be used by passing the `--pakfile=<path-to-pakfile>` param or `PAKFILE` environment variable.

All packages are installed in a store `/var/lib/pak/<package-name-and-version>/<package-md5-sum>/`.

`Pakfile` lists dependencies and package metadata. It is better that KISS packages that have one file for each metadatum (version, sources, checksums, etc)

`package-name-version.pak.zst` is a tar file (zstd) with all the package content that needs to be extracted. Pak keeps track of all files. We can ask pak which package installed which file.

`pak env <envname>` enters the enviroment, and sets the `PAKFILE` env to `/usr/share/pak/envs/envname/Pakfile`

`pak env --list` lists all available envs in `/usr/share/pak/envs/`

`pak run <commmand>` run the command within the enviroment

`pak update` updates all versions updating also the lock file

`pak update <package-name==version>` updates only the package name, updating also the lock file

`pak taste <package-name>` one off shell with the package installed

`pak search <package-name>` search

`pak gc` removes all unreachable packages from the store.

Hierarchy: package stores/environments/configs can be also defined in `~/.local/share/pak/`, etc.


Sandboxing GUI apps should be done with another binary that allows to set firewalls and also allow GUI interactions to happen via portals like in flatpak (https://github.com/containers/bubblewrap). Another example would be Opensnitch.

https://drewdevault.com/dynlib.html -> sharing packages is ok, sharing libs is an overkill

Docker + docker-compose re implement a package distribution + process manager and orchestration + build system.

https://utcc.utoronto.ca/~cks/space/blog/linux/MicrosoftTeamsBadArrogance

Los packetes se pueden obtener de distintos repos/mirrors (http/ipfs/torrent/etc), that return a URI (http link, magnet link, etc) for a given key (package name)


Pak is a runtime environment manager.
An environment is defined in a Pakfile it might list dependencies of `.pak` files that can be pinned in a Pakfile.lock

System directories should be mounted as RO. To avoid malicius packages from globally altering the system.

https://www.youtube.com/watch?v=oPymb2-IXbg NixOS: How it works and how to install it!

Like software which needs to be built + released, systems can also be built (packeages installed) and released (services started, db migrations run, etc).

http://www.cse.unsw.edu.au/~plaice/archive/WWW/1993/P-SPE93-Sloth.pdf


Use python 3.8 + nuitka