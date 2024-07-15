from django.shortcuts import render, get_object_or_404, redirect
from .models import Terminal
from .forms import TerminalForm
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q

def terminal_list(request):
    sort_by = request.GET.get('sort_by', 'unit_id')  # Default sort by unit_id if no parameter is provided
    search_query = request.GET.get('search', '')  # Get the search query from the request

    valid_sort_fields = ['unit_id', 'terminal_id', 'terminal_name', 'branch_name', 'port', 'location', 'status']
    if sort_by not in valid_sort_fields:
        sort_by = 'unit_id'  # Default to unit_id if invalid sort_by value is provided

    terminals = Terminal.objects.all().order_by(sort_by)

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

    paginator = Paginator(terminals, 3)  # Show 10 terminals per page
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

    terminals = Terminal.objects.all().filter(type=terminal_type).order_by(sort_by)

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

    paginator = Paginator(terminals, 3)  # Show 10 terminals per page
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
    

def hitachi_crm_terminals(request):
    return terminal_list_by_type(request, 'Hitachi CRM')

def ncr_terminals(request):
    return terminal_list_by_type(request, 'NCR')

def pos_terminals(request):
    return terminal_list_by_type(request, 'POS')
