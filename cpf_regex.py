import re

pattern = '(\d{3}\.){2}\d{3}-\d{2}'
string = '556.658.659-89'

result = re.fullmatch(pattern, string)

print(result)