Types

This regex entries define which words are from which type.

Sentences

The place for knowledge in language form.

-------------- Advanced stuff --------------

Repres(Representation)

Which word types are a sort of variable (things, what, something, and other abstract words) and which words mean the same?

Ops(Operators)

Special cases of words which correspond to logical operators, for example "or" and "and" (may not exist in such a pure form in all natural languages).

Rules

By default the system generates them when it hears synonymous sentences,
it tries to reduce new grammatical structures to a combination of known ones,
Rules describes the mapping between grammatical structures and logical meaning (with an optional command argument).

----- Profi stuff (can change the behavior of the system fundamentally) -------

Axioms

Here you can define additional axioms of thought (FOL) to the included ones in MOM0.1.py BaseAxioms.

CustomCode

Here you can define Python functions called by the optional command argument of the Rules with access to the Request function which makes it easy to collect the needed knowledge before starting a procedural custom algorithm.

Note

Most of the definition file is also trainable by simply chatting to the AI,
but sometimes an adjustment of the deffile is needed. (For example if you want to define custom algorithms or the system understood a synonymity wrong)