===
wind: programming-language, intent-oriented, operations
===
We define a set of operations on intent here:

--
operations: vm
--
@illuminate:
Creates or updates existing artifact to be aligned with an intent and runs it.

@wind:
Turns artifact into an intent. Adds intent, combining it in.

@unwind:
Removes intent.

@safe:
Safeproofs the intent.

@kid:
Simplifes the intent.

@run:
Executes an existing artifact.

@artifact:
Creates or updates existing artifact to be aligned with an intent.

@measure:
Evaluates against a baseline.


--
operations: context
--

@context: default, context, include, exclude
Explicitly sets context files and scope.

@default:
Uses standard context without modifications.

@include:
Adds specific elements to context.

@exclude:
Removes specific elements from context.

@draft:
Creates preliminary version for review.

@dry:
Don't Repeat Yourself - removes redundancy.

@wet:
Write Everything Twice - adds helpful redundancy.

@kiss:
Keep It Simple, Stupid - simplifies to essence.

@brush:
Applies styling and refinement.

@lift:
Extracts specific aspects or patterns.

@move:
Relocates elements within the winding.

@unwind
Removes intent from the existing winding

@heat:
Increases temperature/creativity for varied output.

@cool:
Reduces temperature/creativity for conservative output.

@whine:
Complains about issues found in the winding.

@fresh:
Complete rebuild from intent (unwind + wind in context).

@freshen:
Updates and modernizes while preserving structure.

@fly:
Adds freedom and creativity.

@not:
Negates the intent

--
operations: developers
--
@chat:
Responds in a chat mode.

@help:
Provides assistance and documentation.

@feedback:
Provides feedback.

@todo:
Adds to a todo list

@fix:
Attempts automatic error correction.

@debug:
Attempts to debug.

@test:
Runs test cases.

@prove:
Formally verifies.

@probe:
Safe and non-destructively test mode.

@kite:
Experiments and tests ideas.

@wing:
Wing-it mode to make it up as you go.


--
operations: kids
--
@Wind: 8
Applies the character.

@Sophie: 8
Applies the character.

@boy: 8
Applies the character.

@girl: 8
Applies the character.

@aloha: 8
Applies the character.

--
operations: simulation
--

Here we simulate how operations transform intent and artifacts:

**Initial State:**
```
intent: "Create a simple calculator"
artifact: (empty)
```

**@artifact:**
```
intent: "Create a simple calculator"
artifact: 
  def add(a, b):
      return a + b
  def subtract(a, b):
      return a - b
```

**@wind: "Add multiplication"**
```
intent: "Create a simple calculator with multiplication"
artifact:
  def add(a, b):
      return a + b
  def subtract(a, b):
      return a - b
  def multiply(a, b):
      return a * b
```

**@unwind: "Remove subtraction"**
```
intent: "Create a simple calculator with multiplication"
artifact:
  def add(a, b):
      return a + b
  def multiply(a, b):
      return a * b
```

**@kid:**
```
intent: "Simple calculator"
artifact:
  def add(a, b): return a + b
  def multiply(a, b): return a * b
```

**@safe:**
```
intent: "Simple calculator"
artifact:
  def add(a, b):
      if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
          raise TypeError("Arguments must be numbers")
      return a + b
  def multiply(a, b):
      if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
          raise TypeError("Arguments must be numbers")
      return a * b
```

**@kiss:**
```
intent: "Calculator"
artifact:
  def calc(op, a, b):
      return {'+': a+b, '*': a*b}[op]
```

**@dry:**
```
intent: "Calculator"
artifact:
  ops = {'+': lambda a,b: a+b, '*': lambda a,b: a*b}
  def calc(op, a, b): return ops[op](a, b)
```

**@wet:**
```
intent: "Calculator"
artifact:
  def add(a, b):
      """Adds two numbers together."""
      return a + b
  
  def multiply(a, b):
      """Multiplies two numbers together."""
      return a * b
  
  # Example usage:
  # result = add(5, 3)  # Returns 8
  # result = multiply(4, 7)  # Returns 28
```

**@brush:**
```
intent: "Calculator"
artifact:
  class Calculator:
      """A simple calculator class."""
      
      def add(self, a: float, b: float) -> float:
          """Add two numbers."""
          return a + b
      
      def multiply(self, a: float, b: float) -> float:
          """Multiply two numbers."""
          return a * b
```

**@heat:**
```
intent: "Creative calculator with multiple approaches"
artifact:
  # Approach 1: Functional style
  add = lambda a, b: a + b
  multiply = lambda a, b: a * b
  
  # Approach 2: Class-based
  class Calculator:
      def add(self, a, b): return a + b
      def multiply(self, a, b): return a * b
  
  # Approach 3: Dictionary dispatch
  operations = {'+': add, '*': multiply}
```

**@cool:**
```
intent: "Calculator"
artifact:
  def add(a, b):
      return a + b
  
  def multiply(a, b):
      return a * b
```

**@fresh:**
```
intent: "Modern calculator with error handling"
artifact:
  from typing import Union
  
  class Calculator:
      def add(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
          return a + b
      
      def multiply(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
          return a * b
```

**@freshen:**
```
intent: "Calculator"
artifact:
  class Calculator:
      def add(self, a: float, b: float) -> float:
          """Add two numbers."""
          return a + b
      
      def multiply(self, a: float, b: float) -> float:
          """Multiply two numbers."""
          return a * b
```

