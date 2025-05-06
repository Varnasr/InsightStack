# Generated Codebook


## `name`
**Label:** What is your name?

**Type:** text name

**Hint:** Enter your full name

**Constraint:** ``

**Relevant if:** ``



## `age`
**Label:** How old are you?

**Type:** integer age

**Hint:** In completed years

**Constraint:** `. >= 0`

**Relevant if:** `${age} >= 0`



## `gender`
**Label:** Select your gender

**Type:** select_one gender gender

**Hint:** 

**Constraint:** ``

**Relevant if:** ``

**Choices:**
- `m`: Male
- `f`: Female


## `hobby`
**Label:** Select hobbies

**Type:** select_multiple hobbies hobby

**Hint:** Tick all that apply

**Constraint:** ``

**Relevant if:** ``

**Choices:**
- `reading`: Reading
- `sports`: Sports
- `music`: Music


## `endnote`
**Label:** Thank you for completing the survey!

**Type:** note endnote

**Hint:** 

**Constraint:** ``

**Relevant if:** ``

