import json
import re
import ner

date_pattern = re.compile("^2012-")
digit_pattern = re.compile("\d")
html_pattern = re.compile("<[^>]*>")

first_index = 392
last_index = 550
# last_index = 395

judgments_to_process = 100

tmp_file_name = "raw_text_input"

if __name__ == "__main__":
  all_judgments = []

  for index in range(first_index, last_index):
    path = ('data/json/judgments-%s.json' % index)
    data = json.load(open(path))['items']
    data = [j for j in data if date_pattern.match(j['judgmentDate']) ]

    for j in data:
      date = j['judgmentDate']
      text = j['textContent']
      text = text.replace("-\n", "")
      text = html_pattern.sub("", text)
      all_judgments.append((date, text))

  all_judgments.sort()

  all_texts = [text for date, text in all_judgments]
  input = "\n".join(all_texts[:judgments_to_process])

  tmp_file = open(tmp_file_name, 'w')
  tmp_file.write(input)
  tmp_file.close()

  processed = ner.upload_process(tmp_file_name)


  tmp_file = open('xml_data', 'w')
  tmp_file.write(processed.decode('utf-8'))
  tmp_file.close()

