
with open("address",'r') as file:
    urls = file.readlines()
print(len(urls))
for url in urls:
    print(url)