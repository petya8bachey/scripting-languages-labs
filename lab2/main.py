with open('customers1.txt') as f1, open('customers2.txt') as f2:
    set1 = {line.strip() for line in f1 if line.strip()}
    set2 = {line.strip() for line in f2 if line.strip()}

print("Только в первой:", set1 - set2)
print("В обеих:", set1 & set2)
print("Все:", set1 | set2)