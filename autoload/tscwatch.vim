"
" autoload/tscwatch.vim
"

let s:curdir = fnamemodify(resolve(expand('<sfile>:p')), ':h')
let s:pyfile = s:curdir . '/python/tscwatch.py'
python3 import vim
execute 'py3file ' . s:pyfile

function! tscwatch#start(...)
    python3 args = [vim.eval('expand("%s")' % arg) for arg in vim.eval('a:000')]
    python3 tscwatch_start(args)
endfunction

function! tscwatch#stop()
    python3 tscwatch_stop()
endfunction
