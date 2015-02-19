__author__ = 'chris hamm'

from py4j.java_gateway import JavaGateway, GatewayClient

gateway= JavaGateway(GatewayClient(port=58000))
try:
    temp = gateway.getVar()
    print str(temp)
except Exception as inst:
    print type(inst)
    #srguments stored in .args
    print inst.args
    #_str_ allows args tto be printed directly
    print inst
