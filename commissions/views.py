from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Count
from .models import Commission, Job, JobApplication
from django.db.models import IntegerField


def commissions_list(request):
    commissions = Commission.objects.all().order_by(
        models.Case(
            models.When(status='Open', then=0),
            models.When(status='Full', then=1),
            models.When(status='Completed', then=2),
            models.When(status='Discontinued', then=3),
            default=4,
            output_field=models.IntegerField(),
        ),
        '-created_on'
    )

    user_comms = applied_comms = None
    if request.user.is_authenticated:
        user_comms = Commission.objects.filter(author=request.user.profile)
        applied_comms = Commission.objects.filter(
            jobs__applications__applicant=request.user.profile
        ).distinct()

    return render(request, 'commissions/commission_list.html', {
        'commissions': commissions,
        'user_commissions': user_comms,
        'applied_commissions': applied_comms,
    })


def commission_detail(request, id):
    commission = get_object_or_404(Commission, id=id)
    jobs = commission.jobs.all().order_by(
        models.Case(
            models.When(status='Open', then=0),
            models.When(status='Full', then=1),
            default=2,
            output_field=models.IntegerField(),
        ),
        '-manpower_required',
        'role'
    )

    accepted_counts = JobApplication.objects.filter(
        job__commission=commission, status='Accepted'
    ).values('job').annotate(count=Count('id'))
    accepted_map = {item['job']: item['count'] for item in accepted_counts}

    total_manpower = sum(job.manpower_required for job in jobs)
    total_accepted = sum(accepted_map.values())
    open_manpower = total_manpower - total_accepted

    job_id = {}
    can_apply_filter = {}

    for job in jobs:
        accepted = accepted_map.get(job.id, 0)
        job.accepted_count = accepted

        if request.user.is_authenticated:
            already_applied = JobApplication.objects.filter(
                job=job, applicant=request.user.profile
            ).exists()
            not_author = commission.author is None or commission.author != request.user.profile
        else:
            already_applied = False
            not_author = True 

        not_full = accepted < job.manpower_required
        can_apply = not already_applied and not_full and not_author
        can_apply_filter[job.id] = can_apply
        job_id[job.id] = job.id

    if request.method == 'POST' and request.user.is_authenticated:
        apply_job_id = request.POST.get('apply_job_id')
        job = get_object_or_404(Job, id=apply_job_id, commission=commission)

        already_applied = JobApplication.objects.filter(
            job=job, applicant=request.user.profile
        ).exists()
        accepted = accepted_map.get(job.id, 0)
        not_author = commission.author is None or commission.author != request.user.profile

        if not already_applied and accepted < job.manpower_required and not_author:
            JobApplication.objects.create(
                job=job,
                applicant=request.user.profile,
                status='Pending'
            )
            messages.success(request, f"Successfully applied to '{job.role}'.")
            return redirect('commissions:commission', id=commission.id)
    
    if total_manpower == 0:
        commission.status = 'Open'
    elif all(job.accepted_count >= job.manpower_required for job in jobs):
        commission.status = 'Full'
        for job in jobs:
            if job.accepted_count >= job.manpower_required and job.status != 'Full':
                job.status = 'Full'
                job.save()
                job.applications.filter(status='Pending').update(status='Rejected')
    else:
        commission.status = 'Open'
    commission.save()


    return render(request, 'commissions/commission_detail.html', {
        'commission': commission,
        'jobs': jobs,
        'total_manpower': total_manpower,
        'open_manpower': open_manpower,
        'can_apply_filter': can_apply_filter,
        'job_id': job_id,
    })


@login_required
def commission_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        commission = Commission.objects.create(
            title=title,
            description=description,
            author=request.user.profile,
            status='Open' 
        )

        messages.success(request, "Commission created successfully!")
        return redirect('commissions:commission_update', pk=commission.pk)

    return render(request, 'commissions/commission_create.html', {
        'status_choices': Commission.COMMISSION_STATUS_CHOICES  
    })


