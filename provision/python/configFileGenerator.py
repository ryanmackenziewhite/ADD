import xml.etree.ElementTree as ET
import sys, getopt
import os
import shutil
import xml.dom.minidom as md
defdict = dict()

#Adds xml version and reference to the stylesheet. Makes it easier to read in xml readers.
def insertStylesheet(fileName):
    with open(fileName, "r") as f3:
        lines = f3.readlines()
    lines.insert(0, '<?xml version="1.0"?>\n<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n')
    with open(fileName, "w") as f4:
        for line in lines:
            f4.write(line)

def indent(elem,level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem,level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

#Reads the default xml files from Apache. Update files when Hadoop version updates.
#Keep files in same directory as script.
def readDefs():
    
    tree = ET.parse("defaults/yarn-default.xml")
    for elem in tree.iter():
        if elem.tag == "name":
            defdict[elem.text] = "yarn-site.xml"
        
    tree = ET.parse("defaults/core-default.xml")
    for elem in tree.iter():
        if elem.tag == "name":
            defdict[elem.text] = "core-site.xml"
    
    tree = ET.parse("defaults/hdfs-default.xml")
    for elem in tree.iter():
        if elem.tag == "name":
            defdict[elem.text] = "hdfs-site.xml"
    
    tree = ET.parse("defaults/mapred-default.xml")
    for elem in tree.iter():
        if elem.tag == "name":
            defdict[elem.text] = "mapred-site.xml"

#Creates a new set of xml config files for hadoop.
def initialConfig(HadoopConf):
    fileName = ""
    readDefs()

    #Use the default property files as base to create the modified files.
    #shutil.copy2("core-default.xml", "core-site.xml")
    #shutil.copy2("hdfs-default.xml", "hdfs-site.xml")
    #shutil.copy2("mapred-default.xml", "mapred-site.xml")
    #shutil.copy2("yarn-default.xml", "yarn-site.xml")
####################################################
    root = ET.Element("configuration")
    tree = ET.ElementTree(root)
    tree.write("core-site.xml")

    root = ET.Element("configuration")
    tree = ET.ElementTree(root)
    tree.write("hdfs-site.xml")

    root = ET.Element("configuration")
    tree = ET.ElementTree(root)
    tree.write("mapred-site.xml")

    root = ET.Element("configuration")
    tree = ET.ElementTree(root)
    tree.write("yarn-site.xml")
####################################################

    
    #This loop needs to be optimized.
    with open(HadoopConf) as f:
        for line in f:
            properties = line.split("::")
            properties[1]=properties[1].rstrip()
            #properties[1]=val
	    print properties
            #print val
            
            fileName = defdict[properties[0]]
            tree = ET.parse(fileName)
#            for elem in tree.iter():
#                if elem.tag == "property" and elem[0].text == properties[0]:
#                    elem[1].text = properties[1].rstrip()
################################################################
            root = tree.getroot()
            myprop = ET.SubElement(root, 'property')
            ET.SubElement(myprop, 'name')
            ET.SubElement(myprop, 'value')
            myprop[0].text = properties[0]
            myprop[1].text = properties[1]
################################################################
            indent(root)
            tree.write(fileName) #Files get written every loop.
            insertStylesheet(fileName) #Files get written again.

#Changes the value of one property.
def singleConfig(hadoopProp):
    readDefs()
    properties = hadoopProp.split("::")
    fileName = defdict[properties[0]]
    
    tree = ET.parse(fileName)

    for elem in tree.iter():
        if elem.tag == "property" and elem[0].text == properties[0]:
            elem[1].text = properties[1].rstrip()
    #indent(tree) 
    tree.write(fileName)
    insertStylesheet(fileName)

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:s:",["iconfig=","sconfig="])
   except getopt.GetoptError:
      print('configFileGenerator.py -i <config file name> -s <propertyname::propertyvalue>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('configFileGenerator.py -i <config file name> -s <propertyname::propertyvalue>')
         sys.exit()
      elif opt in ("-i", "--iconfig"):
         initialConfig(arg)
      elif opt in ("-s", "--sconfig"):
         singleConfig(arg)

if __name__ == "__main__":
   main(sys.argv[1:])
