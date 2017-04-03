def check_inclusion(large,small): # two lists, |large|>=|small|,
    while small!=[]:
        for i in range(len(large)):        # checking from the back
            if small[0]==large[i]:
                small.pop(0)
                large.pop(i)
                break
        else: break
    if small==[]:
        return True
    else:
        return False
