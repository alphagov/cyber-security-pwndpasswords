import pwndapi
import logging
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy
import pandas
from PIL import Image

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

testapp = pwndapi.pwndapi("test-agent", unverified=True, truncate=True)

all_breaches = testapp.all_breaches()

list_of_breaches = []
for breach in all_breaches:
    list_of_breaches.append([breach["Name"], breach["PwnCount"]])

list_of_breaches.sort(key=lambda x: x[1], reverse=True)

#### commented out because i'm switching to pandas

#count_total_breaches = sum(n for _, n in list_of_breaches)

#top_ten_breaches=list_of_breaches[:10]
#count_top_ten_breaches = sum(n for _, n in top_ten_breaches)

#logger.info("total breached accounts is %s", count_total_breaches)
#logger.info("breached accounts of top 10 is %s", count_top_ten_breaches)
#logger.info("our list of breaches is as follows")
#logger.info(top_ten_breaches)

# Generate a word cloud image
#wordcloud = WordCloud().generate(top_ten_breaches)

df = pandas.DataFrame(list_of_breaches)
df.columns = ['name', 'count']
df.sort_values(by="count", ascending=True)

breaches = df.groupby("name")
breaches.size().sort_values(ascending=False).plot.bar()

d = {}
for a, x in df.values:
    d[a] = x

#wordcloud = WordCloud()
#wordcloud.generate_from_frequencies(frequencies=d)
#plt.figure()
#plt.imshow(wordcloud, interpolation="bilinear")
#plt.axis("off")
#plt.show()

def transform_format(val):
    if val > 200:
        return 255
    else:
        return val

image_mask = numpy.array(Image.open("hacker.png"))
#image_mask = image_mask.reshape((image_mask.shape[0], -1), order='F')

#transformed_mask = numpy.ndarray((image_mask.shape[0],image_mask.shape[1]), numpy.int32)
#for i in range(len(image_mask)):
#    transformed_mask[i] = list(map(transform_format, image_mask[i]))

wc = WordCloud(background_color="white", max_words=300, mask=image_mask,
               contour_width=1, contour_color='grey',
               max_font_size=400)

wc.generate_from_frequencies(frequencies=d)

# show
image_colors = ImageColorGenerator(image_mask)
plt.figure(figsize=[20,10])
plt.imshow(wc, interpolation='None')
plt.axis("off")

plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.figure()
#plt.imshow(image_mask, cmap=plt.cm.gray, interpolation='bilinear')
plt.axis("off")


#plt.imshow(image_mask, cmap=plt.cm.gray, interpolation="None")
plt.show()

#plt.imshow(image_mask, cmap=plt.cm.gray, interpolation="None")
#plt.imshow(wordcloud.recolor(color_func=image_colors), alpha=.8, interpolation='None')


#plt.figure(figsize=(15,10))
#plt.xticks(rotation=50)
#plt.xlabel("Site")
#plt.ylabel("Number")
#plt.show()

#wordcloud = WordCloud().generate(text)

# Display the generated image:
#plt.imshow(wordcloud, interpolation='bilinear')
#plt.axis("off")
#plt.show()

#df = df.transpose()

#wordcloud = WordCloud().generate("word1, word2, word3, word4")
# Display the generated image:
#plt.imshow(wordcloud, interpolation='bilinear')
#plt.axis("off")

#wordcloud = WordCloud(max_font_size=40).generate("word1, word2, word3, word4")
#plt.figure()
#plt.imshow(wordcloud, interpolation="bilinear")
#plt.axis("off")
#plt.show()




#5,696,187,306
#3,325,124,558