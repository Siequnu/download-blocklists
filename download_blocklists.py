# blocklist_download v0.2
# python script to automate downloading of blacklists
# automatically download and extract blacklist files. 

import gzip
import urllib2
import subprocess
import sys
from datetime import datetime


def printNewLine ():
	print ""


# Receives text to be printed to log, temporarily changes stdout to log text.
# Logs text, then reverts stdout back to terminal, and returns the original text as a string to be printed on screen if wanted
def log(logText):
	backup = sys.stdout
	sys.stdout = open('/var/log/download_blocklists.log', 'a') # Set all print to go to log file
	print (str(logText))
	sys.stdout = backup # Revert back to original output in terminal
	return str(logText)

# Start log
print (log (datetime.now().strftime('Starting new download script at %H:%M on %d/%m/%Y')))

blocklistUrls = [("level1", "http://list.iblocklist.com/?list=ydxerpxkpcfqjaybcssw&fileformat=p2p&archiveformat=gz"), ("level2", "http://list.iblocklist.com/?list=gyisgnzbhppbvsphucsw&fileformat=p2p&archiveformat=gz"), ("level3", "http://list.iblocklist.com/?list=uwnukjqktoggdknzrhgh&fileformat=p2p&archiveformat=gz"), ("spyware", "http://list.iblocklist.com/?list=llvtlsjyoyiczbkjsxpf&fileformat=p2p&archiveformat=gz"), ("spider", "http://list.iblocklist.com/?list=mcvxsnihddgutbjfbghy&fileformat=p2p&archiveformat=gz"), ("ads", "http://list.iblocklist.com/?list=dgxtneitpuvgqqcpfulq&fileformat=p2p&archiveformat=gz"), ("proxy", "http://list.iblocklist.com/?list=xoebmbyexwuiogmbyprb&fileformat=p2p&archiveformat=gz"), ("badpeers", "http://list.iblocklist.com/?list=cwworuawihqvocglcoss&fileformat=p2p&archiveformat=gz"), ("microsoft", "http://list.iblocklist.com/?list=xshktygkujudfnjfioro&fileformat=p2p&archiveformat=gz"), ("hijacked", "http://list.iblocklist.com/?list=usrcshglbiilevmyfhse&fileformat=p2p&archiveformat=gz"), ("webexploit", "http://list.iblocklist.com/?list=ghlzqtqxnzctvvajwwag&fileformat=p2p&archiveformat=gz"), ("pedophiles", "http://list.iblocklist.com/?list=dufcxgnbjsdwmwctgfuj&fileformat=p2p&archiveformat=gz"), ("rangetest", "http://list.iblocklist.com/?list=plkehquoahljmyxjixpu&fileformat=p2p&archiveformat=gz"), ("bogon", "http://list.iblocklist.com/?list=gihxqmhyunbxhbmgqrla&fileformat=p2p&archiveformat=gz"), ("dshield", "http://list.iblocklist.com/?list=xpbqleszmajjesnzddhv&fileformat=p2p&archiveformat=gz"), ("forumspam", "http://list.iblocklist.com/?list=ficutxiwawokxlcyoeye&fileformat=p2p&archiveformat=gz"), ("ianareserved", "http://list.iblocklist.com/?list=bcoepfyewziejvcqyhqo&fileformat=p2p&archiveformat=gz"), ("edu", "http://list.iblocklist.com/?list=imlmncgrkbnacgcwfjvh&fileformat=p2p&archiveformat=gz"), ("iana-private", "http://list.iblocklist.com/?list=cslpybexmxyuacbyuvib&fileformat=p2p&archiveformat=gz"), ("iana-multicast", "http://list.iblocklist.com/?list=pwqnlynprfgtjbgqoizj&fileformat=p2p&archiveformat=gz"), ("DROP", "http://list.iblocklist.com/?list=zbdlwrqkabxbcppvrnos&fileformat=p2p&archiveformat=gz")]

blocklistTargetFolder = "/var/lib/transmission-daemon/.config/transmission-daemon/blocklists/"

print "Downloading the following " + str(len(blocklistUrls)) + " lists:"
indexNumber = 1
for url in blocklistUrls:
	prettyName, blocklistUrl = url[0], url[1]
	print str(indexNumber) + ": " + prettyName + ": " + blocklistUrl
	indexNumber = indexNumber + 1
printNewLine()
print "Blocklist files will be extracted to: " + blocklistTargetFolder
printNewLine()

# Stop the transmission daemon - this will be restarted as the last step of this script
print "Stopping transmission daemon..."
subprocess.call("sudo service transmission-daemon stop",shell=True)
print "Transmission daemon stopped."
printNewLine()

print "Starting download..."
for url in blocklistUrls:
	prettyName, blocklistUrl = url[0], url[1]
	print "Downloading " + prettyName + " blocklist..."
	response = urllib2.urlopen(blocklistUrl)
	zipcontent = response.read()
	
	with open("/tmp/" + prettyName + "-blocklist", 'w') as f:
		f.write(zipcontent)

	print "Download successful. Attempting to extract file..."

	inF = gzip.open("/tmp/" + prettyName + "-blocklist", 'rb')
	outFilename = blocklistTargetFolder + prettyName + "unpacked" + ".txt"
	outF = open(outFilename, 'wb')
	outF.write( inF.read() )
	inF.close()
	outF.close()
	
	print "Successfully extracted " + prettyName + " blocklist."

printNewLine()
print "Successfully downloaded and extracted all blocklists."
printNewLine()
print "Restarting transmission daemon..."
subprocess.call("sudo service transmission-daemon start", shell=True)
print "Transmission daemon restarted."
printNewLine()

# Log that the script ran successfully
print (log(datetime.now().strftime('Blocklist download script finished successfully at %H:%M on %d/%m/%Y')))
