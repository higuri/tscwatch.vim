"
" plugin/tscwatch.vim
"

" TODO: support python2.
if !has('python3')
    finish
endif
if exists("g:loaded_tscwatch")
    finish
endif
let g:loaded_tscwatch = 1
let s:save_cpo = &cpo
set cpo&vim

command! -nargs=* TscWatchStart call tscwatch#start(<f-args>)
command! -nargs=0 TscWatchStop call tscwatch#stop()
command! -nargs=0 TscWatchIsRunning call tscwatch#is_running()
autocmd VimLeave * call tscwatch#stop()

let &cpo = s:save_cpo
unlet s:save_cpo
