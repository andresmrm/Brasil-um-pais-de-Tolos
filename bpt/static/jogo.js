var mode = 0;
var num_jogada = -1;
var cartas = {};
$.getJSON("baralho", function(data){
  cartas = data;
});

function carta_clicada() {
  var id = $(this).attr('id');
  $.post("jogada", {"jogada":modo+id})
  //.success(function(data) { alert("sucesso!"+data); })
  .success(tratar_erro)
  .error(function(data) { alert("erro!"+data); });
  atualizar();
}
$("#jogar_carta").click(function() {
  modo = "J";
});
$("#descartar_carta").click(function() {
  modo = "D";
});
$("#comprar_carta").click(function() {
  modo = "C";
});
$("#mais_din").click(function() {
  $.post("jogada", {"jogada":"G1"})
  .success(tratar_erro)
  .error(function(data) { alert("erro!"+data); });
  atualizar();
});
$("#mais_carta").click(function() {
  $.post("jogada", {"jogada":"M1"})
  .success(tratar_erro)
  .error(function(data) { alert("erro!"+data); });
  atualizar();
});
$("#reiniciar").click(function() {
  $.post("jogada", {"jogada":"R1"})
  .success(tratar_erro)
  .error(function(data) { alert("erro!"+data); });
  num_jogada = -1;
  atualizar();
});
function tratar_erro(msg) {
  if(msg.split(":")[0] == "ERRO") {
    alert(msg);
  }
}
function atualizar() {
  $.post("atualizar", {"num_jogada":num_jogada}, function(data){
    if(data!="0"){
      dic = JSON.parse(data);
      num_jogada = dic["num_jogada"];
      $('.menu_mao').html(dic["mao"]);
      $('.mesas').html(dic["mesas"]);
      $(".carta").click(carta_clicada);
    }
  });
}

setInterval('atualizar()', 3000);

$(".carta").click(carta_clicada);
