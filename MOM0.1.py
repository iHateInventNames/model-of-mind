from subprocess import Popen, PIPE, STDOUT
import re,os
from MOM_def import *
ReplaceRequest(lambda s,arg: [d.split("=")[1].replace(",","") for d in eval(PrettyTell(s)) if "=" in d and d.split("=")[0]==arg])
regexp_tag=lambda w: (j[1] for j in Types if re.match(j[0],w)!=None).next()
print "I'm MOM, a general AI system created by Patrick Hammer! If you want me to output all my knowledge, write KNOWLEDGE, if you want to save it write SAVE\n"
Knowledge=[]; BaseAxioms=""":-op(700,xfx,<-).
:-op(450,xfx,..).
:-op(1100,yfx,&).
Vs<-[Var | Dec] :- findall(Var,maplist(call,[Dec]),Vs).
mem(mom,you,0).
len(A,B,T) :- Li<-[W| mem(W,A,T)], length(Li,Z), B=Z, B\==0.
len(A,B,T) :- Li<-A, len(Li,B,T).
do(A,B,C,T,P) :- mem(A,Z,T), do(Z,B,C,T,P).
iss(A,B,T,P) :- mem(A,B,T).
iss(A,B,T,P) :- mem(A,Z,T), mem(Z,B,T).
doestimes(X,Action,B,Times,T) :- W<-[K|(mem(K,B,T),do(X,Action,K,T,P))],length(W,Times),Times\==0.
doestimes(X1,Action1,B1,Z,T) :- current_predicate(doestimesxmorethan/8), doestimesxmorethan(X1,Action1,B1,More,X2,Action2,B2,T), doestimes(X2,Action2,B2,Times2,T),Z is Times2+More.
doestimesmorethan(A,Action,B,X,Bction2,Y,T) :- doestimes(A,Action,B,N,T), doestimes(X,Bction2,Y,M,T), N>M.
getval(X,Y,T) :- (number(X),Y=X);(iss(X,Y,T,P1),number(Y)). %lets define when something is probable true in a set of elements:
probable(M,H,NH,S,T):-G<-[E|mem(E,M,T)],L<-[F|(mem(F,M,T),(iss(F,H,T,P);do(F,H,S,T,P2)))],D<-[V|(mem(V,M,T),(iss(V,NH,T,P3);do(V,NH,S,T,P4)))],length(D,U),length(L,Z),length(G,N),U==0,2*Z>N,N\==0.
plan(A,V,B,T,N,Path):-call_with_depth_limit((V=is,iss(A,B,T,P);do(A,V,B,T,P2)),N,R),(number(R),reverse(P,Path);(R=depth_limit_exceeded,K is N+1,plan(A,V,B,T,K,Path))). %planning
"""

def Question(a,syntax,ret,bOtherQuestion,bWhen,bWhy,bHowMany,bWhat,bHow,bPlan,MaxResults=100,MaxDepth=100):
	rs=Popen('swipl -q -f MOM_pl.pl', shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT).communicate("leash(-all),"+
	("trace," if not bPlan else "")+ret.split("A")[1]+"."+(("\n;".join("" for z in range(MaxResults))) if bHow==False and bPlan==False else ""))[0]
	ReasWHEN=set([]); ReasWHY=set([]); Ansli=set([]); M=["Call:","Fail:","Exit:","Redo:"]
	for l in M: rs=rs.replace(l,"\n"+l)
	for a in rs.split("\n"): #read the proof, succeeded goals in the reason predicate list are reasons, in answer mode add answers
		if "=" in a and "HERE" not in a and True not in [b in a for b in M]: Ansli.add(a.replace(".","").replace(" ","").replace("?",""))
		if "Exit:" in a and a.split(") ")[1].split("(")[0] in Reasons and "=" not in a: ReasWHY.add( a.split(") ")[1])
		if "Fail:" in a and a.split(") ")[1].split("(")[0] in Reasons and "=" not in a: ReasWHEN.add(a.split(") ")[1])
	if not bWhen and not bWhy and not bHowMany and not bWhat: return True if "true" in rs.replace(" ","") else "No/ne"
	if bWhy:  return re.sub(r'(\,|\s|\(|\))',' '," and ".join(r for r in ReasWHY  if r.replace(" ","")!=ret.split("A")[1].replace(" ",""))) if bHow or "true"  in rs.replace(" ","") else ""
	if bWhen: return re.sub(r'(\,|\s|\(|\))',' '," and ".join(r for r in ReasWHEN if r.replace(" ","")!=ret.split("A")[1].replace(" ",""))) if "true"      not in rs.replace(" ","") else ""
	return Ansli if not bHowMany else len(Ansli)

