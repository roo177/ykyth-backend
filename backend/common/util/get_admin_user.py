


def get_admin_user(user_list):
    for item in user_list:
        if 'mahirer@gmail.com' == item[1]:
            return item[0]

    raise Exception("Admin user not found! - mahirer@gmail.com")



