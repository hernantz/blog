Title: Introducing Pak
Date: 2020-03-19
Description: A virtualenv for system packages.
Status: Draft

A distribution is a combination of a kernel + a package manager + a process manager.
Each distribution establishes it's own policies on packaging, release cycle, filesystem layout, etc.

Some package managers allow you to run scripts after installing a package. This should
be done with oneshot scripts in systemd (like run migrations for example).

A package manager is a program that gets a bunch of files (binaries, images, etc) from somewhere (a package) and distributes them on a filesystem (your pc for example). The manager part implies that it can keep track of installed packages, versions, etc. Packages are archives that contain files and metadata, the metadata specifies where to place the files. 

Transactional updates: https://www.youtube.com/watch?v=ureneyH06AE

We need a virtualenv but for system packages. Otherwise python, rust, javascript, etc re-implement the wheel over and over.

Documentation should teach, not tell.
Reprocible builds come at the cost of more disk space, you need a lib which works fine with versions v0.[1-3], the user already installed v0.2 but you specified v0.1 in your dependencies, the user will get both copies installed (v0.1 and v0.2), even though only one was enough.

Qué pasa en Nix con paquetes que cambian de acuerdo a la arquitectura o SO -> Son packetes distintos.
Cómo se hace configuración, man pages, etc en Nix, symlinks igual que con binarios?

https://cachix.org/
https://www.redox-os.org/news/pkgar-introduction/
https://github.com/whyrusleeping/gx

Packages can contain arch independent files like images or docs.
Some may include source files for building the project and testing it.

Qué pasa si dos librerías dependen de de una misma dependencia pero en distintas versiones, es el mismo caso que dos apps distintas dependan de distintas versiónes de una misma librería.

Updates de seguridad implican actualizar todo? Si, sino se pierde la build reproducible

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
https://ostree.readthedocs.io/en/latest/manual/related-projects/
https://xyrillian.de/thoughts/posts/argh-pm.html
https://www.microsoft.com/en-us/research/uploads/prod/2018/03/build-systems.pdf
https://dependabot.com/
https://nixos.org/nixos/nix-pills/

• unpriviliged package management
• per-user profiles
• atomic updates and rollbacks
• reproducible builds
• source-based with transparent binary downloads
https://media.libreplanet.org/u/libreplanet/m/practical-verifiable-software-freedom-with-guixsd/
What if instead of using symlinks we used images mounts? https://distr1.org/
https://getkiss.org/
https://stefanoborini.com/current-status-of-python-packaging/
https://github.com/David-OConnor/pyflow
https://sedimental.org/the_packaging_gradient.html
https://github.com/g-plane/tiny-package-manager
https://www.youtube.com/watch?v=ULqoCjANK-I

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


pak --lock should create a Pakfile.lock?

Maybe each pak install <package-name==version> --lock

Do you have to be in the same dir where the Pakfile is?

Pakfile lists dependencies and package metadata. It is better that KISS packages that have one file for each metadatum (version, sources, checksums, etc)

pak shell enters the enviroment

pak run <commmand> run the command within the enviroment


Sandboxing GUI apps should be done with another binary that allows to set firewalls and also allow GUI interactions to happen via portals like in flatpak (https://github.com/containers/bubblewrap). Another example would be Opensnitch.


Docker + docker-compose re implement a package distribution + process manager and orchestration + build system.
