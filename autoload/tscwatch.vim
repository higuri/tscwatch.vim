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
from tscwatch import TscWatchRunner
sys.path.pop()
tscwatch = TscWatchRunner()
endpython


function! tscwatch#start(...)
    if 0 < a:0
        let l:lastarg = a:1
    else
        let l:lastarg = ''
    endif
    python3 tscwatch.start(vim.eval('g:tscwatch_tsccmd'), vim.eval('l:lastarg'))
endfunction

function! tscwatch#stop()
    python3 tscwatch.stop()
endfunction

function! tscwatch#restart()
    python3 tscwatch.restart()
endfunction

function! tscwatch#is_running()
    python3 tscwatch.is_running()
endfunction