def SplitAndCombineMeaning(syntax,s,Offset):
	r2,r1,b1,c=(((("A"+Tell(s.split(c)[0],Recursion=True,Offset=Offset))).split("A"),("A"+Tell(c.join(s.split(c)[1:]),Recursion=True,Offset=Offset+len(
	[j for j in s.split(c)[0].split(" ") if j!=""])+1)).split("A"),b[1],c) for b in Ops for c in b[0] if c in s).next()
	return r2[len(r2)-1].replace("T0","T0")+" "+b1.replace(",",". " if ":-" in r1[len(r1)-1] else ",")+" "+r1[len(r1)-1]

def AssumeReferences(syntax,words):  #if something like it or he or she is used, use the last noun we talked about (maybe better strategies one day)
	global lastNoun
	for u in range(len(syntax)):
		if u in range(len(syntax)) and syntax[u]=="N" and (u-1<0 or (syntax[u-1]!="IS" and syntax[u-1]!="N")): lastNoun=words[u]
		if syntax[u]=="REF": words[u],syntax[u]=lastNoun,"N"
	return " ".join(syntax),words

def AddSynonym(syntax,a,means): #add a synonymous sentence (much todo here) example: patrick is a cat = a cat patrick is
	global Rules
	try:#search for the equivalent words in the new sentence and update the indices in the meaning expression
		li=[ind.split("}")[0] for ind in means.split("{") if "}" in ind] 	     #old indices
		li2=[str(synonymli.index(a[int(li[i])])) for i in range(len(li))]        #new indices
		Rules+=[[lastSyntax,"".join([h.split("{")[0]+("{"+li2[i]+"}" if i<len(li2) else "") for i,h in enumerate(means.split("}")) if h!=""])]] #index replaced, pattern add
	except: print "(I don't understand the synonymity)"

def TrainTagger(bQuestion,Rs):
    global Types,Repres
    if len(Rs)==2 and not bQuestion:                                          #simple not grammatic dependent word learning 
        if Rs[0].isupper(): Repres+=[(Rs[0]," "+Rs[1]+" ")]; return True      #bicycle CYCLE; fahhrad CYCLE; CYCLE cycle => cycle=bicycle=fahrrad
        if Rs[1].isupper(): Types=[("("+Rs[0]+")$",Rs[1])]+Types; return True #word CATEGORY, CATEGORY word, example^

def AddKnowledge(ret):
    global Knowledge
    newknol=ret.replace("A",",").replace("T0","T0" if ":-" in ret else "0")
    Knowledge+=sum([[kn+"." for kn in newknol.split(", ") if kn!=""] if ":-" not in newknol else [newknol+"."]],[])
    with open("MOM_pl.pl", "w") as text_file: text_file.write(BaseAxioms+"\n"+Axioms+"\n"+"\n".join(Knowledge))

def GetMeaning(syntax,s,Offset):
    try: 
        ret2=[b[1] for b in Rules if len(syntax.split(" "))==len(b[0].split(" ")) and not False in [x in y for x,y in zip(syntax.split(" "),b[0].split(" "))]][0]
        for i,h in enumerate(re.finditer(r'\{([0-6]*)\}',ret2)): ret2=ret2.replace(h.group(0),"{"+str(int(h.group(0).replace("{","").replace("}",""))+Offset)+"}")
    except: ret2=str(SplitAndCombineMeaning(syntax,s,Offset))
    return ret2

