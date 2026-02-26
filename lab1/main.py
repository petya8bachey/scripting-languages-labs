def compress_rle(data):
    if not data:
        return ""
    
    result = []
    count = 1
    
    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            count += 1
        else:
            result.append(data[i - 1])
            result.append(str(count))
            count = 1
    
    result.append(data[-1])
    result.append(str(count))
    
    return "".join(result)


def decompress_rle(data):
        if not data:
            return ""
    
        result = []
        
        for i in range(0, len(data), 2):
            result.append(data[i] * int(data[i + 1]))
        
        return "".join(result)


data = "AAABCC"

print(decompress_rle(compress_rle(data)) == data)