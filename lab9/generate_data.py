import json
import re
import sys

html_pattern = re.compile("<[^>]*>")


if __name__ == "__main__":
  data_written = 0
  output_data = open("output", "w")

  for index in range(1, 1000000):
    path = ('data/json/judgments-%s.json' % index)
    data = json.load(open(path))['items']

    for j in data:
      text = j['textContent']
      text = text.replace("-\n", "")
      text = html_pattern.sub("", text)

      data_written = data_written + len(text)
      output_data.write(text + "\n")

      if data_written > 1000000000:
        break

    if data_written > 1000000000:
      break

  output_data.close()



