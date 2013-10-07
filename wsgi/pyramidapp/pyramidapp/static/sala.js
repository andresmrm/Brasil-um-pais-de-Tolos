$("#botao_pronto").click(function() {
  $.post("pronto")
  .error(function(data) { alert("erro!"+data); });
});

function atualizar_sala() {
  $.post("atualizar", function(data){
    if(data!="0"){
      dic = JSON.parse(data);
      link = dic["link"];
      if(link){
        window.location.replace(link);
      }else{
        $('#participantes_sala').html(dic["jogadores"]);
      }
    }
  })
  .error(function(data) { alert("Erro ao Atualizar_Sala!"+data); });
}

setInterval('atualizar_sala()', 2000);
