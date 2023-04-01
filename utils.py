from aiogram.utils.helper import Helper, HelperMode, ListItem


class UserState(Helper):
    mode = HelperMode.snake_case



    CREATE_GROUP_STATE = ListItem()
    JOIN_GROUP_STATE = ListItem()
    IN_GROUP_STATE = ListItem()
    WAITING_LIST_NAME = ListItem()
    WAITING_TO_OPEN_LIST = ListItem()
    IN_LIST = ListItem()
    ADD_NEW_PRODUCT = ListItem()


if __name__ == '__main__':
    print(UserState.all())