synonymadd=False; synonymli=[]; lastSyntax=""; SInput=[]; lastNoun=""
def Tell(s,ret="",Recursion=False,AddToSentences=True,Offset=0): 
    global Knowledge,synonymadd,synonymli,lastSyntax,SInput
    bQuestion,Rs="?" in s,s.split(" ")
    if TrainTagger(bQuestion,Rs): print "Thank you for correcting me and training my tagger."; return ""
    if not Recursion and not bQuestion and AddToSentences: SInput+=[s]
    s=s.replace("?"," ").replace("."," ").replace(" ","  ") #which words of which type are in s:
    x_wd_in_s=lambda tp:["\s"+w+"\s" for w in [re.sub(r'(\$|\(|\))','',h) for h in sum([(g[0]+"|").split("|") for g in Types if g[1]==tp],[])] if " "+w+" " in " "+s+" " and w!='']
    for wordtype,replacement in Repres: #create boolean variables and rewrite word types instances according to the Repres rules
		exec wordtype+"=x_wd_in_s('"+wordtype+"');\nb"+wordtype+"="+wordtype+"!=[] if not Recursion else b"+wordtype in locals(),globals()
		s=eval("re.sub(r'('+'|'.join("+wordtype+")+')','"+replacement+"',' '+s+' ').replace(' not  ',' not')  if "+wordtype+"!=[] else s")
    words=[z for z in s.split(" ") if z!=""]; syntax=map(regexp_tag,words)
    syntax,words=AssumeReferences(syntax,[d[1]+str(d[0]) if len(d[1])==1 and d[1].isupper() else d[1] for d in enumerate(words)]) #also replace N V and such with enumerated vars
    try:
		ret2=GetMeaning(syntax,s,Offset)
		ret2,command=ret2.split("$") if "$" in ret2 else (ret2,"")
		ret=ret2.format(*words) if not Recursion else ret2
		if bQuestion and not "None" in ret and not Recursion:
			return Question(words,syntax,(ret if "A" in ret else "A"+ret).replace("T0",("T0" if bHOW or bPLAN else "0")),"n" in words,bWHEN,bWHY or bHOW,bNUM,bWHAT or bPLAN,bHOW,bPLAN)
		elif not Recursion: AddKnowledge(ret)
		exec (command.format(*words) if not Recursion else "") in locals(),globals()
		synonymadd=(AddSynonym(syntax,words,ret2) and False) if synonymadd and not Recursion else synonymadd
		return ret
    except:
		synonymli,synonymadd,lastSyntax=words,True,syntax
		print "I don't understand the form "+syntax+", tell me something synonymous or add a rule."

def PrettyTell(txt,ret=""): #make some syntactic modifications here if needed or pretty printing
	global SInput
	Sp=[a[0][0] for a in Ops if a[2]=="ENUMERATION"][0]
	if Sp in txt:
		SInput+=[txt]    #enumeration syntactic sugar, maybe use regex groups for it one day
		lu=[o for o in txt.split(Sp) if o!=""] #split after the enumeration symbol
		a=[list(reversed(lu[0].split(" ")))[0]]+lu[1:len(lu)-1]+[lu[len(lu)-1].split(" ")[0]] #but use only the last from the first and the first from the last split and tell all
		for h in a: ret+=str(Tell(" ".join(list(lu[0].split(" ")[0:len(lu[0].split(" "))-1]))+" "+h+" "+(" ".join(list(lu[len(lu)-1].split(" ")[1:]))),AddToSentences=False))+"\n"
	else: ret=str(Tell(txt))
	return ret

if os.path.exists("MOM_pl.pl"): os.remove("MOM_pl.pl")
[PrettyTell(Sentence) for Sentence in Sentences]
while 1!=0:
	txt=raw_input("you: ")
	if txt=="KNOWLEDGE" or txt=="SAVE":
		toWrite=("def ReplaceRequest(R): exec 'def Request(s,arg=\"N0\"): return R(s,arg)' in locals(),globals()\n#Representations (type,transform), as what should words of type get transformed to? to variables, words?\nRepres="+str(Repres)+
		"\n# Logic Operators (words,syntax,type)\nOps="+str(Ops))+("\n# Word Types (word_regex,Type)\nTypes="+str(Types)+
		"\n#Reasons - which predicates are relevant as reasons to the why question?\nReasons="+str(Reasons)+"\n#Sentence Structures [WordTypes,"+
		"Meaning,Description]\n"+"#in sentences the left part of A in Meaning is for assumptions, else its just a &, and the part after $ is a python cmd(T0 for now(time)):\nRules="+str(Rules)+
		"\n#FOL axioms MOM system doesn't include \nAxioms=\"\"\""+Axioms+"\"\"\"\n#Procedural Knowledge\nCustomCode=\"\"\""+CustomCode+"\"\"\"\nexec CustomCode\n#Language Knowledge\nSentences="+str(SInput).replace(", '",",\n'")).replace(", (",",\n(").replace(", [",",\n[")
		if txt=="SAVE":
			with open("MOM_def.py", "w") as def_file: def_file.write(toWrite)
		else: print toWrite
	else:
		print str(PrettyTell(txt))
