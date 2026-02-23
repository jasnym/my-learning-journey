# ============================================================
# SYNTAX COMPARISON: Basic/Pascal  vs  Python
# Session 1.1 — Python vs. My Old Languages
# ============================================================


# ------------------------------------------------------------
# 1. PRINTING OUTPUT
# ------------------------------------------------------------
# Basic:   PRINT "Hello"
# Pascal:  WriteLn('Hello');
# Python:
print("Hello, Milan!")


# ------------------------------------------------------------
# 2. VARIABLES — no type declaration needed in Python
# ------------------------------------------------------------
# Basic:   DIM name AS STRING  /  name = "Milan"
# Pascal:  var name: string;   /  name := 'Milan';
# Python:  just assign — Python figures out the type itself
name = "Milan"
age = 45
height = 1.80        # float (decimal number)
is_learning = True   # boolean — True or False (capital T/F)

print(name, age, height, is_learning)


# ------------------------------------------------------------
# 3. STRING FORMATTING — putting variables inside text
# ------------------------------------------------------------
# Basic:   PRINT "Hello " & name
# Pascal:  WriteLn('Hello ' + name);
# Python option A — f-string (most modern, recommended):
print(f"Hello, {name}! You are {age} years old.")

# Python option B — old style, you may see this in older code:
print("Hello, %s! You are %d years old." % (name, age))


# ------------------------------------------------------------
# 4. IF / ELSE — note: NO "then", NO "end if", use indentation
# ------------------------------------------------------------
# Basic:
#   IF age > 18 THEN
#     PRINT "Adult"
#   END IF
#
# Pascal:
#   if age > 18 then
#     WriteLn('Adult');
#
# Python — the colon (:) replaces THEN, indentation replaces END IF:
if age > 18:
    print("Adult")
else:
    print("Not an adult")


# ------------------------------------------------------------
# 5. LOOPS
# ------------------------------------------------------------
# Basic:   FOR i = 1 TO 5 ... NEXT i
# Pascal:  for i := 1 to 5 do begin ... end;
# Python:  range(1, 6) means "1 up to but NOT including 6"
for i in range(1, 6):
    print(f"  Loop iteration: {i}")

# WHILE loop — same idea as Basic/Pascal
# Basic:   WHILE x < 10 ... WEND
# Pascal:  while x < 10 do begin ... end;
x = 0
while x < 3:
    print(f"  While x = {x}")
    x = x + 1    # Python also allows: x += 1


# ------------------------------------------------------------
# 6. FUNCTIONS — reusable blocks of code
# ------------------------------------------------------------
# Basic:   SUB greet(n AS STRING) ... END SUB
# Pascal:  procedure greet(n: string); begin ... end;
# Python — "def" keyword, colon, indented body:
def greet(n):
    print(f"  Hello from the function, {n}!")

greet("Milan")    # calling the function


# A function that RETURNS a value (like a Pascal function):
# Pascal:  function add(a, b: integer): integer; begin add := a + b; end;
def add(a, b):
    return a + b

result = add(10, 5)
print(f"  10 + 5 = {result}")


# ------------------------------------------------------------
# 7. KEY DIFFERENCES TO REMEMBER
# ------------------------------------------------------------
# - No semicolons at end of lines
# - No BEGIN / END blocks — indentation (4 spaces) does that job
# - No type declarations — Python is "dynamically typed"
# - # is a comment (Basic used REM or ', Pascal used { } or //)
# - Strings use " or ' — both work
# ============================================================
