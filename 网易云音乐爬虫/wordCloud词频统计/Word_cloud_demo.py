from wordcloud import WordCloud

w = WordCloud()
w.generate("Python and WordCloud,python is a high-level programing language.")
w.to_file("pywordcloud.png")

text = "dog cat fish bird cat cat dog"
wc = WordCloud(
    background_color='white',
    width=600,
)
wc.generate(text)
wc.to_file("1.png")