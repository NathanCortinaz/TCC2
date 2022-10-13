async function runButton() {
  var text = document.getElementById('b_IA').firstChild;

  if (text.data == 'Iniciar análise') {
    text.data = 'Encerrar análise';
    await eel.run()();
  } else {
    text.data = 'Iniciar análise';
    alert('Análise registrada.');
  }
}

eel.expose(checkRunButton);
function checkRunButton() {
  document.getElementById('arquivosMonitorados').innerHTML = 'Realizando análise...';
  var text = document.getElementById('b_IA').firstChild;
  if (text.data != 'Encerrar análise') {
    document.getElementById('arquivosMonitorados').innerHTML = 'Selecione uma ação acima';
    return 1;
  }
}

async function debugButton() {
  var text = document.getElementById('b_D').firstChild;

  if (text.data == 'Debugar') {
    text.data = 'Encerrar análise';
    await eel.debug()();
  } else {
    text.data = 'Debugar';
    alert('Análise registrada.');
  }
}

eel.expose(checkDebugButton);
function checkDebugButton() {
  document.getElementById('arquivosMonitorados').innerHTML = 'Debugando...';
  var text = document.getElementById('b_D').firstChild;
  if (text.data != 'Encerrar análise') {
    document.getElementById('arquivosMonitorados').innerHTML = 'Selecione uma ação acima';
    return 1;
  }
}

async function openResults() {
  await eel.open_results()();
}
