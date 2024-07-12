from django.shortcuts import render, get_object_or_404, redirect
from .models import Terminal
from .forms import TerminalForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def terminal_list(request):
    terminals = Terminal.objects.all()
    return render(request, 'terminals/terminal_lists.html', {'terminals': terminals})

def terminal_detail(request, pk):
    terminal = get_object_or_404(Terminal, pk=pk)
    return render(request, 'terminals/terminal_detail.html', {'terminal': terminal})

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
    terminals = Terminal.objects.filter(type=terminal_type)
    return render(request, 'terminals/terminal_lists.html', {'terminals': terminals, 'title': terminal_type})

def hitachi_crm_terminals(request):
    return terminal_list_by_type(request, 'Hitachi CRM')

def ncr_terminals(request):
    return terminal_list_by_type(request, 'NCR')

def pos_terminals(request):
    return terminal_list_by_type(request, 'POS')