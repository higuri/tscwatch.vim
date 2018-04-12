"
" autoload/tscwatch.vim
"

let s:curdir = fnamemodify(resolve(expand('<sfile>:p')), ':h')
let s:pyfile = s:curdir . '/python/tscwatch.py'
python3 import vim
execute 'py3file ' . s:pyfile

python3 tscwatch_cmd = vim.eval('g:tscwatch_tsccmd')
let s:lastargs = []
function! tscwatch#start(...)
    python3 tscwatch_args = [vim.eval('expand("%s")' % arg) for arg in vim.eval('a:000')]
    python3 vim.command('let s:lastargs = %r' % tscwatch_args)
    python3 tscwatch_start(tscwatch_cmd, tscwatch_args)
endfunction

function! tscwatch#stop()
    python3 tscwatch_stop()
endfunction

function! tscwatch#restart()
    " stop
    python3 tscwatch_stop()
    " start with last arguments
    python3 lastargs = vim.eval('s:lastargs')
    python3 tscwatch_start(tscwatch_cmd, lastargs)
endfunction

function! tscwatch#is_running()
    python3 tscwatch_is_running()
endfunction