@login_required
def commission_update(request, pk):
    commission = get_object_or_404(Commission, pk=pk)

    if commission.author is None or request.user.profile != commission.author:
        messages.error(request, "You are not authorized to edit this commission.")
        return redirect('commissions:commissions_list')

    jobs = commission.jobs.all()

    if request.method == 'POST':
        if 'update_commission' in request.POST:
            commission.title = request.POST.get('title')
            commission.description = request.POST.get('description')
            new_status = request.POST.get('status')

            has_jobs = jobs.exists()
            all_jobs_full = all(job.status == 'Full' for job in jobs)

            if new_status == 'Open':
                if not has_jobs:
                    messages.error(request, "Cannot set status to 'Open' with no jobs.")
                elif all_jobs_full:
                    messages.error(request, "Cannot set status to 'Open' if all jobs are full.")
                else:
                    commission.status = 'Open'
                    commission.save()
                    messages.success(request, "Commission updated successfully!")
            elif new_status == 'Full':
                commission.status = 'Full'
                commission.save()

                for job in jobs:
                    job.applications.filter(status='Pending').update(status='Rejected')
                messages.success(request, "Commission marked as full. Pending applications rejected.")
            elif new_status in ['Completed', 'Discontinued']:
                commission.status = new_status
                commission.save()
                messages.success(request, "Commission updated successfully!")
            else:
                messages.error(request, "Invalid status.")

        elif 'add_job' in request.POST:
            role = request.POST.get('role')
            manpower_required = request.POST.get('manpower_required')
            status = request.POST.get('status')

            if role and manpower_required and status:
                Job.objects.create(
                    commission=commission,
                    role=role,
                    status=status,
                    manpower_required=manpower_required
                )
                messages.success(request, "Job added successfully!")
            else:
                messages.error(request, "All job fields are required.")

        return redirect('commissions:commission_update', pk=commission.pk)

    return render(request, 'commissions/commission_update.html', {
    'commission': commission,
    'jobs': jobs,
    'status_choices': Commission.COMMISSION_STATUS_CHOICES,
    })


@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if job.commission.author is None or request.user.profile != job.commission.author:
        messages.error(request, "You are not authorized to manage this job.")
        return redirect('commissions:commissions_list')

    applicants = JobApplication.objects.filter(job=job).order_by(
        models.Case(
            models.When(status='Pending', then=0),
            models.When(status='Accepted', then=1),
            models.When(status='Rejected', then=2),
            default=3,
            output_field=IntegerField(),
        )
    )

    if request.method == 'POST':
        applicant_id = request.POST.get('applicant_id')
        action = request.POST.get('action')

        if applicant_id and action:
            applicant = get_object_or_404(JobApplication, id=applicant_id)

            if action == 'accept':
                accepted_count = JobApplication.objects.filter(job=job, status='Accepted').count()
                if accepted_count >= job.manpower_required:
                    messages.error(request, "Cannot accept more applicants—job is already full.")
                else:
                    applicant.status = 'Accepted'
                    applicant.save()
                    messages.success(request, f"Applicant {applicant.applicant.display_name} accepted successfully.")

            
                    accepted_count += 1  
                    if accepted_count >= job.manpower_required:
                        job.status = 'Full'
                        job.save()
                        job.applications.filter(status='Pending').update(status='Rejected')

            elif action == 'reject':
                was_accepted = applicant.status == 'Accepted'
                applicant.status = 'Rejected'
                applicant.save()
                messages.success(request, f"Applicant {applicant.applicant.display_name} rejected successfully.")

            
                if was_accepted:
                    accepted_count = JobApplication.objects.filter(job=job, status='Accepted').count()
                    if accepted_count < job.manpower_required and job.status == 'Full':
                        job.status = 'Open'
                        job.save()

            return redirect('commissions:job_detail', job_id=job.id)

    return render(request, 'commissions/job_detail.html', {
        'job': job,
        'applicants': applicants,
    })
