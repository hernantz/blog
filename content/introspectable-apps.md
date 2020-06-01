Title: Introspectable apps
Date: 2013-07-03
Category: Personal
Tags: programming, ideas
Summary: Thinking apps as functions.
Status: draft

Programmers know the convinience of using libraries.
Reusable pieces of code.
Can we provide the same convinience to our users?
Usually this means building a API.
For CLI applications we can simply spawn a new shell and call the right methods.
BUt for GUI apps this is not possible.
But what if instead every app, be it GUI or CLI used the D-bus. D-bus would the api to call and coordinate applications in your desktop.
It could also expose a socket to coordinate apps from the network.
Imagine a webrtc channel in your DBUS session.

GUI apps need to be built differently for this. Here is were the idea of using redux, where every change in the GUI is represented by intents.
The gui simply sends intents to the Redux server via the DBUS session and the server responds.

All of the sudden we can implement diffent external middlewares and plugins, without having to modify the GUI of the app.

this idea is also implemented to some degree by neovim (sever to process text and external guis that communicate via msgpack) or GIMP et al, with the.

So apps would become little engines that can be extended or combined (like functions or libraries) while GUIs, CLIs and Websites are simply interfaces to those engines via a COM Bus.

This could also help expose databases.

Another way to instrospect apps is if they use standard data formats, like exposing a sql database or simply use files on disk like .md, .json, .txt etc

Connecting computers and sharing data/applications and commands would be a matter of opening sockets to stream channels.

The bus could be also used for streaming replication over the network.

Yes there might be an overhead on complexity and performance.

The bus is a repl, apps are libraries (or collections of functions), the user is the new developer.

We have some of that with Zapier and Integromat.

[1]: https://www.expressionsofchange.org/reification-of-interaction/
[2]: https://www.brandonsmith.ninja/blog/libraries-not-frameworks
[3]: https://orndorffgrant.com/own-your-data-idea/
