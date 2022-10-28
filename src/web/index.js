async function runButton() {
  var text = document.getElementById('b_IA').firstChild;

  if (text.data == 'Iniciar análise') {
    text.data = 'Encerrar análise';
    document.getElementById('msgBox').innerHTML = 'Aguarde, iniciando análise...';
    await eel.run()();
  } else {
    text.data = 'Iniciar análise';
    alert('Análise registrada.');
  }
}

eel.expose(checkRunButton);
function checkRunButton() {
  document.getElementById('msgBox').innerHTML = 'Realizando análise...';
  var text = document.getElementById('b_IA').firstChild;
  if (text.data != 'Encerrar análise') {
    document.getElementById('msgBox').innerHTML = 'Selecione uma ação acima';
    return 1;
  }
}

async function debugButton() {
  var text = document.getElementById('b_D').firstChild;

  if (text.data == 'Depurar') {
    text.data = 'Encerrar depuração';
    document.getElementById('msgBox').innerHTML = 'Aguarde, iniciando debug...';
    await eel.debug()();
  } else {
    text.data = 'Depurar';
    alert('Análise registrada.');
  }
}

eel.expose(checkDebugButton);
function checkDebugButton() {
  document.getElementById('msgBox').innerHTML = 'Depurando...';
  var text = document.getElementById('b_D').firstChild;
  if (text.data != 'Encerrar depuração') {
    document.getElementById('msgBox').innerHTML = 'Selecione uma ação acima';
    return 1;
  }
}

async function openResults() {
  await eel.open_results()();
}

eel.expose(camError);
function camError() {
  document.getElementById('msgBox').innerHTML = 'Selecione uma ação acima';
  alert('Não foi possível acessar a webcam do dispositivo.');
  window.close();
}
