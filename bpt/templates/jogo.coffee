-coffee
  
  carta_sobre (carta) ->
    alert carta.css("background-image")
    alert "aaa"

  $("body").keypress (e) ->
    if e.which == 122
      alert "Uhu"
      $("#_messages_content").focus()

  atualizar () ->
    $.post("atualizar", {"num_jogada":num_jogada}, function(data){
      if(data!="0"){
        dic = JSON.parse(data);
        num_jogada = dic["num_jogada"];
        $('.menu_mao').html(dic["mao"]);
        $('.mesas').html(dic["mesas"]);
        $(".carta").click(carta_clicada);
        $(".carta").hover(carta_sobre);
      }
    })

  setInterval('atualizar()', 3000)
  $(".carta").hover(carta_sobre)
