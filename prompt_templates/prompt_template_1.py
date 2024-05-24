# This prompt contains the following information:
# - Method name
# - Class name
# - Method code

prompt_template_1 = """
Write a test for the method using the code below:
Method: {method_name}
Class: {class_name}
Method code: 
```Python
{method_code}
```
"""