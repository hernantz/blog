Everything in this universe can be further improved ad infinitum, and so is the Architecture of a program.
At some point the cost of improving it will not provide as much value so someone has to say this is good enough, for some definition of good.

That decision is not easy, so that is why technical debt is something you have to live with.

Hay tres tipos de deuda tecnica.
1. The good. Producto de no hacer optimizaciones tempranas -> muy bien

2. The bad. Producto de explorar ideas dentro de tu codigo. Codigo a medio terminar,
a/b testing que perdura en el tiempo. Esto esta muy mal.
Existen mejores formas de probar si algo puede funcionar o no. y es con experimentos satelite.
Usar servicios que cuestan como mucho $50 dolares, integromat, ziggeo, s3, mailchimp, buttercms, google sheets, etc. You can put together this services in a sattlelite project just to try out new ideas. Create reports from scratch using some scripting, do things manually.
Don't get your engineering team pollute the main codebase, you will acquire unnecessary technical debt.
Your codebase will be a graveyard of many ways of doing something.
https://letterstoanewdeveloper.com/2019/04/01/the-best-code-is-no-code/

3. THe ugly. This is a product of bad engineering, big-O, etc. Newbies programming. Lack of wisdom about data structures, using wrong tools, wrong abstractions, etc. Seniority helps to address this type of debt.