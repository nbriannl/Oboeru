from pykakasi import kakasi,wakati

text = u"かな漢字交じり文"
kakasi = kakasi()
kakasi.setMode("H","a") # Hiragana to ascii, default: no conversion
kakasi.setMode("K","a") # Katakana to ascii, default: no conversion
kakasi.setMode("J","a") # Japanese to ascii, default: no conversion
kakasi.setMode("r","Hepburn") # default: use Hepburn Roman table
kakasi.setMode("s", True) # add space, default: no separator
kakasi.setMode("C", True) # capitalize, default: no capitalize
conv = kakasi.getConverter()
result = conv.do(text)
print(result)

wakati = wakati()
conv = wakati.getConverter()
result = conv.do(text)
print(result)