from pykakasi import kakasi,wakati

text = "かな漢字交じり文"
kakasi = kakasi()
kakasi.setMode("J","H") # Katakana to ascii, default: no conversion
conv = kakasi.getConverter()
result = conv.do(text)
print(result)

# wakati = wakati()
# conv = wakati.getConverter()
# result = conv.do(text)
# print(result)