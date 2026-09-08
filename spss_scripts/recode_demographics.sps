
* Recode Gender and Education into usable categories.
RECODE gender (1='Male') (2='Female') INTO gender_recoded.
RECODE edu (1='None') (2='Primary') (3='Secondary') (4='Higher') INTO edu_recoded.
EXECUTE.
