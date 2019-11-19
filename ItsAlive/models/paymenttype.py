from django.db import models
from django.urls import reverse
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE


class PaymentType(SafeDeleteModel):
    '''
    description: This class creates a Payment Type.
    properties:
      merchant_name: name of merchant

    '''
    _safedelete_policy = SOFT_DELETE
    merchant_name = models.CharField(max_length=25)

    class Meta:
        verbose_name = ("PaymentType")
        verbose_name_plural = ("PaymentTypes")

    def get_absolute_url(self):
        return reverse("paymenttype_details", kwargs={"pk": self.pk})