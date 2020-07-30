from crm.service import v1
from . import models


class UserInfoConfig(v1.CrmSetting):
    def test(self, is_header=False):
        if is_header:
            return 'test'
        return 'xx'

    list_display = ['id', 'username', 'password', test]


v1.site.register(models.UserInfo, UserInfoConfig)
