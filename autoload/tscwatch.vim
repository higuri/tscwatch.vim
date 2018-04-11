"
" autoload/tscwatch.vim
"

let s:curdir = fnamemodify(resolve(expand('<sfile>:p')), ':h')
let s:pyfile = s:curdir . '/python/tscwatch.py'
python3 import vim
execute 'py3file ' . s:pyfile

function! tscwatch#start(...)
    python3 tscwatch_cmd = vim.eval('g:tscwatch_tsccmd')
    python3 tscwatch_args = [vim.eval('expand("%s")' % arg) for arg in vim.eval('a:000')]
    python3 tscwatch_start(tscwatch_cmd, tscwatch_args)
endfunction

function! tscwatch#stop()
    python3 tscwatch_stop()
endfunction

function! tscwatch#is_running()
    python3 tscwatch_is_running()
endfunction
