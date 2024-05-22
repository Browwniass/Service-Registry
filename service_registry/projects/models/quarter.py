from django.db.models import Model, CharField, IntegerField, UniqueConstraint
from dirtyfields import DirtyFieldsMixin


class Quarter(DirtyFieldsMixin, Model):
    QUARTER_CHOICES =(
        ('q1','Q1'),
        ('q2','Q2'),
        ('q3','Q3'),
        ('q4','Q4'),
    )
    year = IntegerField()
    quarter = CharField(max_length=4, choices=QUARTER_CHOICES)
        
    class Meta:
        app_label = 'projects'
        constraints = [UniqueConstraint(fields=['year', 'quarter'], name='quarter_constr')]
    
    def __str__(self):
        return f"{self.year}[{self.quarter}]"
    
    def save(self, *args, **kwargs):
        if self.pk == None:
            for choice in self.QUARTER_CHOICES:
                instance = Quarter(year=self.year, quarter = choice[0])
                super(Quarter, instance).save(*args, **kwargs)
        