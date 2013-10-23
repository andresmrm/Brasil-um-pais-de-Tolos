-coffee
	modo = 0
	modoObj = 0
	num_jogada = -1
	cartas = {}
	jogando_carta = null
	num_params_faltantes = 0
	params_acumulados = []
	#$.getJSON "baralho", (data) -> cartas = data

	tratar_erro = (msg) =>
		if msg.split(":")[0] == "ERRO"
			alert(msg)

	selecionar_jogador = () =>
		$("#titulo_escolha").html('Escolha '+1+' jogador.')
		$("#msg_escolha").show()

	selecionar_carta = (local) =>
		$("#msg_escolha").show()
		#param_carta = null
		#aguardando_param_carta = true
		#$("#escolha_carta").show()

	jog_clicado = () ->
    nome = $(this).attr('id')[3]
    if num_params_faltantes
      params_acumulados += [nome]
      num_params_faltantes -= 1

      if not num_params_faltantes
        codigo = modo+jogando_carta
        for param in params_acumulados
          codigo += "-"+param
        p = $.post("jogada", {"jogada":codigo})
        $("#msg_escolha").hide()
        p.success(tratar_erro)
        p.error (data) -> alert("erro!"+data)
        num_jogada -= 1
        atualizar()

	carta_clicada = () ->
		id = $(this).attr('id')

		if num_params_faltantes
			params_acumulados += [id]
			num_params_faltantes -= 1
		else
			jogando_carta = id
			params_acumulados = []
			parametros = $(this).attr('param')
			num_params_faltantes = parseInt(parametros[0])

			if num_params_faltantes
				if parametros[1] == "j"
					selecionar_jogador()
        #if parametros[1] == "c"
        #	selecionar_carta(parametros[2])

		if not num_params_faltantes
			params_acumulados += [id]
			codigo = modo+jogando_carta
			for param in params_acumulados
				codigo += "-"+param
			p = $.post("jogada", {"jogada":codigo})
			#.success(function(data) { alert("sucesso!"+data); })
			p.success(tratar_erro)
			p.error (data) -> alert("erro!"+data)
			num_jogada -= 1
			atualizar()

	$("#jogar_carta").click () ->
		modo = "J"
		$(modoObj).removeClass("modo-atual")
		modoObj = "#jogar_carta"
		$(modoObj).addClass("modo-atual")
	$("#descartar_carta").click () ->
		modo = "D"
		$(modoObj).removeClass("modo-atual")
		modoObj = "#descartar_carta"
		$(modoObj).addClass("modo-atual")
	$("#comprar_carta").click () ->
		modo = "C"
		$(modoObj).removeClass("modo-atual")
		modoObj = "#comprar_carta"
		$(modoObj).addClass("modo-atual")

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

	$("#bot_escolha_cancelar").click () ->
		$("#msg_escolha").hide()
		num_params_faltantes = 0

	$("body").keypress (e) ->
		if e.which == 122
			$("#carta_zoom").toggle()

	dar_zoom = (event, delta) ->
		event.preventDefault()
		if delta > 0
			$("#carta_zoom").show()
		else
			$("#carta_zoom").hide()

	tirar_zoom = (event, delta) ->
		event.preventDefault()
		if delta < 0
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
        $(".nome_jog").click(jog_clicado)
        $(".carta").bind 'mousewheel', dar_zoom
        $("body").bind 'mousewheel', tirar_zoom
        if dic["fim"]
          $("#msg_fim").show()
        else
          $("#msg_fim").hide()
	setInterval(atualizar,3000)

	$(".carta").hover(carta_sobre)
	$(".carta").bind 'mousewheel', dar_zoom
	#$(".carta").click(carta_clicada)
