from django.contrib.sessions.backends.base import SessionBase
from django.shortcuts import render
from django.http import HttpRequest

# Create your views here.

from lisp.lisp.interpreter import evaluate, LispError


def evaluateRequest(request: HttpRequest):
    session: SessionBase = request.session
    source, stdout, stderr = '', '', ''
    try:
        source = request.POST.get('inputtext').strip()
        stdout = evaluate(source)
    except KeyError:
        source = ''
    except LispError as ex:
        stderr = ex.message

    context = {
        'inputtext': source,
        'stdout': stdout,
        'stderr': stderr
    }
    return render(request, 'lisp/index.html', context)
