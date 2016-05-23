def pca_test_load_config():
	return pca_test_load_config_exist_true() &&
	pca_test_load_config_exist_false() &&
	pca_test_load_config_json_true() &&
	pca_test_load_config_json_false() &&
	pca_test_load_config_empty_true() &&
	pca_test_load_config_empty_false()

def pca_test_load_config_verbose():
	print ("pca_test_load_config_exist_true():", pca_test_load_config_exist_true()
	print ("pca_test_load_config_exist_false():", pca_test_load_config_exist_false()
	print ("pca_test_load_config_json_true():", pca_test_load_config_json_true()
	print ("pca_test_load_config_json_false():", pca_test_load_config_json_false()
	print ("pca_test_load_config_empty_true():", pca_test_load_config_empty_true()
	print ("pca_test_load_config_empty_false():", pca_test_load_config_empty_false()

def pca_test_git():
	return pca_test_git_use_true() &&
	pca_test_git_use_false() &&
	pca_test_git_path_true() &&
	pca_test_git_path_false() &&
	pca_test_git_repo_true() &&
	pca_test_git_repo_false()

def pca_test_git_verbose():
	print ("pca_test_git_use_true():", pca_test_git_use_true()
	print ("pca_test_git_use_false():", pca_test_git_use_false()
	print ("pca_test_git_path_true():", pca_test_git_path_true()
	print ("pca_test_git_path_false():", pca_test_git_path_false()
	print ("pca_test_git_repo_true():", pca_test_git_repo_true()
	print ("pca_test_git_repo_false():", pca_test_git_repo_false()