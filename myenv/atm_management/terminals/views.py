from django.shortcuts import render, get_object_or_404, redirect
from .models import Terminal
from .forms import TerminalForm
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q

import pandas as pd
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

def upload_terminal_excel(request):
    if request.method == 'POST' and request.FILES['file']:
        excel_file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)
        file_path = fs.path(filename)

        # Read the Excel file using pandas
        df = pd.read_excel(file_path)
        
        # Convert the DataFrame to a list of dictionaries
        terminals = df.to_dict(orient='records')

        # Store the terminals in the session
        request.session['terminals'] = terminals

        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def review_terminals(request):
    terminals = request.session.get('terminals', [])
    return render(request, 'terminals/review_terminals.html', {'terminals': terminals})

def submit_terminals(request):
    if request.method == 'POST':
        terminals = request.session.get('terminals', [])
        for terminal in terminals:
            Terminal.objects.create(
                unit_id=terminal.get('unit_id'),
                terminal_id=terminal.get('terminal_id'),
                terminal_name=terminal.get('terminal_name'),
                branch_name=terminal.get('branch_name'),
                port=terminal.get('port'),
                ip=terminal.get('ip'),
                location=terminal.get('location'),
                type=terminal.get('type'),
                status=terminal.get('status')
            )
        
        # Clear the session data after submission
        request.session['terminals'] = []
        return redirect('terminal_list')
    return redirect('review_terminals')

def terminal_list(request):
    sort_by = request.GET.get('sort_by', 'unit_id')  # Default sort by unit_id if no parameter is provided
    search_query = request.GET.get('search', '')  # Get the search query from the request

    valid_sort_fields = ['unit_id', 'terminal_id', 'terminal_name', 'branch_name', 'port', 'location', 'status']
    if sort_by not in valid_sort_fields:
        sort_by = 'unit_id'  # Default to unit_id if invalid sort_by value is provided

    terminals = Terminal.objects.all().order_by(sort_by)
    print(f'all terminals--------: {terminals}')
    if search_query:
        terminals = terminals.filter(
            Q(unit_id__icontains=search_query) |
            Q(terminal_id__icontains=search_query) |
            Q(terminal_name__icontains=search_query) |
            Q(branch_name__icontains=search_query) |
            Q(port__icontains=search_query) |
            Q(ip__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(status__icontains=search_query)
        )

    paginator = Paginator(terminals, 10)  # Show 10 terminals per page
    page_number = request.GET.get('page')
    terminals = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'terminals/terminal_list_results.html', {
        'terminals': terminals,
    })

    return render(request, 'terminals/terminal_lists.html', {
        'terminals': terminals,
        'sort_by': sort_by,
        'search_query': search_query,
    })


def terminal_new(request):
    if request.method == "POST":
        form = TerminalForm(request.POST)
        if form.is_valid():
            terminal = form.save(commit=False)
            terminal.save()
            return redirect('terminal_detail', pk=terminal.pk)
    else:
        form = TerminalForm()
    return render(request, 'terminals/terminal_edit.html', {'form': form})


@csrf_exempt
def terminal_edit(request, pk):
    terminal = get_object_or_404(Terminal, pk=pk)
    if request.method == "POST":
        form = TerminalForm(request.POST, instance=terminal)
        if form.is_valid():
            terminal = form.save(commit=False)
            terminal.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = TerminalForm(instance=terminal)
        return render(request, 'terminals/terminal_edit.html', {'form': form})

def terminal_new(request):
    if request.method == "POST":
        form = TerminalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('terminal_list')
    else:
        form = TerminalForm()
    return render(request, 'terminals/terminal_new.html', {'form': form})

def port_assignment(request):
    return render(request, 'terminals/port_assignment.html')

def dashboard(request):
    return render(request, 'terminals/dashboard.html')

def accounts(request):
    return render(request, 'terminals/accounts.html')

def terminal_list_by_type(request, terminal_type):
    sort_by = request.GET.get('sort_by', 'unit_id')  # Default sort by unit_id if no parameter is provided
    search_query = request.GET.get('search', '')  # Get the search query from the request

    valid_sort_fields = ['unit_id', 'terminal_id', 'terminal_name', 'branch_name', 'port', 'location', 'status']
    if sort_by not in valid_sort_fields:
        sort_by = 'unit_id'  # Default to unit_id if invalid sort_by value is provided

    filtered_terminals = Terminal.objects.all().filter(type=terminal_type).order_by(sort_by)
    print(f'list_by_type----------: {filtered_terminals}')
    if search_query:
        filtered_terminals = filtered_terminals.filter(
            Q(unit_id__icontains=search_query) |
            Q(terminal_id__icontains=search_query) |
            Q(terminal_name__icontains=search_query) |
            Q(branch_name__icontains=search_query) |
            Q(port__icontains=search_query) |
            Q(ip__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(status__icontains=search_query)
        )

    paginator = Paginator(filtered_terminals, 10)  # Show 10 terminals per page
    page_number = request.GET.get('page')
    filtered_terminals = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'terminals/terminal_list_results.html', {
        'terminals': filtered_terminals,
    })

    return render(request, 'terminals/terminal_lists.html', {
        'terminals': filtered_terminals,
        'sort_by': sort_by,
        'title': terminal_type,
        'search_query': search_query,
    })
    

def hitachi_crm_terminals(request):
    return terminal_list_by_type(request, 'Hitachi CRM')

def ncr_terminals(request):
    return terminal_list_by_type(request, 'NCR')

def pos_terminals(request):
    return terminal_list_by_type(request, 'POS')
