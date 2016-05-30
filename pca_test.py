import pca

def pca_test_load_config(): 
	return pca_test_load_config_exist_true() &&
	not pca_test_load_config_exist_false() &&
	pca_test_load_config_json_true() &&
	not pca_test_load_config_json_false() &&
	pca_test_load_config_empty_true() &&
	not pca_test_load_config_empty_false()

def pca_test_load_config_verbose(): 
	print ("pca_test_load_config_exist_true(): ", pca_test_load_config_exist_true() )
	print ("pca_test_load_config_exist_false(): ", not pca_test_load_config_exist_false() )
	print ("pca_test_load_config_json_true(): ", pca_test_load_config_json_true() )
	print ("pca_test_load_config_json_false(): ", not pca_test_load_config_json_false() )
	print ("pca_test_load_config_empty_true(): ", pca_test_load_config_empty_true() )
	print ("pca_test_load_config_empty_false(): ", not pca_test_load_config_empty_false() )

def pca_test_git(): 
	return pca_test_git_use_true() &&
	not pca_test_git_use_false() &&
	pca_test_git_path_true() &&
	vpca_test_git_path_false() &&
	pca_test_git_repo_true() &&
	not pca_test_git_repo_false()

def pca_test_git_verbose(): 
	print ("pca_test_git_use_true(): ", pca_test_git_use_true() )
	print ("pca_test_git_use_false(): ", not pca_test_git_use_false() )
	print ("pca_test_git_path_true(): ", pca_test_git_path_true() )
	print ("pca_test_git_path_false(): ", not pca_test_git_path_false() )
	print ("pca_test_git_repo_true(): ", pca_test_git_repo_true() )
	print ("pca_test_git_repo_false(): ", not pca_test_git_repo_false() )

def pca_test_check_files():
	return pca_test_check_files_exist_true() &&
	not pca_test_check_files_exist_false() &&
	pca_test_check_files_modified_true() &&
	not pca_test_check_files_modified_false()

def pca_test_check_files_verbose():
	print("pca_test_check_files_exist_true(): ", pca_test_check_files_exist_true() )
	print("pca_test_check_files_exist_false(): ", not pca_test_check_files_exist_false() )
	print("pca_test_check_files_modified_true(): ", pca_test_check_files_modified_true() )
	print("pca_test_check_files_modified_false(): ", not pca_test_check_files_modified_false() )

def pca_test_verify_process():
	return pca_test_verify_process_exist_true() &&
	not pca_test_verify_process_exist_false &&
	pca_test_verify_process_correct_true &&
	not pca_test_verify_process_correct_false

def pca_test_verify_process_verbose():
	print("pca_test_verify_process_exist_true(): ", pca_test_verify_process_exist_true() )
	print("pca_test_verify_process_exist_false: ", not pca_test_verify_process_exist_false )
	print("pca_test_verify_process_correct_true: ", pca_test_verify_process_correct_true )
	print("pca_test_verify_process_correct_false: ", not pca_test_verify_process_correct_false )

def pca_test_parse_config():
	return pca_test_parse_config_exist_true() &&
	not pca_test_parse_config_exist_false() &&
	pca_test_parse_config_correct_true() &&
	not pca_test_parse_config_correct_false()

def pca_test_parse_config_verbose():
	print("pca_test_parse_config_exist_true(): ", pca_test_parse_config_exist_true() )
	print("pca_test_parse_config_exist_false(): ", not pca_test_parse_config_exist_false() )
	print("pca_test_parse_config_correct_true(): ", pca_test_parse_config_correct_true() )
	print("pca_test_parse_config_correct_false(): ", not pca_test_parse_config_correct_false() )

def pca_test_parse_rules():
	return pca_test_parse_config_exist_true() &&
	not pca_test_parse_config_exist_false() &&
	pca_test_parse_config_correct_true() &&
	not pca_test_parse_config_correct_false()

def pca_test_parse_rules_verbose():
	print("pca_test_parse_rules_exist_true(): ", pca_test_parse_rules_exist_true() )
	print("pca_test_parse_rules_exist_false(): ", not pca_test_parse_rules_exist_false() )
	print("pca_test_parse_rules_correct_true(): ", pca_test_parse_rules_correct_true() )
	print("pca_test_parse_rules_correct_false(): ", not pca_test_parse_rules_correct_false() )

def pca_test_send_log():
	return pca_test_send_log_use_true() &&
	not pca_test_send_log_use_false() &&
	pca_test_send_log_mail_true() &&
	not pca_test_send_log_mail_false()

def pca_test_send_log_verbose():
	print("pca_test_send_log_use_true(): ", pca_test_send_log_use_true() )
	print("pca_test_send_log_use_false(): ", not pca_test_send_log_use_false() )
	print("pca_test_send_log_mail_true(): ", pca_test_send_log_mail_true() )
	print("pca_test_send_log_mail_false(): ", not pca_test_send_log_mail_false() )

def pca_test_update_files():
	return pca_test_update_files_changes_true() &&
	pca_test_update_files_changes_false()

def pca_test_update_files_verbose():
	print("pca_test_update_files_changes_true(): ", pca_test_update_files_changes_true() )
	print("pca_test_update_files_changes_false(): ", pca_test_update_files_changes_false() )

def pca_test_all():
	return pca_test_load_config() &&
	pca_test_git() &&
	pca_test_check_files() &&
	pca_test_verify_process() &&
	pca_test_parse_config() &&
	pca_test_parse_rules() &&
	pca_test_send_log() &&
	pca_test_update_files()

def pca_test_all_verbose():
	print("pca_test_load_config(): ", pca_test_load_config() )
	pca_test_load_config_verbose()
	print("pca_test_git(): ", pca_test_git() )
	pca_test_git_verbose()
	print("pca_test_check_files(): ", pca_test_check_files() )
	pca_test_check_files_verbose()
	print("pca_test_verify_process(): ", pca_test_verify_process() )
	pca_test_verify_process_verbose()
	print("pca_test_parse_config(): ", pca_test_parse_config() )
	pca_test_parse_config_verbose()
	print("pca_test_parse_rules(): ", pca_test_parse_rules() )
	pca_test_parse_rules_verbose()
	print("pca_test_send_log(): ", pca_test_send_log() )
	pca_test_send_log_verbose()
	print("pca_test_update_files(): ", pca_test_update_files() )
	pca_test_update_files_verbose()

def main(argv):
	if pca_test_all() != True:
		pca_test_all_verbose()

if __name__ == "__main__":
	main(sys.argv[1:])