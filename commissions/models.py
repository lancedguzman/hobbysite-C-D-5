from django.db import models
from django.urls import reverse


class Commission(models.Model):
    COMMISSION_STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Full', 'Full'),
        ('Completed', 'Completed'),
        ('Discontinued', 'Discontinued'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=12, choices=COMMISSION_STATUS_CHOICES, default='Open')
    author = models.ForeignKey(
        'user_management.Profile',
        on_delete=models.CASCADE,
        related_name='commissions',
        null=True
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("commissions:commission", args=[str(self.id)])


class Job(models.Model):
    JOB_STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Full', 'Full'),
    ]

    commission = models.ForeignKey(
        Commission,
        on_delete=models.CASCADE,
        related_name='jobs'
    )
    role = models.CharField(max_length=255)
    manpower_required = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=JOB_STATUS_CHOICES, default='Open')

    class Meta:
        ordering = ['status', '-manpower_required', 'role']

    def __str__(self):
        return f"Job: {self.role} ({self.commission.title})"


class JobApplication(models.Model):
    APPLICATION_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    applicant = models.ForeignKey(
        'user_management.Profile',
        on_delete=models.CASCADE,
        related_name='job_applications'
    )
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS_CHOICES, default='Pending')
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['status', '-applied_on']
        constraints = [ 
            models.UniqueConstraint(fields=['job', 'applicant'], name='unique_job_applicant')
        ]

    def __str__(self):
        return f"{self.applicant}, applying for {self.job.role}"
