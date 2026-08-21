import hashlib
import os

def authenticate_user():
    # Flaw 1: Hardcoded credential string (Bandit: B105)
    api_key = "secret_api_key_9988776655"
    
    # Flaw 2: Insecure hash function MD5 (Bandit: B303/B324)
    user_password = "UserPassword123"
    password_hash = hashlib.md5(user_password.encode()).hexdigest()
    
    return api_key, password_hash

def execute_user_command(user_input):
    # Flaw 3: Dangerous dynamic code evaluation (Bandit: B307)
    eval(user_input)
    
    # Flaw 4: Command injection via shell system call (Bandit: B605)
    os.system("echo " + user_input)

if __name__ == "__main__":
    key, p_hash = authenticate_user()
    execute_user_command("print('Testing SAST Analysis')")
