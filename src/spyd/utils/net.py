from socket import inet_ntop, inet_pton, ntohl, htonl, AF_INET
from struct import pack, unpack

def dottedQuadToLong(ip):
    "convert decimal dotted quad string to long integer"
    return ntohl(unpack('!L',inet_pton(AF_INET,ip))[0])

def longToDottedQuad(n):
    "convert long int to dotted quad string"
    return inet_ntop(AF_INET, pack('!L',htonl(n)))

def simpleMaskedIpToLongIpAndMask(masked_ip):
    ip   = ['0']*4
    mask = ['0']*4
    
    parts = masked_ip.split('.')
    
    for i in xrange(len(parts)):
        ip[i] = parts[i]
        mask[i] = '255'
        
    long_ip   = dottedQuadToLong('.'.join(ip))
    long_mask = dottedQuadToLong('.'.join(mask))
    
    return long_ip, long_mask