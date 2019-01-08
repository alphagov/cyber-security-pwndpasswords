import pwndapi

testapp = pwndapi.pwndapi("test-agent", unverified=True, truncate=True)

# get breaches ordered by size of breach
# then make a word cloud

### exampl

all_breaches = testapp.all_breaches()

list_of_breaches = []
for breach in all_breaches:
    list_of_breaches.append([breach["Name"], breach["PwnCount"]])

list_of_breaches.sort(key=lambda x: x[1], reverse=True)

count_total_breaches = sum(n for _, n in list_of_breaches)

top_ten_breaches=list_of_breaches[:10]
count_top_ten_breaches = sum(n for _, n in top_ten_breaches)

print("total breached accounts is ", count_total_breaches)
print("breached accounts of top 10 is ", count_top_ten_breaches)

print("our list of breaches is as follows")
print(top_ten_breaches)

#5,696,187,306
#3,325,124,558