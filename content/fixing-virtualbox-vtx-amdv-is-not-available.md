Title: Fixing VirtualBox VT-X or AMD-V is not available
Date: 2014-04-10 22:36
Category: Programming
Tags: linux, virtualization, virtualbox
Summary: Fix issue with native virtualization technologies in VirtualBox
Status: draft

This warning/error started to appear in VirtualBox v4.3, where using Intel's
VT-X and AMD's AMD-V native virtualization technologies is set to enabled by
default on every VM. You computer may or may not have these goodies.

Check the output of these commands to verify this in case you are not sure:

```sh
grep --color vmx /proc/cpuinfo  ## for an Intel processor
grep --color svm /proc/cpuinfo  ## for an AMD processor
```

In case you have support for VT-x or AMD-v, you will see an option to enable
the virtualization in the BIOS, and after doing that the problem is solved.

![Enable virtualization in BIOS](/images/BIOS-enable-virtualization.png)


In case you do not have support for VT-x or AMD-v, you can disable that feature.
The configuration file for your VM is in `/path/to/vm/files/myvmname/myvmname.vbox`
(where myvmname is your VM name n_n).

It is an xml, but it states that you should not modify it directly becouse
changes won't take effect, so we have to use other tools, such as the VirtualBox
UI or VBoxManage.  As that option didn't appear in the UI, I had to go with the
VBoxManage command line tool. To disable Hardware Virtualization I run the
following command:

```sh
VBoxManage modifyvm myvmname --hwvirtex off
```

In case you run more configuration problems and your current virtualbox ui does
not display, just check:

```sh
VBoxManage --help | less
```

and for sure you will be able to configure almost anything.

*-BIOS image taken from: [http://askubuntu.com/a/256853](http://askubuntu.com/a/256853)*
