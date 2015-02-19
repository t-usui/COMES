import os
import subprocess

class SignatureGenerator(object):
    
    def __init__(self):
        pass
    
    def __del__(self):
        pass
    
    @staticmethod
    def extract_string(file_name):
        command = 'strings -a ' + file_name
        string_list = subprocess.check_output(command, shell=True).split('\n')
        string_list.remove('')
        
        return string_list
    
    @staticmethod
    def extract_common_string(string_list1, string_list2):
        common_string_list = list(set(string_list1) & set(string_list2))
        return common_string_list
    
    @staticmethod
    def extract_diff_string(string_list1, string_list2):
        diff_string_list = list(set(string_list1) - set(string_list2))
        return diff_string_list
    
    @classmethod
    def extract_compiler_common_string(cls, compiler_dir_path):
        file_name_list = os.listdir(compiler_dir_path)
        
        first_flag = True
        for file_name in file_name_list:
            file_path = compiler_dir_path + os.sep + file_name
            if first_flag == True:
                compiler_common_string_list = cls.extract_strings(file_path)
                first_flag = False
            new_string_list = cls.extract_strings(file_path)
            compiler_common_string_list = cls.extract_common_strings(common_string_list, new_string_list)
        
        return compiler_common_string_list
    
    @classmethod
    def extract_string_signature(cls, compiler_dir_path_list):
        """
        ##### not tested yet #####
        dirname should be equal to compiler name
        """
        string_signature_dict = {}
        
        for path in compiler_dir_path_list:
            compiler_name = os.path.basename(path)
            compiler_common_string_list = cls.extract_compiler_common_string(path)
            
            for string in compiler_common_string_list:
                try:
                    if string_signature_dict.has_key(string):
                        del string_signature_dict[string]
                    else:
                        string_signature_dict[string] = compiler
                except:
                    print 'Unknown error occured'
                    sys.exit()

        return string_signature_dict
    

if __name__ == '__main__':
    signature_list = extract_compiler_common_strings('./test')
    for sig in signature_list:
        print sig
