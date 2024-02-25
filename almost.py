import re

# Your input string
input_string = input()

# Split the string using regular expression
result_list = re.findall('\s+|\S+', input_string)
#result_list = re.findall(r"^[a-zA-Z0-9_]*$", input_string)

# Output the result list
print(result_list)
print(input_string)

# W gives '++ '