-coffee

	modo = 0
	num_jogada = -1
	cartas = {}
	jogando_carta = null
	aguardando_param_carta = false
	param_carta = null
	#$.getJSON "baralho", (data) -> cartas = data

	tratar_erro = (msg) =>
		if msg.split(":")[0] == "ERRO"
			alert(msg)

	selecionar_jogador = () =>
		$("#escolha_jogador").show()

	selecionar_carta = (local) =>
		param_carta = null
		aguardando_param_carta = true
		$("#escolha_carta").show()

	carta_clicada = () ->
		id = $(this).attr('id')
		if not aguardando_param_carta
			parametros = $(this).attr('param')
			if parseInt(parametros[0]) > 0
				jogando_carta = id
				if parametros[1] == "j"
					selecionar_jogador()
				if parametros[1] == "c"
					selecionar_carta(parametros[2])
			else
				p = $.post("jogada", {"jogada":modo+id})
				#.success(function(data) { alert("sucesso!"+data); })
				p.success(tratar_erro)
				p.error (data) -> alert("erro!"+data)
				atualizar()
		else
			param_carta = id

	$("#jogar_carta").click () -> modo = "J"
	$("#descartar_carta").click () -> modo = "D"
	$("#comprar_carta").click () -> modo = "C"

	$("#mais_din").click () ->
		p = $.post("jogada", {"jogada":"G1"})
		p.success(@tratar_erro)
		p.error (data) -> alert("erro!"+data)
		atualizar()
	$("#mais_carta").click () ->
		p = $.post("jogada", {"jogada":"M1"})
		p.success(@tratar_erro)
		p.error (data) -> alert("erro!"+data)
		atualizar()
	#$("#reiniciar").click () ->
	#	p = $.post("jogada", {"jogada":"R1"})
	#	p.success(tratar_erro)
	#	p.error (data) ->
	#		alert("erro!"+data)
	#	num_jogada = -1
	#	atualizar()
  
	carta_sobre = (carta) ->
		$("#carta_zoom").css("background-image", $(@).css("background-image"))

	$("body").keypress (e) ->
		if e.which == 122
			$("#carta_zoom").toggle()
	dar_zoom = (event, delta) ->
    event.preventDefault()
    if delta > 0
      $("#carta_zoom").show()
    else
      $("#carta_zoom").hide()

	atualizar = () ->
		$.post "atualizar", {"num_jogada":num_jogada}, (data) ->
			if data != "0"
        dic = JSON.parse(data)
        num_jogada = dic["num_jogada"]
        $('.menu_mao').html(dic["mao"])
        $('.mesas').html(dic["mesas"])
        $(".carta").click(carta_clicada)
        $(".carta").hover(carta_sobre)
        $(".carta").bind 'mousewheel', dar_zoom
        if dic["fim"]
          $("#msg_fim").show()
        else
          $("#msg_fim").hide()
	setInterval(atualizar,3000)

	$(".carta").hover(carta_sobre)
	$(".carta").bind 'mousewheel', dar_zoom
	#$(".carta").click(carta_clicada)
