def data_types():
    """This function prints type of variables as a list without quotes"""
    
    type1 = 1
    type2 = "hello"
    type3 = 3.14
    type4 = True
    type5 = [1,2,3]
    type6 = {"first":1, "second":2}
    type7 = (1,2,3)
    type8 = {1,2,3}

    types = [type1,type2,type3,type4,type5,type6,type7,type8]
    result= list()
    for t in types:
        result.append(type(t).__name__ )

    print('[' + ', '.join(result) + ']')

if __name__ == '__main__':
     data_types()
