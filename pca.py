import sys
inport os
import getopt
import os.path
import json
import subprocess
import glob
import smtplib
from email.mime.text import MIMEText

from ciscoconfparse import CiscoConfParse

def pca_load_config(pca_config_filepath):
	if not os.path.isfile(pca_config_filepath):
		print "Error: config file does not exist"
		sys.exit(2)
	
	pca_config_file = open(pca_config_filepath, 'r')
	pca_config = pca_config_file.read()
	result = json.loads(pca_config)
	return result

def pca_git(pca_config):
	pca_path = os.path.dirname(os.path.realpath(__file__))
	if pca_config['git']['in_use'] == "yes":
		subprocess.call(["cd", pca_config['net_config_filepath']])
		subprocess.call(["git", "pull"])
		subprocess.call(["cd", pca_config['user_rules_filepath']])
		subprocess.call(["git", "pull"])
		subprocess.call(["cd", pca_path])

def pca_check_files(pca_config):
	filelist = []
	recorded_files = pca_config['modifications']
	recorded_filenames = [d['filename'] for d in recorded_files]
	recorded_timestamps = [d['timestamp'] for d in recorded_files]
	rule_files = glob.glob("user_rules_filepath"+"/*.rule")
	for rule_file in rule_files:
		if rule_file in recorded_filenames:
			target_index = recorded_filenames.index(rule_file)
			target_timestamp = recorded_timestamps[target_index]
			if int(target_timestamp) != os.path.getmtime(rule_file):
				filelist = glob.glob("net_config_filepath" + "/*.config")
	if filelist == []:
		config_files = glob.glob("net_config_filepath" + "/*.config")
		for config_file in config_files:
			if config_file in recorded_filenames:
				target_index = recorded_filenames.index(config_file)
				target_timestamp = recorded_timestamps[target_index]
				if int(target_timestamp) == os.path.getmtime(config_file):
					filelist.pop(filelist.index(config_file))
	return filelist

def pca_validate(filelist, pca_config):
	result = {"correct": True, "log":""}
	rule_files = glob.glob("user_rules_filepath"+"/*.rule")
	for rule_file in rule_files:
		for config_file in filelist:
			rules = parse_rules(rule_file)
			config = parse_config(config_file)
			res = pca_calidate_process(rules, config)
			result = {result['correct'] & res['correct'], result['log'] + config_file + "\n" + res['log']}
	return result
	
def pca_calidate_precess(rules, config):
	correct = True
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
					log += "\tdevice_type: ", device_type + "\n"
					log += "\tsection_type: ", section_type + "\n"
					log += "\ttrigger: ", trigger + "\n"
					log += "\tconfig_section: ", config.find_all_children(config_section) + "\n"
					log += "\tvalid_rule: ", valid_rule + "\n"
					log += "\tres: ", res + "\n"
					log += valid_message + "\n" + "\n"
					#do valid_command
					correct = False
	return {"correct":correct, "log":log}

def parse_config(config):
	result = CiscoConfParse(config)
	return result

def parse_rules(rules):
	rule_file = open(rules, 'r')
	rules = rule_file.read()
	result = json.loads(rules)
	return result

def pca_send_log(log, pca_config):
	if pca_config['email']['in_use'] == "yes":
	msg = MIMEText(log)
	msg['Subject'] = 'pca report ' + datetime.datetime.now().strftime("%I:%M%p, %B %d, %Y")
	msg['From'] = pca_config['email']['mail_from']
	msg['To'] = pca_config['email']['mail_to']

	s = smtplib.SMTP(pca_config['email']['host']+":"+pca_config['email']['port'])
	s.starttls()
	s.login(pca_config['email']['mail_from'], pca_config['email']['password_filepath'].read())
	s.sendmail(pca_config['email']['mail_from'], pca_config['email']['mail_to'], msg)
	s.quit()

def print_help():
	print "Usage: pca.py [<config>]"
	print "\t<config>: .pca_config custom path (default is ~/.pca_config)"

def main(argv):

	pca_config_filepath = "~/.pca_config"

	try:
		opts, args = getopt.getopt(argv,"h",[])
	except getopt.GetoptError:
		print_help()
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print_help()
			sys.exit()
		else:
			print_help()
			sys.exit(2)

	if len(args) == 1:
		pca_config_filepath = args[0]
	pca_config = pca_load_config(pca_config_filepath)
	pca_git(pca_config)
	filelist = pca_check_files(pca_config)
	result = pca_validate(filelist, pca_config)

	correct = result["correct"]
	log = result["log"]
	if not correct:
		print "Configuration file is not correct"
		pca_send_log(log, pca_config)
		log_file = open(datetime.datetime.now().strftime("%I%M%p_%B%d_%Y.log"), "w")
		text_file.write(log)
		text_file.close()
	pca_update_files(filelist, pca_config)

if __name__ == "__main__":
	main(sys.argv[1:])