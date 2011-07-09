'''  
Created on Apr 10, 2011  
Read KDD cup data to store in format suitable for graphlab pmf   
  
Requires numpy, uses ndarray.tofile() to write the binary file  
  
Module recreates the functionality of the matlab file formatData.m by Danny Bickson  
  
Differences:  
Does not hard-code the number of users, items or ratings. these are determined from the file  
This behavior allows more general usage on variable length subsets of the KDDcup data  
Also allows the last user to have a truncated number of items; this handles the case   
where the subset is created by truncating the full file.   
Function prints a (pseudo) warning message when this occurs  
  
Function returns the number of users, items, days, ratings read.   
It is up to the user to check that the returned counts make sense  
  
usage: python readKddData.py --help  
@author: Sanmi Koyejo; sanmi.k@mail.utexas.edu  
'''  
  
from optparse import OptionParser  
from time import time  
from numpy import array, vstack, dtype, amax  
import pickle

def remove_dups(some_list):
    return dict(map(lambda i: (i,1),some_list)).keys()


def readLine(fileHandle, splitter='|'):  
    ''' read single line'''  
    line = fileHandle.readline()  
    if not line: #EOF  
        return line # return null and let caller handle it  
    return line.rstrip().split(splitter) # split the line ans remove newline character  
  
def readChunk(fileHandle, chunkSize, splitter='\t'):  
    '''read a pre-specified chunksize'''  
    for _ in range(chunkSize):  
        line = fileHandle.readline()  
        if not line: #EOF  
            break  
        yield line.rstrip().split(splitter)  
          
def readOneUser(fileHandle, testFlag=False, verbose=True):  
    ''' reads data for one user and returns lists  
    userChunk, itemChumk, timeChunk, rateChunk  
    only reads day, ignores more detailed time'''  
    userChunk = []  
    itemChunk = []  
    timeChunk = []  
    rateChunk = []  
      
    while 1:  
        line = readLine(fileHandle)  
        if not line: break # EOF  
        userID, nRatings = [int(x) for x in line]  
          
        del userChunk[:], itemChunk[:], timeChunk[:], rateChunk[:] # remove previously read data  
          
        for line in readChunk(fileHandle, nRatings):  
            # note allow last user to break nratings constraint. All other users should satisfy this  
            userChunk.append(userID)  
            itemChunk.append(int(line[0]))  
              
            if testFlag:  
                rateChunk.append(0)  
                timeChunk.append(int(line[1]))  
            else:  
                rateChunk.append(int(line[1]))  
                timeChunk.append(int(line[2]))  
          
        if verbose and nRatings != len(userChunk): #last user had a different number of items than expected   
            print "Waring: Expected", nRatings, "ratings from last user; id:", userID, "read", len(userChunk), "ratings."  
              
        yield userChunk, itemChunk, timeChunk, rateChunk   
  
def saveDataToBin(rateMat, outfile, verbose):  
    '''save rateMat array to binary file required by pmf'''  
    nUser = int(amax(rateMat[:,0]))+1 # nUser is max user ID read  
    nItem = int(amax(rateMat[:,1]))+1 # nItem is max itemID read  
    nTime = int(amax(rateMat[:,2]))   # nTime is max time read     
    
    #nUser = len(remove_dups(rateMat[:,0]))
    #nItem = len(remove_dups(rateMat[:,1]))
    #nTime = len(remove_dups(rateMat[:,2]))
    nRate = rateMat.shape[0]
      
    # setup size and rateMat  
    size = array([nUser, nItem, nTime, nRate], dtype=dtype('i4'))  
  
    rateMat[:,0] +=1 # user index starts from 0, graphlab pmf expects 1  
    rateMat[:,1] += nUser+1 # item index starts from 0, graphlab pmf expects nUser+1  
    
    filehandle = open(outfile,'wb')  
    if verbose:   
        print "writing to", outfile  
        start = time()  
          
    size.tofile(filehandle)  
    rateMat.tofile(filehandle)  
    filehandle.close()  
    
    if verbose:  
        print "done writing"  
        print 'writing completed in' , time()-start, 'secs'  
      
    return nUser, nItem, nTime, nRate, rateMat
  
def readKddData(infile, testFlag, verbose):  
    '''open file and read data'''  
    userList = [] # list of users  
    itemList = [] # list of items  
    timeList = [] # list of times  
    rateList = [] # list of ratings  
    fileHandle = open(infile,'rb')  
      
    if verbose: print 'reading data from', infile  
    # read each user's ratings  
    for count, argout in enumerate(readOneUser(fileHandle, testFlag, verbose)):  
        userChunk, itemChunk, timeChunk, rateChunk = argout # rename for readability  
        userList.extend(userChunk)  
        itemList.extend(itemChunk)  
        timeList.extend(timeChunk)  
        rateList.extend(rateChunk)  
      
    fileHandle.close()      
    if verbose: print 'done reading data'  
    return userList, itemList, timeList, rateList  
  
def readAndWriteKddData(infile, outfile, testFlag, verbose):  
    ''' read data then write binary format'''  
  
    # read data  
    if verbose: print 'Starting'  
    userList, itemList, timeList, rateList = readKddData(infile, testFlag, verbose)  
    if verbose: print 'Converting list to numpy array'  
    # convert lists to numpy arrays  
    rateMat = vstack((array(userList, dtype=dtype('f4')), array(itemList, dtype=dtype('f4')),array(timeList, dtype=dtype('f4')), array(rateList, dtype=dtype('f4')))).T  
    #return rateMat
    if verbose: print 'Conversion completed'  
    # TODO: This version requires more memory, @ least while converting between list and numpy array. Fixme  
    if 1: del userList, itemList, timeList, rateList # currently deleting un-needed lists  
    # write to bin format  
    nUser, nItem, nTime, nRate, rateMat = saveDataToBin(rateMat, outfile, verbose)  
    return nUser, nItem, nTime, nRate, rateMat  
  
def main():  
    usage = "usage: %prog [options] arg"  
    parser = OptionParser(usage)  
    parser.add_option("-i", "--infile", dest="infile",  help="input file name", default="SmartTypes_kdd.txt") # fixme  
    parser.add_option("-o", "--outfile", dest="outfile",  help="output file name", default="smarttypes_pmf")  
    parser.add_option("-t", "--istest", action="store_true", dest="istest",  help="treat as test file (format is different)", default=False)  
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose")  
    parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True) # decide  
    (options, args) = parser.parse_args()  
      
    nUser, nItem, nDays, nRate, rateMat = readAndWriteKddData(options.infile,options.outfile,options.istest, options.verbose)  
    print 'followers:', nUser  
    print 'followies:', nItem  
    print 'days', nDays  
    print 'links:', nRate
    return rateMat
      
if __name__ == '__main__':  
    rateMat = main()
    
    