def ReplaceRequest(R): exec 'def Request(s,arg=\"N0\"): return R(s,arg)' in locals(),globals()
#Representations (type,transform), as what should words of type get transformed to? to variables, words?
Repres=[('PLAN', ' plan '), ('HOW', ' '), ('WHY', ' '), ('WHEN', ' '), ('IRRELEVANT', ' '), ('WHAT', ' N '), ('DET', ' '), ('NUM', ' N '), ('IS', ' is ')]
# Logic Operators (words,syntax,type)
Ops=[([', '], '', 'ENUMERATION'), (['if'], ':-', 'IF'), (['and'], ',', 'AND'), (['or'], ';', 'OR')]
# Word Types (word_regex,Type)
Types=[('(was|be|gets|is|are)$', 'IS'),
('(why)$', 'WHY'),
('(when)$', 'WHEN'),
('(how)$', 'HOW'),
('(plan)$', 'PLAN'),
('(after)$', 'AFTER'),
('(it|he|she|they)$', 'REF'),
('(would|actually|immediately|that|the|a|an|in|on|to|of|inside|onto|under|can)$', 'IRRELEVANT'),
('(not)$', 'NOT'),
('(probable)$', 'PROBABLE'),
('(much|many)$', 'NUM'),
('(more|\\+|plus)$', 'ADD'),
('(what|who|where|which|someone|something|somewhere|some|any|anything|anywhere|things|all|does)$', 'WHAT'),
('.*', 'N')]
#Reasons - which predicates are relevant as reasons to the why question?
Reasons=['do', 'iss']
#Sentence Structures [WordTypes,Meaning,Description]
#in sentences the left part of A in Meaning is for assumptions, else its just a &, and the part after $ is a python command(T0 for now(time)):
Rules=[['N', '{0}', 'maybe a prolog question? debugging? be careful!'],
['N IS N', 'mem({0},{2},T0) A iss({0},{2},T0,P)', 'house is old'],
['PLAN N IS N', 'plan({1},{2},{3},T0,1,Path)', 'plan house is old?'],
['N IS N AFTER N IS N', 'iss({0},{2},T0+1,Path):- iss({4},{6},T0,P),append([{4},is,{6}],P,Path)', 'trafficlight is red after it is green'],
['N N N AFTER N N N', 'do({0},{1},{2},T0+1,Path):- do({4},{5},{6},T0,P),append([{4},{5},{6}],P,Path)', 'trafficlight gets red after it gets green'],
['N N', 'do({0},{1},unspecified,T0,P)', 'panther kill'],
['N N N', 'do({0},{1},{2},T0,P)', 'panther kill stefan'],
['N N N N', 'doestimes({0},{1},{3},{2},T0)', 'gimpa burns 4 tires'],
['N IS N N', 'len({3},{2},T0)', 'there are 5 houses'],
['N N ADD N N N N N', 'doestimesmorethan({0},{1},{3},{5},{6},{7},T0)', 'what has more feet than cat has eye?'],
['N N N N ADD N N N N', 'doestimesxmorethan({0},{1},{3},{2},{6},{7},{8},T0)', 'tiger has 2 feet more than cat has eye'],
['N IS N IS PROBABLE', 'probable({0},{2},not{2},nix,T0)', 'humans are red is probable?'],
['N N N IS PROBABLE', 'probable({0},{1},not{1},{2},T0)', 'humans kill pigs is probable?']]
#FOL axioms (Prolog) MOM system doesn't include 
Axioms=""""""
#Procedural Knowledge
CustomCode=""""""
exec CustomCode
#Language Knowledge
Sentences=[]
