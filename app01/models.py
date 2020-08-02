from django.db import models


class UserInfo(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=16)
    password = models.CharField(verbose_name='密码', max_length=32)
    ug = models.ForeignKey(verbose_name='用户组', to='UserGroup', on_delete=models.CASCADE, null=True)
    roles = models.ManyToManyField(verbose_name='用户角色', to='Role', related_name='users')

    def __str__(self):
        return self.username


class UserGroup(models.Model):
    title = models.CharField(verbose_name='组名', max_length=32)

    def __str__(self):
        return self.title


class Role(models.Model):
    caption = models.CharField(verbose_name='角色名称', max_length=16)

    def __str__(self):
        return self.caption
