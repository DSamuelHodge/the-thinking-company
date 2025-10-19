import os
import json
import textwrap
import inspect
import asyncio
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

def short(x, n=500):
    try:
        s = json.dumps(x, indent=2) if not isinstance(x, str) else x
    except Exception:
        s = str(x)
    return (s[:n] + '...') if len(s) > n else s

def verify_jira():
    try:
        from jira_mcp import search_issues
    except Exception as e:
        return False, f"Import error: {e}"
    try:
        print('Calling JIRA search_issues("project = TEST")')
        fn = getattr(search_issues, 'fn', None) or (search_issues if callable(search_issues) else None)
        if fn is None:
            return False, "Cannot resolve callable for search_issues"
        if inspect.iscoroutinefunction(fn):
            res = asyncio.run(fn("project = TEST"))
        else:
            res = fn("project = TEST")
        return True, short(res)
    except Exception as e:
        return False, str(e)

def verify_confluence():
    try:
        from confluence_mcp import search_pages
    except Exception as e:
        return False, f"Import error: {e}"
    try:
        print('Calling Confluence search_pages("test")')
        fn = getattr(search_pages, 'fn', None) or (search_pages if callable(search_pages) else None)
        if fn is None:
            return False, "Cannot resolve callable for search_pages"
        if inspect.iscoroutinefunction(fn):
            res = asyncio.run(fn("test"))
        else:
            res = fn("test")
        return True, short(res)
    except Exception as e:
        return False, str(e)

def verify_cal():
    try:
        from cal_mcp import get_event_types
    except Exception as e:
        return False, f"Import error: {e}"
    try:
        print('Calling Cal.com get_event_types()')
        fn = getattr(get_event_types, 'fn', None) or (get_event_types if callable(get_event_types) else None)
        if fn is None:
            return False, "Cannot resolve callable for get_event_types"
        if inspect.iscoroutinefunction(fn):
            res = asyncio.run(fn())
        else:
            res = fn()
        return True, short(res)
    except Exception as e:
        return False, str(e)

def verify_resend(send_email=False):
    try:
        from resend_mcp import send_email
    except Exception as e:
        return False, f"Import error: {e}"
    if not send_email:
        return None, "Skipped (send_email requires explicit --send-emails flag)"
    try:
        print('Sending test email via Resend (this will actually send an email)')
        fn = getattr(send_email, 'fn', None) or (send_email if callable(send_email) else None)
        if fn is None:
            return False, "Cannot resolve callable for send_email"
        if inspect.iscoroutinefunction(fn):
            res = asyncio.run(fn(os.getenv('RECIPIENT'), 'Test from verify_connectors', '<p>Test</p>'))
        else:
            res = fn(os.getenv('RECIPIENT'), 'Test from verify_connectors', '<p>Test</p>')
        return True, short(res)
    except Exception as e:
        return False, str(e)

def main():
    print('\nVERIFY MCP CONNECTORS\n')
    results = {}
    ok, msg = verify_jira()
    results['jira'] = (ok, msg)
    ok, msg = verify_confluence()
    results['confluence'] = (ok, msg)
    ok, msg = verify_cal()
    results['cal'] = (ok, msg)
    # Resend skipped by default
    ok, msg = verify_resend(send_email=False)
    results['resend'] = (ok, msg)

    print('\nRESULTS:')
    for k, (ok, msg) in results.items():
        state = 'SKIPPED' if ok is None else ('OK' if ok else 'ERROR')
        print(f"- {k.upper():10} {state}\n  {textwrap.indent(str(msg), '  ')}\n")

if __name__ == '__main__':
    main()
