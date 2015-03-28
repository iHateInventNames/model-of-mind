It tries to combine (not as a collection but as whole working unit) different AI algorithms such that it can not only deduce logically, but also understand many concepts of applied (math) first order theories, for example estimate if something is probable or not and use induction, understanding numbers, action-related planning (by iterative deepening which guarantees completeness) in time and space, answering "why" questions, understand and learn new language, and where its easy to manage the knowledge and to extend it, it's also easily possible to add command patterns (which can also reference the system itself in a intiutive way: Cars=Request("what has 4 tires and it has a motor?") and Cars will be a Python string list of all known cars) which execute code. So far projects of this sort failed because of code complexity, too less modularity and flexibility, and because they are often more a algorithm collection than a working architecture) so far, this projects tries to keep things as easy and predictable and easily manageable as possible, it's already useful and stable, the main interface to the system is with the language defined in the def file.


<<<>>>Example dialogs:<<<>>>

>>>Karatemaster dialog: (default def file)<<<

you: dad, sebastian is pleased if the coffee is good

you: dad tried the coffee

you: when dad would be pleased?

if is coffee good at t=now

you: guenther goes to the school after dad tried the coffee

you: guenther is a karatemaster if he goes karate

you: guenther goes karate after he goes to school

you: how guenther gets karatemaster?

by do dad tried coffee at t=now and do guenther goes school at t=1 and
> do guenther goes karate at t=2 and is guenther karatemaster at t=2

you: something died if it was in the coffee and dad tried the coffee

you: the fly was in the coffee

you: the fly died?

True

you: the coffee was good

you: why dad was pleased?

because is coffee good at t=now

you: the crumb was in the coffee

you: what was in the coffee?

crumb, fly

you: guenther is karatemaster?

No/ne (note: because he is karatemaster in t+2 but not now already)

you: the dog has 4 feet and guenther has 2 feet

you: the dog has more feet than guenther has feet?

True

you: dad, sebastian are human

you: human are pleased is probable?

True

you: why human are pleased is probable?

because is sebastian pleased at t=now and is dad pleased at t=now and is coffee good at t=now



>>>Graph example:<<< (default def file)

![http://upload.wikimedia.org/wikipedia/commons/5/5b/6n-graf.svg](http://upload.wikimedia.org/wikipedia/commons/5/5b/6n-graf.svg)

you: in g 4 connects with 6

I don't understand that, tell me something synonymous.

you: g is 6 after g is 4 and g is 4 after g is 6 (now with that definition the rest of the graph)

you: in g 3, 5 connects with 4 and in g 5 connects with 1

you: in g 1, 3, 5 connects with 2

you: g is 6  (the start point)

you: plan g is 1? (answer from the AI:)

at first g is 6, then g is 4, then g is 5, then g is 1



>>>Shell example:<<< (shell def file which is just an extension to the default def file)

you: directory1 is '/home/tc'

you: list directory1

file listing...