:- include("db.pl").

sentence(sent(Noun_P, Verbal_P)) --> noun_phrase(Noun_P), verbal_phrase(Verbal_P).
sentence(sent(NP_Plural, VP_Plural)) --> noun_phrase_p(NP_Plural), verbal_phrase_p(VP_Plural).

noun_phrase(noun_phrase(Det_F, Noun_F)) --> determiner_f(Det_F), noun_f(Noun_F).
noun_phrase(noun_phrase(Det_M, Noun_M)) --> determiner_m(Det_M), noun_m(Noun_M).

noun_phrase(noun_phrase(Noun_F)) --> noun_f(Noun_F).
noun_phrase(noun_phrase(Noun_M)) --> noun_m(Noun_M).

noun_phrase_p(noun_phrase(Noun_FP)) --> noun_p_f(Noun_FP).
noun_phrase_p(noun_phrase(Noun_MP)) --> noun_p_m(Noun_MP).

noun_phrase_p(noun_phrase(Det_FP, Noun_FP)) --> determiner_p_f(Det_FP), noun_p_f(Noun_FP).
noun_phrase_p(noun_phrase(Det_MP, Noun_MP)) --> determiner_p_m(Det_MP), noun_p_m(Noun_MP).

noun_phrase_p_det(noun_phrase(Det_FP, Noun_FP)) --> determiner_p_f(Det_FP), noun_p_f(Noun_FP).
noun_phrase_p_det(noun_phrase(Det_MP, Noun_MP)) --> determiner_p_m(Det_MP), noun_p_m(Noun_MP).

verbal_phrase(verbal_phrase(Verbal_P)) --> verb(Verbal_P).
verbal_phrase(verbal_phrase(Verbal_P, Noun_P)) --> verb(Verbal_P), noun_phrase(Noun_P).
verbal_phrase(verbal_phrase(Verbal_P, Prep, Noun_P)) --> verb(Verbal_P), preposition(Prep) , noun_phrase(Noun_P).
verbal_phrase(verbal_phrase(Verbal_P, Prep, NP_Plural)) --> verb(Verbal_P), preposition(Prep), noun_phrase_p_det(NP_Plural).
verbal_phrase(verbal_phrase(Verbal_P, Prep_P, NP_Plural)) --> verb(Verbal_P), preposition_p(Prep_P), noun_phrase_p(NP_Plural).

verbal_phrase_p(verbal_phrase_p(VP_Plural)) --> verb_p(VP_Plural).
verbal_phrase_p(verbal_phrase_p(VP_Plural, NP_Plural)) --> verb_p(VP_Plural), noun_phrase_p(NP_Plural).
verbal_phrase_p(verbal_phrase_p(VP_Plural, Prep, Noun_P)) --> verb_p(VP_Plural), preposition(Prep), noun_phrase(Noun_P).
verbal_phrase_p(verbal_phrase_p(VP_Plural, Prep, NP_Plural)) --> verb_p(VP_Plural), preposition(Prep), noun_phrase_p_det(NP_Plural).
verbal_phrase_p(verbal_phrase_p(VP_Plural, Prep_P, NP_Plural)) --> verb_p(VP_Plural), preposition_p(Prep_P), noun_phrase_p(NP_Plural).
