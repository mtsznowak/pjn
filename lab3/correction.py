from string import ascii_lowercase


def gen_adjecent_words(base):
  output_arr = set()

  # replace char
  for x in ascii_lowercase:
    for i in range(0, len(base)):
      output_arr.add(base[:i] + x + base[i+1:])

  # remove char
  for i in range(0, len(base)):
    output_arr.add(base[:i] + base[i+1:])


  # add char
  for x in ascii_lowercase:
    for i in range(0, len(base)):
      output_arr.add(base[:i] + x + base[i:])

    output_arr.add(base + x)

  return output_arr



def gen_corrections(base, distance, dictionary):
  output_arr = {base}

  for it in range(distance):
    new_output_array = set()
    for word in output_arr:
      new_output_array = new_output_array.union(gen_adjecent_words(word))
    output_arr = new_output_array


  output_arr = filter(lambda word: dictionary.has_key(word), output_arr)

  return list(output_arr)


