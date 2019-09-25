from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _

class User(AbstractBaseUser, PermissionsMixin):
    """ 使用一个扩展AbstractBaseUser的自定义的模型来扩展User模型

    由于我们是从AbstractBaseUser继承的，因此必须遵循一些规则：
    USERNAME_FIELD: 一个描述User模型名字字段的字符串，作为唯一标识。该字段必须唯一 (即，在其定义中，必须设置unique=True);
    REQUIRED_FIELDS: 一个字段名列表，用于当通过createsuperuser管理命令创建一个用户时的提示；
    is_active: 一个布尔值属性，表示用户是否被认为是“活跃的(active)”;
    get_full_name(): 用户的一个更长的正式标识符。一个常见的理解是用户的全名，但它可以是标识该用户的任何字符串。
    get_short_name(): 用户的一个简短的非正式标识符。一个常见的理解是用户的名。

    好吧，让我们继续。我还必须定义自己的UserManager。这是因为现有的manager定义了create_user和create_superuser方法。
    """

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('用户名'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('邮箱'), max_length=100, db_index=True, null=True, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    ) # 用户是否拥有网站的管理权限
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    ) # 设置该账户是否可以登录。 把该标志位置为False而不是直接删除账户。
    # is_superuser # 标识用户是否拥有所有权限，无需显式地权限分配定义。
    # last_login 	用户上次登录的时间日期。 它被默认设置为当前的日期/时间。
    # date_joined 	账号被创建的日期时间 当账号被创建时，它被默认设置为当前的日期/时间。
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", "女")), default="female", verbose_name="性别")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = "core_user"
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