**@not:**
```
intent: "NOT a calculator"
artifact:
  # This is explicitly not a calculator
  # It does not perform arithmetic operations
  pass
```

**@lift: "Extract error handling pattern"**
```
intent: "Error handling pattern"
artifact:
  def safe_operation(operation, *args):
      try:
          return operation(*args)
      except Exception as e:
          return f"Error: {e}"
```

**@move: "Move add function to utils module"**
```
intent: "Calculator"
artifact:
  from utils import add
  
  def multiply(a, b):
      return a * b
```

**@measure:**
```
intent: "Calculator"
artifact: [current implementation]
baseline: [previous version]
evaluation:
  - Performance: +15% faster
  - Lines of code: -20%
  - Test coverage: 95%
```

**@test:**
```
intent: "Calculator"
artifact: [implementation]
test_results:
  - test_add: PASSED
  - test_multiply: PASSED
  - test_edge_cases: PASSED
```

**@debug:**
```
intent: "Calculator"
artifact: [implementation]
debug_output:
  - Found: Missing type hints
  - Fixed: Added type annotations
  - Found: No input validation
  - Fixed: Added validation
```

**@fix:**
```
intent: "Calculator"
artifact: [before]
  def add(a, b):
      return a + b  # Missing type hints

artifact: [after]
  def add(a: float, b: float) -> float:
      return a + b  # Fixed: Added type hints
```

**@probe:**
```
intent: "Calculator"
probe_results:
  - Function signatures: OK
  - Return types: OK
  - Potential issues: None found
  - Recommendations: Add docstrings
```

**@whine:**
```
intent: "Calculator"
complaints:
  - "Why no division? This is incomplete!"
  - "Where are the tests?"
  - "No error handling? What if someone passes strings?"
  - "This needs better documentation!"
```

**@todo:**
```
intent: "Calculator"
todos:
  - [ ] Add division operation
  - [ ] Add subtraction operation
  - [ ] Add comprehensive tests
  - [ ] Add error handling
  - [ ] Write documentation
```

**@context: include="math_utils.py", exclude="legacy.py"**
```
intent: "Calculator"
context:
  included: math_utils.py
  excluded: legacy.py
artifact: [implementation using math_utils]
```

**@default:**
```
intent: "Calculator"
context: [standard project context]
artifact: [implementation]
```

**@draft:**
```
intent: "Calculator (DRAFT)"
artifact: [preliminary implementation]
status: DRAFT - needs review
notes: "Basic structure in place, needs refinement"
```

**@fly:**
```
intent: "Calculator"
artifact:
  # Let's try something creative!
  class Calculator:
      def __init__(self):
          self.history = []
      
      def add(self, a, b):
          result = a + b
          self.history.append(f"{a} + {b} = {result}")
          return result
      
      def multiply(self, a, b):
          result = a * b
          self.history.append(f"{a} * {b} = {result}")
          return result
      
      def get_history(self):
          return self.history
```

**@chat:**
```
User: "I need a calculator"
Assistant: "I can help you create a calculator! What operations do you need?"
User: "Just add and multiply"
Assistant: "Great! Here's a simple calculator with add and multiply..."
```

**@help:**
```
Operation: @artifact
Usage: @artifact
Description: Creates or updates existing artifact to be aligned with an intent.
Example: @artifact transforms intent "calculator" into code implementation.
```

**@feedback:**
```
intent: "Calculator"
feedback:
  - "Good: Simple and clear"
  - "Improve: Add type hints"
  - "Improve: Add error handling"
  - "Good: Follows Python conventions"
```

**@kite:**
```
intent: "Calculator (experimental)"
artifact:
  # Experimenting with operator overloading
  class Calculator:
      def __init__(self, value=0):
          self.value = value
      
      def __add__(self, other):
          return Calculator(self.value + other.value)
      
      def __mul__(self, other):
          return Calculator(self.value * other.value)
```

**@wing:**
```
intent: "Calculator"
artifact:
  # Making it up as we go!
  def calc(operation, *args):
      if operation == 'add':
          return sum(args)
      elif operation == 'multiply':
          result = 1
          for arg in args:
              result *= arg
          return result
      else:
          return "Unknown operation"
```

**@run:**
```
intent: "Calculator"
artifact: [implementation]
execution:
  $ python calculator.py
  > add(5, 3)
  8
  > multiply(4, 7)
  28
```

**@intent:**
```
artifact: 
  def add(a, b):
      return a + b
  def multiply(a, b):
      return a * b

intent: "A calculator that can add and multiply numbers"
```

**Character Operations:**

**@Wind: 8**
```
intent: "Calculator"
artifact: [implementation with Wind's creative, exploratory style]
tone: Curious, experimental, asks "what if?"
```

**@Sophie: 8**
```
intent: "Calculator"
artifact: [implementation with Sophie's careful, methodical approach]
tone: Precise, thoughtful, considers edge cases
```

**@boy: 8**
```
intent: "Calculator"
artifact: [implementation with boy's straightforward, practical style]
tone: Direct, efficient, gets things done
```

**@girl: 8**
```
intent: "Calculator"
artifact: [implementation with girl's collaborative, inclusive approach]
tone: Friendly, explanatory, considers user experience
```

**@aloha: 8**
```
intent: "Calculator"
artifact: [implementation with aloha's warm, welcoming style]
tone: Welcoming, helpful, makes it accessible
```

