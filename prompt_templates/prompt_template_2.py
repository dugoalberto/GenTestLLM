# This prompt contains the following information:
# - Method name
# - Class name
# - Method code

prompt_template_2 = """
Write a test for the class using the code below:
Class: {class_name}
class code: 
```Python
{class_code}
```
"""