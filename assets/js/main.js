(function(){
  var input=document.querySelector('.search-teaser input');
  var words=['hidden gems','unofficial patches','spiritual successors','must-have software','buried memories','the ones that survived'];
  var w=0,c=0,del=false;
  function tick(){
    if(!input)return;
    var t=words[w];
    c+=del?-1:1;
    input.placeholder='dig for '+t.slice(0,c)+' ...';
    var d=del?38:92;
    if(!del&&c===t.length){d=1700;del=true}
    if(del&&c===0){del=false;w=(w+1)%words.length;d=380}
    setTimeout(tick,d);
  }
  tick();

  var toast=document.querySelector('.key-toast');
  var tm=null;
  addEventListener('keydown',function(e){
    if(!e.key||e.repeat)return;
    if(e.target&&/INPUT|TEXTAREA/.test(e.target.tagName))return;
    if(e.key.toLowerCase()==='s'){
      document.body.classList.add('s-hit');
      if(toast)toast.classList.add('show');
      clearTimeout(tm);
      tm=setTimeout(function(){
        document.body.classList.remove('s-hit');
        if(toast)toast.classList.remove('show');
      },950);
    }
  });
})();
