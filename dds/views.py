from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from .models import Record, RecordStatus, RecordType, RecordCategory, RecordSubcategory
from .forms import (
    RecordForm,
    RecordTypeForm,
    RecordStatusForm,
    RecordCategoryForm,
    RecordSubcategoryForm,
    RecordFilterForm,
)


def record_list(request):
    records = Record.objects.select_related('status', 'type', 'category', 'subcategory').all()
    filter_form = RecordFilterForm(request.GET)
    if filter_form.is_valid():
        data = filter_form.cleaned_data
        if data.get('date_from'):
            records = records.filter(date__gte=data['date_from'])
        if data.get('date_to'):
            records = records.filter(date__lte=data['date_to'])
        if data.get('status'):
            records = records.filter(status=data['status'])
        if data.get('type'):
            records = records.filter(type=data['type'])
        if data.get('category'):
            records = records.filter(category=data['category'])
        if data.get('subcategory'):
            records = records.filter(subcategory=data['subcategory'])

    return render(request, 'dds/record_list.html', {
        'records': records,
        'filter_form': filter_form,
    })

def record_create(request):
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('record_list')
    else:
        form = RecordForm()

    return render(
        request,
        'dds/record_form.html',
        {
            'form': form,
            'title': 'Создать запись ДДС',
            'categories': RecordCategory.objects.all(),
            'subcategories': RecordSubcategory.objects.all(),
        },
    )

def record_update(request, pk):
    record = get_object_or_404(Record, pk=pk)
    if request.method == 'POST':
        form = RecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('record_list')
    else:
        form = RecordForm(instance=record)

    return render(
        request,
        'dds/record_form.html',
        {
            'form': form,
            'title': 'Редактировать запись ДДС',
        },
    )

def record_delete(request, pk):
    record = get_object_or_404(Record, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('record_list')
    return render(
        request,
        'dds/confirm_delete.html',
        {
            'object': record,
            'cancel_url': reverse('record_list'),
            'title': 'Удалить запись ДДС',
        },
    )

def ajax_load_categories(request):
    type_id = request.GET.get('type_id')
    categories = RecordCategory.objects.filter(type_id=type_id).order_by('name')
    return JsonResponse([{'id': c.id, 'name': c.name} for c in categories], safe=False)


def ajax_load_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = RecordSubcategory.objects.filter(category_id=category_id).order_by('name')
    return JsonResponse([{'id': s.id, 'name': s.name} for s in subcategories], safe=False)

# Status management

def manage_statuses(request):
    statuses = RecordStatus.objects.all()
    if request.method == 'POST':
        form = RecordStatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_statuses')
    else:
        form = RecordStatusForm()
    return render(
        request,
        'dds/manage_statuses.html',
        {'statuses': statuses, 'form': form},
    )


def edit_status(request, pk):
    status = get_object_or_404(RecordStatus, pk=pk)
    if request.method == 'POST':
        form = RecordStatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            return redirect('manage_statuses')
    else:
        form = RecordStatusForm(instance=status)
    return render(
        request,
        'dds/reference_form.html',
        {'form': form, 'title': 'Редактировать статус', 'cancel_url': reverse('manage_statuses')},
    )


def delete_status(request, pk):
    status = get_object_or_404(RecordStatus, pk=pk)
    if request.method == 'POST':
        status.delete()
        return redirect('manage_statuses')
    return render(
        request,
        'dds/confirm_delete.html',
        {'object': status, 'cancel_url': reverse('manage_statuses'), 'title': 'Удалить статус'},
    )

# Type management

def manage_types(request):
    types = RecordType.objects.all()
    if request.method == 'POST':
        form = RecordTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_types')
    else:
        form = RecordTypeForm()
    return render(request, 'dds/manage_types.html', {'types': types, 'form': form})


def edit_type(request, pk):
    record_type = get_object_or_404(RecordType, pk=pk)
    if request.method == 'POST':
        form = RecordTypeForm(request.POST, instance=record_type)
        if form.is_valid():
            form.save()
            return redirect('manage_types')
    else:
        form = RecordTypeForm(instance=record_type)
    return render(
        request,
        'dds/reference_form.html',
        {'form': form, 'title': 'Редактировать тип', 'cancel_url': reverse('manage_types')},
    )


def delete_type(request, pk):
    record_type = get_object_or_404(RecordType, pk=pk)
    if request.method == 'POST':
        record_type.delete()
        return redirect('manage_types')
    return render(
        request,
        'dds/confirm_delete.html',
        {'object': record_type, 'cancel_url': reverse('manage_types'), 'title': 'Удалить тип'},
    )

# Category management

def manage_categories(request):
    categories = RecordCategory.objects.select_related('type').all()
    if request.method == 'POST':
        form = RecordCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_categories')
    else:
        form = RecordCategoryForm()
    return render(
        request,
        'dds/manage_categories.html',
        {'categories': categories, 'form': form},
    )


def edit_category(request, pk):
    category = get_object_or_404(RecordCategory, pk=pk)
    if request.method == 'POST':
        form = RecordCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('manage_categories')
    else:
        form = RecordCategoryForm(instance=category)
    return render(
        request,
        'dds/reference_form.html',
        {'form': form, 'title': 'Редактировать категорию', 'cancel_url': reverse('manage_categories')},
    )


def delete_category(request, pk):
    category = get_object_or_404(RecordCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('manage_categories')
    return render(
        request,
        'dds/confirm_delete.html',
        {'object': category, 'cancel_url': reverse('manage_categories'), 'title': 'Удалить категорию'},
    )

# Subcategory management

def manage_subcategories(request):
    subcategories = RecordSubcategory.objects.select_related('category__type').all()
    if request.method == 'POST':
        form = RecordSubcategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_subcategories')
    else:
        form = RecordSubcategoryForm()
    return render(
        request,
        'dds/manage_subcategories.html',
        {'subcategories': subcategories, 'form': form},
    )


def edit_subcategory(request, pk):
    subcategory = get_object_or_404(RecordSubcategory, pk=pk)
    if request.method == 'POST':
        form = RecordSubcategoryForm(request.POST, instance=subcategory)
        if form.is_valid():
            form.save()
            return redirect('manage_subcategories')
    else:
        form = RecordSubcategoryForm(instance=subcategory)
    return render(
        request,
        'dds/reference_form.html',
        {'form': form, 'title': 'Редактировать подкатегорию', 'cancel_url': reverse('manage_subcategories')},
    )


def delete_subcategory(request, pk):
    subcategory = get_object_or_404(RecordSubcategory, pk=pk)
    if request.method == 'POST':
        subcategory.delete()
        return redirect('manage_subcategories')
    return render(
        request,
        'dds/confirm_delete.html',
        {'object': subcategory, 'cancel_url': reverse('manage_subcategories'), 'title': 'Удалить подкатегорию'},
    )
