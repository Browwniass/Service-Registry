from django.db.models import Model, CharField, IntegerField, UniqueConstraint


class Quarter(Model):
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
       