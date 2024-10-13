from django.db import models
from django.core import checks
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):
    description = "Ordering Field on a unique field"

    def __init__(self, unique_for_field=None, *args, **kwargs):
        self.unique_for_field = unique_for_field
        super(OrderField, self).__init__(*args, **kwargs)

    def check(self, **kwargs):
        return [
            *super(OrderField, self).check(**kwargs),
            *self._check_for_field_attribute(),
        ]

    def _check_for_field_attribute(self):
        if self.unique_for_field is None:
            return [
                checks.Error(
                    "OrderField must provide a unique_for_field attribute",
                )
            ]
        elif self.unique_for_field not in [f.name for f in self.model._meta.get_fields()]:
            return [
                checks.Error(
                    f"{self.model.__name__} has no field named {self.unique_for_field}",
                )
            ]
        return []

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.unique_for_field) is None:
            queryset = self.model.objects.all()

            try:
                query = {
                    self.unique_for_field: getattr(
                        model_instance, self.unique_for_field)
                }

                queryset = queryset.filter(**query)
                last_item = queryset.latest(self.attname)
                value = last_item.sequence + 1

            except ObjectDoesNotExist:
                value = 1
            return value

        return super().pre_save(model_instance, add)
