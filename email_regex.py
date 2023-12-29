import re

pattern = '[^@^\.]+@[^@^.]+\.com(\.br)?'

string = 'email@email.com'

result = re.search(pattern, string)

print(result)