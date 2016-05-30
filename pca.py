import sys
import os
import os.path
import getopt
import os.path
import json
import subprocess
import glob
import smtplib
import datetime
from email.mime.text import MIMEText

from ciscoconfparse import CiscoConfParse

PCA_DEBUG = False
PCA_VERBOSE = False

def pca_load_config(pca_config_filepath):
	global PCA_VERBOSE
	global PCA_DEBUG
	if not os.path.isfile(pca_config_filepath):
		print("Error: pca_config file does not exist")
		sys.exit(2)
	pca_config_file = open(pca_config_filepath, 'r')
	if PCA_DEBUG:
		print("pca_config file descriptor:")
		print(pca_config_file)
	pca_config = pca_config_file.read()
	if PCA_DEBUG:
		print("pca_config file content:")
		print(pca_config)
	result = json.loads(pca_config)
	if PCA_DEBUG:
		print("pca_config JSON structure:")
		print(result)
	return result

def pca_git(pca_config):
	global PCA_VERBOSE
	global PCA_DEBUG
	user_rules_filepath = os.path.expanduser(pca_config['user_rules_filepath'])
	net_config_filepath = os.path.expanduser(pca_config['net_config_filepath'])
	if PCA_DEBUG:
		print("user rules filepath: " + user_rules_filepath)
		print("net config filepath: " + net_config_filepath)
	if PCA_DEBUG:
		print("git usage: " + pca_config['git']['in_use'])
	if pca_config['git']['in_use'] == "yes":
		if PCA_VERBOSE:
			print("updating git repositories")
		subprocess.call(["git", "pull"], cwd=net_config_filepath)
		subprocess.call(["git", "pull"], cwd=user_rules_filepath)

def pca_check_files(pca_config):
	global PCA_VERBOSE
	global PCA_DEBUG
	filelist = []
	recorded_files = pca_config['modifications']
	user_rules_filepath = os.path.expanduser(pca_config['user_rules_filepath'])
	net_config_filepath = os.path.expanduser(pca_config['net_config_filepath'])
	recorded_filenames = [d['filename'] for d in recorded_files]
	recorded_timestamps = [d['timestamp'] for d in recorded_files]
	if PCA_VERBOSE:
		print("checking rule files")
	rule_files = glob.glob(user_rules_filepath+"/*.rule")
	if PCA_DEBUG:
		print("rule files: ")
		print(rule_files)
	for rule_file in rule_files:
		if rule_file in recorded_filenames:
			target_index = recorded_filenames.index(rule_file)
			target_timestamp = recorded_timestamps[target_index]
			if int(target_timestamp) != int(os.path.getmtime(rule_file)):
				filelist = glob.glob(net_config_filepath + "/*.config")
	if filelist == []:
		if PCA_VERBOSE:
			print("checking config files")
		filelist = glob.glob(net_config_filepath + "/*.config")
		config_files = glob.glob(net_config_filepath + "/*.config")
		if PCA_DEBUG:
			print("config files: ")
			print(config_files)
		for config_file in config_files:
			if config_file in recorded_filenames:
				target_index = recorded_filenames.index(config_file)
				target_timestamp = recorded_timestamps[target_index]
				if int(target_timestamp) == int(os.path.getmtime(config_file)):
					filelist.pop(filelist.index(config_file))
	if PCA_DEBUG:
		print("resulting filelist:")
		print(filelist)
	return filelist

def pca_verify(filelist, pca_config):
	global PCA_VERBOSE
	global PCA_DEBUG
	result = {"correct": True, "log":""}
	filelist_incorrect = []
	user_rules_filepath = os.path.expanduser(pca_config['user_rules_filepath'])
	rule_files = glob.glob(user_rules_filepath+"/*.rule")
	for rule_file in rule_files:
		for config_file in filelist:
			if PCA_VERBOSE:
				print("checking " + config_file + " using rules from " + rule_file)
			rules = parse_rules(rule_file)
			config = parse_config(config_file)
			res = pca_verify_process(rules, config)
			correct = result['correct'] & res['correct']
			log = res['log']
			if PCA_DEBUG:
				print("config: " + config_file)
				print("rules: " + rule_file)
				print("result: ")
				print(res)
			if not res['correct']:
				filelist_incorrect.append(config_file)
				log += config_file + "\n" + res['log']
			result = {"correct": correct, "log": log}
	for file_incorrect in filelist_incorrect:
		filelist.pop(filelist.index(file_incorrect))
	return result
	
def pca_verify_process(rules, config):
	global PCA_VERBOSE
	global PCA_DEBUG
	correct = True
	log = ""
	sections = rules['sections']
	for section in sections:
		section_type = section['type']
		device_type = section['device_type']
		trigger = section['trigger']
		confitions = section['conditions']
		config_sections = config.find_parents_w_child(section_type, trigger)
		for condition in confitions:
			valid_rule = condition['rule']
			valid_message = condition['message']
			valid_command = None
			if 'command' in condition:
				valid_command = condition['command']
			for config_section in config_sections:
				res = config.find_children_w_parents(config_section, valid_rule)
				if res == []:
					log += "\tdevice_type: " + device_type + "\n"
					log += "\tsection_type: " + section_type + "\n"
					log += "\ttrigger: " + trigger + "\n"
					log += "\tconfig_section: " + '\n\t'.join(config.find_all_children(config_section)) + "\n"
					log += "\tvalid_rule: " + valid_rule + "\n"
					log += valid_message + "\n" + "\n"
					#do valid_command
					correct = False
	return {"correct":correct, "log":log}

def parse_config(config):
	if not os.path.isfile(config):
		print("Error: config file does not exist")
		sys.exit(2)
	result = CiscoConfParse(config)
	return result

