$("#criar_sala").keypress(function(event) {
  if ( event.which == 13 ) {
     event.preventDefault();
     texto = $("#criar_sala").val();
     $("#criar_sala").val("");
     location.href="/sala/"+texto+"/";
   }
});

function atualizar_sala() {
  $.post("atualizar", function(data){
    if(data!="0"){
      dic = JSON.parse(data);
      $('#salas').html(dic["salas"]);
    }
  })
  .error(function(data) { alert("Erro ao Atualizar_Sala!"+data); });
}

setInterval('atualizar_sala()', 2000);
