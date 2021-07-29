def domain_checker(email):
    return "." in email[-4] or "." in email[-3]
