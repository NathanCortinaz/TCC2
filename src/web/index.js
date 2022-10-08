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
  var text = document.getElementById('b_IA').firstChild;
  if (text.data != 'Encerrar análise') {
    return 1;
  }
}

async function debugButton() {
  await eel.debug()();
  alert('Análise registrada.');
}

async function openResults() {
  await eel.open_results()();
}