def parse_rules(rules):
	if not os.path.isfile(rules):
		print("Error: rule file does not exist")
		sys.exit(2)
	rule_file = open(rules, 'r')
	rules = rule_file.read()
	result = json.loads(rules)
	return result

def pca_send_log(log, pca_config):
	global PCA_VERBOSE
	global PCA_DEBUG
	if PCA_DEBUG:
		print("email usage: " + pca_config['email']['in_use'])
	if pca_config['email']['in_use'] == "yes":
		if PCA_VERBOSE:
			print("sending mail")
		msg = MIMEText(log)
		msg['Subject'] = 'pca report ' + datetime.datetime.now().strftime("%I:%M%p, %B %d, %Y")
		msg['From'] = pca_config['email']['mail_from']
		msg['To'] = pca_config['email']['mail_to']
		s = smtplib.SMTP(pca_config['email']['host']+":"+pca_config['email']['port'])
		s.starttls()
		s.login(pca_config['email']['mail_from'], pca_config['email']['password_filepath'].read())
		s.sendmail(pca_config['email']['mail_from'], pca_config['email']['mail_to'], msg)
		s.quit()

def search(ld, name):
	for d in ld:
		if d['filename'] == name:
			return d
	return None

def pca_update_files(filelist, pca_config, pca_config_filepath):
	global PCA_VERBOSE
	global PCA_DEBUG
	user_rules_filepath = os.path.expanduser(pca_config['user_rules_filepath'])
	net_config_filepath = os.path.expanduser(pca_config['net_config_filepath'])
	modifications = pca_config['modifications']
	recorded_filenames = [d['filename'] for d in modifications]
	recorded_timestamps = [d['timestamp'] for d in modifications]
	for config_file in filelist:
		if PCA_VERBOSE:
			print("updating config file "+config_file+" information")
		if config_file in recorded_filenames:
			f = search(modifications, config_file)
			modifications[modifications.index(f)]['timestamp'] = os.path.getmtime(config_file)
		else:
			modifications.append({'filename':config_file, 'timestamp':os.path.getmtime(config_file)})
	rule_files = glob.glob(user_rules_filepath+"/*.rule")
	for rule_file in rule_files:
		if PCA_VERBOSE:
			print("updating rule file "+rule_file+" information")
		if rule_file in recorded_filenames:
			f = search(modifications, rule_file)
			modifications[modifications.index(f)]['timestamp'] = os.path.getmtime(rule_file)
		else:
			modifications.append({'filename':rule_file, 'timestamp':os.path.getmtime(rule_file)})
	pca_config['modifications'] = modifications
	outfile = open(pca_config_filepath, 'w')
	json.dump(pca_config, outfile)

def print_help():
	print("Usage: pca.py [-h][-d][-v][-c <config>][-s <filepath>]")
	print("\t-h, --help: print out help")
	print("\t-d, --debug: debug details")
	print("\t-v, --verbose: additional details about processes")
	print("\t-c, --config: .pca_config custom path (default is ~/.pca_config)")
	print("\t-s, --save: log save filepath")

def main(argv):
	global PCA_VERBOSE
	global PCA_DEBUG
	pca_config_filepath = os.path.expanduser("~/.pca_config")
	pca_log_filepath = ("./")
	try:
		opts, args = getopt.getopt(argv,"hdvc:s:",['help', 'debug', 'verbose', 'custom', 'save'])
	except getopt.GetoptError:
		print_help()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ('-h', '--help'):
			print_help()
			sys.exit()
		elif opt in ('-d', '--debug'):
			PCA_DEBUG = True
		elif opt in ('-v', '--verbose'):
			PCA_VERBOSE = True
		elif opt in ('-c', '--custom'):
			pca_config_filepath = os.path.expanduser(arg)
		elif opt in ('-s', '--save'):
			pca_log_filepath = os.path.expanduser(arg)
		else:
			print_help()
			sys.exit(2)
	if PCA_DEBUG:
		print("pca_config filepath: " + pca_config_filepath)
		print("log save filepath: " + pca_log_filepath)
	if PCA_VERBOSE:
		print("loading pca_config")
	pca_config = pca_load_config(pca_config_filepath)
	if pca_config == None:
		print("Error: pca_config file is invalid")
		sys.exit(2)
	if PCA_VERBOSE:
		print("pca_config loaded")
	if PCA_VERBOSE:
		print("checking git")
	pca_git_result = pca_git(pca_config)
	if PCA_VERBOSE:
		print("git checked")
	if PCA_VERBOSE:
		print("checking files")
	filelist = pca_check_files(pca_config)
	if PCA_VERBOSE:
		print("files checked")
	if PCA_VERBOSE:
		print("verifying")
	result = pca_verify(filelist, pca_config)
	if PCA_VERBOSE:
		print("verifying completed")
	if PCA_DEBUG:
		print("verify results:")
		print(result)
	correct = result["correct"]
	log = result["log"]
	if not correct:
		if PCA_VERBOSE:
			print("checking email")
		pca_send_log(log, pca_config)
		if PCA_VERBOSE:
			print("email checked")
		if PCA_VERBOSE:
			print("saving log")
		log_file = open(pca_log_filepath + datetime.datetime.now().strftime("%I%M%p_%B%d_%Y.log"), "w")
		log_file.write(log)
		log_file.close()
		if PCA_VERBOSE:
			print("log saved")
	if PCA_VERBOSE:
		print("updating file information")
	pca_update_files(filelist, pca_config, pca_config_filepath)
	if PCA_VERBOSE:
		print("file information updated")

if __name__ == "__main__":
	main(sys.argv[1:])