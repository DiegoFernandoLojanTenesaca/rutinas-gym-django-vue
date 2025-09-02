from django.db import models
from django.contrib.auth.models import User

class UsersMetadata(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # token puede ser único mientras está activo; puede quedar vacío una vez consumido
    token = models.CharField(max_length=100, blank=True, null=True, unique=True)

    def __str__(self):
        nombre = (self.user.first_name or "").strip() or self.user.username
        return f"{nombre} | token={'--' if not self.token else self.token[:8] + '...'}"

    class Meta:
        db_table = 'users_metadata'
        verbose_name = 'User metadata'
        verbose_name_plural = 'User metadata'
