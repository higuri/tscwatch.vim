"
" autoload/tscwatch.vim
"

" Import python/tscwatch.py
python3 << endpython
import os
import sys
import vim
sys.path.append(os.path.join(
    (os.path.dirname(vim.eval('expand("<sfile>")'))),
    'python'))
import tscwatch
sys.path.pop()
endpython

python3 tscwatch_cmd = vim.eval('g:tscwatch_tsccmd')
let s:lastargs = []
function! tscwatch#start(...)
    python3 tscwatch_args = [vim.eval('expand("%s")' % arg) for arg in vim.eval('a:000')]
    python3 vim.command('let s:lastargs = %r' % tscwatch_args)
    python3 tscwatch.tscwatch_start(tscwatch_cmd, tscwatch_args)
endfunction

function! tscwatch#stop()
    python3 tscwatch.tscwatch_stop()
endfunction

function! tscwatch#restart()
    " stop
    python3 tscwatch.tscwatch_stop()
    " start with last arguments
    python3 lastargs = vim.eval('s:lastargs')
    python3 tscwatch.tscwatch_start(tscwatch_cmd, lastargs)
endfunction

function! tscwatch#is_running()
    python3 tscwatch.tscwatch_is_running()
endfunction
