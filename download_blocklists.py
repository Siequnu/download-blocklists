"""Blocklist Downloader.

Usage:
  download_blocklists.py [<blocklist-target-folder>]
  download_blocklists.py (-h | --help)
  download_blocklists.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt
import gzip
import urllib2
import subprocess
import sys
from datetime import datetime

# Global variables
BLOCKLIST_URLS = [("level1", "http://list.iblocklist.com/?list=ydxerpxkpcfqjaybcssw&fileformat=p2p&archiveformat=gz"), ("level2", "http://list.iblocklist.com/?list=gyisgnzbhppbvsphucsw&fileformat=p2p&archiveformat=gz"), ("level3", "http://list.iblocklist.com/?list=uwnukjqktoggdknzrhgh&fileformat=p2p&archiveformat=gz"), ("spyware", "http://list.iblocklist.com/?list=llvtlsjyoyiczbkjsxpf&fileformat=p2p&archiveformat=gz"), ("spider", "http://list.iblocklist.com/?list=mcvxsnihddgutbjfbghy&fileformat=p2p&archiveformat=gz"), ("ads", "http://list.iblocklist.com/?list=dgxtneitpuvgqqcpfulq&fileformat=p2p&archiveformat=gz"), ("proxy", "http://list.iblocklist.com/?list=xoebmbyexwuiogmbyprb&fileformat=p2p&archiveformat=gz"), ("badpeers", "http://list.iblocklist.com/?list=cwworuawihqvocglcoss&fileformat=p2p&archiveformat=gz"), ("microsoft", "http://list.iblocklist.com/?list=xshktygkujudfnjfioro&fileformat=p2p&archiveformat=gz"), ("hijacked", "http://list.iblocklist.com/?list=usrcshglbiilevmyfhse&fileformat=p2p&archiveformat=gz"), ("webexploit", "http://list.iblocklist.com/?list=ghlzqtqxnzctvvajwwag&fileformat=p2p&archiveformat=gz"), ("pedophiles", "http://list.iblocklist.com/?list=dufcxgnbjsdwmwctgfuj&fileformat=p2p&archiveformat=gz"), ("rangetest", "http://list.iblocklist.com/?list=plkehquoahljmyxjixpu&fileformat=p2p&archiveformat=gz"), ("bogon", "http://list.iblocklist.com/?list=gihxqmhyunbxhbmgqrla&fileformat=p2p&archiveformat=gz"), ("dshield", "http://list.iblocklist.com/?list=xpbqleszmajjesnzddhv&fileformat=p2p&archiveformat=gz"), ("forumspam", "http://list.iblocklist.com/?list=ficutxiwawokxlcyoeye&fileformat=p2p&archiveformat=gz"), ("ianareserved", "http://list.iblocklist.com/?list=bcoepfyewziejvcqyhqo&fileformat=p2p&archiveformat=gz"), ("edu", "http://list.iblocklist.com/?list=imlmncgrkbnacgcwfjvh&fileformat=p2p&archiveformat=gz"), ("iana-private", "http://list.iblocklist.com/?list=cslpybexmxyuacbyuvib&fileformat=p2p&archiveformat=gz"), ("iana-multicast", "http://list.iblocklist.com/?list=pwqnlynprfgtjbgqoizj&fileformat=p2p&archiveformat=gz"), ("DROP", "http://list.iblocklist.com/?list=zbdlwrqkabxbcppvrnos&fileformat=p2p&archiveformat=gz")]


# Prints a new line for prettifying console
def print_new_line ():
	print ""


# Receives text to be printed to log, temporarily changes stdout to log text.
# Logs text, then reverts stdout back to terminal, and returns the original
# text as a string to be printed on screen if wanted
def log(log_text):
	backup = sys.stdout
	sys.stdout = open('/var/log/download_blocklists.log', 'a') # Set all print to go to log file
	print (str(log_text))
	sys.stdout = backup # Revert back to original output in terminal
	return str(log_text)


# Main entrance into the program
def main (blocklist_target_folder = "/var/lib/transmission-daemon/.config/transmission-daemon/blocklists/"):
	global BLOCKLIST_URLS
	
	print (log (datetime.now().strftime('Starting new download script at %H:%M on %d/%m/%Y')))
	
	print "Downloading the following " + str(len(BLOCKLIST_URLS)) + " lists:"
	index_number = 1
	for url in BLOCKLIST_URLS:
		pretty_name, blocklist_url = url[0], url[1]
		print str(index_number) + ": " + pretty_name + ": " + blocklist_url
		index_number = index_number + 1
	print_new_line()
	print "Blocklist files will be extracted to: " + blocklist_target_folder
	print_new_line()
	
	# Stop the transmission daemon - this will be restarted as the last step of this script
	print "Stopping transmission daemon..."
	subprocess.call("sudo service transmission-daemon stop",shell=True)
	print "Transmission daemon stopped."
	print_new_line()
	
	print "Starting download..."
	for url in BLOCKLIST_URLS:
		pretty_name, blocklist_url = url[0], url[1]
		print "Downloading " + pretty_name + " blocklist..."
		response = urllib2.urlopen(blocklist_url)
		zipcontent = response.read()
		
		with open("/tmp/" + pretty_name + "-blocklist", 'w') as f:
			f.write(zipcontent)
	
		print "Download successful. Attempting to extract file..."
	
		inF = gzip.open("/tmp/" + pretty_name + "-blocklist", 'rb')
		outFilename = blocklist_target_folder + pretty_name + "unpacked" + ".txt"
		outF = open(outFilename, 'wb')
		outF.write( inF.read() )
		inF.close()
		outF.close()
		
		print "Successfully extracted " + pretty_name + " blocklist."
	
	print_new_line()
	print "Successfully downloaded and extracted all blocklists."
	print_new_line()
	print "Restarting transmission daemon..."
	subprocess.call("sudo service transmission-daemon start", shell=True)
	print "Transmission daemon restarted."
	print_new_line()
	
	# Log that the script ran successfully
	print (log(datetime.now().strftime('Blocklist download script finished successfully at %H:%M on %d/%m/%Y')))



# Main program start
arguments = docopt(__doc__, version='Blocklist Downloader 1.0')
print ('Starting Blocklist Downloader...')

# Assign arguments
if '<blocklist-target-folder>' in arguments:
	blocklist_target_folder = str(arguments['<blocklist-target-folder>'])
	print ('Setting target folder as ' + blocklist_target_folder)
	main (blocklist_target_folder)
else:
	main ()