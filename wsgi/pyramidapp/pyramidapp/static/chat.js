var num_msgs = 0;

$("#entrada_msg").keypress(function(event) {
  if ( event.which == 13 ) {
     event.preventDefault();
     texto = $("#entrada_msg").val();
     $("#entrada_msg").val("");
     $.post("enviar_msg", {"msg":texto})
     .error(function(data) { alert("Erro ao Enviar_Msg!"+data); });
     atualizar_chat();
   }
});

function atualizar_chat() {
  $.post("ret_msgs", {"num":num_msgs}, function(data){
    if(data!="0"){
      dic = jQuery.parseJSON(data);
      $("#msgs").html(dic.msgs);
    }
  })
  .error(function(data) { alert("Erro ao Atualizar_Chat!"+data); });
}

setInterval('atualizar_chat()', 2000);
