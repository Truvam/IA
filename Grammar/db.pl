determiner_f(determiner_f('A')) --> ['A'].
determiner_f(determiner_f(a)) --> [a].

determiner_m(determiner_m('O')) --> ['O'].
determiner_m(determiner_m(o)) --> [o].

determiner_p_f(determiner_p_f('As')) --> ['As'].
determiner_p_f(determiner_p_f(as)) --> [as].

determiner_p_m(determiner_p_m('Os')) --> ['Os'].
determiner_p_m(determiner_p_m(os)) --> [os].

noun_f(noun(cidade)) --> [cidade].
noun_f(noun(floresta)) --> [floresta].
noun_f(noun(mae)) --> [mae].
noun_f(noun(menina)) --> [menina].
noun_f(noun(noticia)) --> [noticia].
noun_f(noun(porta)) --> [porta].
noun_f(noun(vida)) --> [vida].

noun_m(noun(cacador)) --> [cacador].
noun_m(noun(cachorro)) --> [cachorro].
noun_m(noun(mar)) --> [mar].
noun_m(noun(martelo)) --> [martelo].
noun_m(noun(rio)) --> [rio].
noun_m(noun(rosto)) --> [rosto].
noun_m(noun(sino)) --> [sino].
noun_m(noun(tambor)) --> [tambor].
noun_m(noun(tempo)) --> [tempo].
noun_m(noun(vento)) --> [vento].

noun_p_f(noun(lagrimas)) --> [lagrimas].
noun_p_f(noun(meninas)) --> [meninas].

noun_p_m(noun(lobos)) --> [lobos].
noun_p_m(noun(tambores)) --> [tambores].

verb(verb(bateu)) --> [bateu].
verb(verb(corre)) --> [corre].
verb(verb(correu)) --> [correu].

verb_p(verb_p(bateram)) -->[bateram].
verb_p(verb_p(corriam)) -->[corriam].
verb_p(verb_p(correram)) -->[correram].

preposition(preposition(com)) --> [com].
preposition(preposition(na)) --> [na].
preposition(preposition(nas)) --> [nas].
preposition(preposition(no)) --> [no].
preposition(preposition(para)) --> [para].
preposition(preposition(pela)) --> [pela].
preposition(preposition(pelo)) --> [pelo].