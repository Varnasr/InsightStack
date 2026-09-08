# Codebook

5 variables, of which 4 are questions and 1 are form metadata or calculations.

| Variable | Type | Label |
|---|---|---|
| `personal/name` | text | What is your name? |
| `personal/age` | integer | How old are you? |
| `personal/gender` | select_one | Select your gender |
| `personal/hobby` | select_multiple | Select hobbies |
| `endnote` | note | Thank you for completing the survey! *(metadata)* |

## `personal/name`

**What is your name?**  
Type: `text`  
Hint: Enter your full name  

## `personal/age`

**How old are you?**  
Type: `integer`  
Hint: In completed years  
Asked when: `${age} >= 0`  
Constraint: `. >= 0`  

## `personal/gender`

**Select your gender**  
Type: `select_one` from list `gender`  

| Code | Label |
|---|---|
| `m` | Male |
| `f` | Female |

## `personal/hobby`

**Select hobbies**  
Type: `select_multiple` from list `hobbies`  
Hint: Tick all that apply  

| Code | Label |
|---|---|
| `reading` | Reading |
| `sports` | Sports |
| `music` | Music |

Exported as one space-separated string of selected codes; expand to one column per option before tabulating.

## `endnote`

**Thank you for completing the survey!**  
Type: `note`  
