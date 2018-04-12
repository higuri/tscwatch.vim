"
" plugin/tscwatch.vim
"
if exists('g:loaded_tscwatch')
    finish
endif

" TODO: support python2.
if !has('python3')
    echo 'ERROR: vim-tsc requires +python3'
    finish
endif

let g:loaded_tscwatch = 1
let s:save_cpo = &cpo
set cpo&vim

if !exists('g:tscwatch_tsccmd')
    let g:tscwatch_tsccmd = 'tsc'
endif

command! -nargs=* TscWatchStart call tscwatch#start(<f-args>)
command! -nargs=0 TscWatchStop call tscwatch#stop()
command! -nargs=0 TscWatchRestart call tscwatch#restart()
command! -nargs=0 TscWatchIsRunning call tscwatch#is_running()
autocmd VimLeave * call tscwatch#stop()

let &cpo = s:save_cpo
unlet s:save_cpo
