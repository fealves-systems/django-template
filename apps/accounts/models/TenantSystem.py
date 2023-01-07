from django.db import models
from django.utils.html import mark_safe


class TenantSystem(models.Model):
    class Meta:
        verbose_name = "Sistema Relacionado"
        verbose_name_plural = "Sistema Relacionado"

    system_tenant_name = models.CharField(max_length=100, null=False)
    system_tenant_logo = models.ImageField(upload_to='tenant_company_logos/%Y/%m/%d/', null=True, blank=True)

    def system_tenant_logo_preview(self):
        from django.utils.html import escape
        if (self.system_tenant_logo):
            return mark_safe(u'<img src="%s" width="32" height="32"/>' % escape(self.system_tenant_logo.url))
        else:
            return mark_safe('<img src="" />')

    system_tenant_logo_preview.short_description = 'System Tenant Logo Preview'
    system_tenant_logo_preview.allow_tags = True

    system_description = models.CharField(max_length=255, null=False)
    authorized_by = models.CharField(
        max_length=15, null=False, default="FEALVES")
    ativo = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    oper = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id}: {self.system_tenant_name} [Ativo: {self.ativo}]"
