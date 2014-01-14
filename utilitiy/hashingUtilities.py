

def fileToSha1ChunkArray(filePath, chunkSize):
    outlist =[]
    with open(filePath, 'rb') as theFile:
        while True:
            data = theFile.read(chunkSize)
            if not data:
                break
            hashedData = hashlib.sha1(data).hexdigest()
            outlist.append(hashedData)
    return outlist
      


def addFileAndMetaDataToZookeeper(filePath, chunkKeyArray, kazooInstance):
    

    if not kazooInstance.exists(filePath):
        kazooInstance.create(filePath)
    else:
        return


    transaction = kazooInstance.transaction()
    for chunkValue in chunkKeyArray:
        chunkPath = filePath + "/" + chunkValue
        transaction.create(chunkPath)

    results = transaction.commit()
      


