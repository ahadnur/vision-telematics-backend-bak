from django.db import models


class OperationChoice(models.TextChoices):
	REMOVE = 'remove', 'Remove'
	ADD = 'add', 'Add'
	ADJUST = 'adjust', 'Adjust'



