from erl_terms import decode

file_content = open("./conf_test.erl").readlines()
result = decode(''.join(file_content))


def tuple_to_map(tuple_input):
  if type(tuple_input[1]) == tuple:
    return {tuple_input[0]:list(tuple_input[1])}
  else:
    return {tuple_input[0]:tuple_input[1]}

# print tuple_to_map(('wewe', (23,34)))

# print dict(('2', 3))

def loop(conf_list, key):
  temp = []
  for index, value in enumerate(conf_list):

    if type(value) == list:
      output = loop(value, key)
    elif type(value) == tuple:
      if type(value[1]) in [list, tuple]:
        output = loop(value[1], value[0])
      else:
        output = tuple_to_map( value )
    else:
      output = {key:value}

    temp.append(output)
  return {key:temp}


# print result
output = {}
print result
print loop(result, 'data')

# print result


