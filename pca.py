import sys
import getopt
import os.path
import json

from ciscoconfparse import CiscoConfParse

PCA_DEBUG_MODE = False

def analyze(config, rules):
	correct = True
	sections = rules['sections']
	for section in sections:
		section_type = section['type']
		device_type = section['device_type']
		rule = section['rule']
		validators = section['validators']
		config_sections = config.find_parents_w_child(section_type, rule)
		for validator in validators:
			valid_rule = validator['rule']
			valid_message = validator['message']
			valid_command = None
			if 'command' in validator:
				valid_command = validator['command']
			for config_section in config_sections:
				res = config.find_children_w_parents(config_section, valid_rule)
				if PCA_DEBUG_MODE:
					print "\tsection_type: ", section_type
					print "\trule: ", rule
					print "\tconfig_section: ", config.find_all_children(config_section)
					print "\tvalid_rule: ", valid_rule
					print "\tres: ", res
					print ""
				if res == []:
					print valid_message
					#do valid_command
					correct = False
	return correct

def parse_config(config):
	result = CiscoConfParse(config)
	return result

def parse_rules(rules):
	rule_file = open(rules, 'r')
	rules = rule_file.read()
	result = json.loads(rules)
	return result

def pca_run(config_filepath, rule_filepath):
	if not os.path.isfile(config_filepath):
		print "Error: config file does not exist"
		sys.exit(2)
	if not os.path.isfile(rule_filepath):
		print "Error: rule file does not exist"
		sys.exit(2)

	config = parse_config(config_filepath)
	rules = parse_rules(rule_filepath)

	correct = analyze(config, rules)
	return correct


def print_help():
	print "Usage: pca.py [-d] <config> <rule>"
	print "\t-d: debug mode"
	print "\t<config>: path to configuration file"
	print "\t<rule>: path to custom rule file"

def main(argv):
	config_filepath = ''
	rule_filepath = ''

	try:
		opts, args = getopt.getopt(argv,"hd",[])
	except getopt.GetoptError:
		print_help()
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print_help()
			sys.exit()
		elif opt == '-d':
			global PCA_DEBUG_MODE
			PCA_DEBUG_MODE = True
		else:
			print_help()
			sys.exit(2)
	if len(args) != 2:
		print_help()
		sys.exit(2)

	config_filepath = args[0]
	rule_filepath = args[1]
	correct = pca_run(config_filepath, rule_filepath)
	if not correct:
		print "Configuration file is not correct"

if __name__ == "__main__":
	main(sys.argv[1:])